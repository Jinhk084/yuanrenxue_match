const fs = require('fs');
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;

// 读取路径和保存路径
readPath = 'js_part2.js'
writePath = 'part2_encode.js'


// 读取文件
let input_code = fs.readFileSync(readPath, { encoding: "utf-8" });

// 转换为ast树
let ast = parser.parse(input_code);
/*-------------------------------------------------------------------------------------------------*/

let newAst = parser.parse('')
// 大数组
newAst.program.body.push(ast.program.body[0]) // 大数组
newAst.program.body.push(ast.program.body[1]) // 数据顺序还原函数
newAst.program.body.push(ast.program.body[2]) // 解密函数
// 解密函数名
decrypt_func = ast.program.body[2].declarations[0].id.name
// 将3部分代码转换成js,并且执行加载到内存
eval(generator(newAst, { compact: true }).code)


// 解密函数还原:
traverse(ast, {
    VariableDeclaration(path) {
        // 当变量名与解密函数名相同的时候,就执行相应的操作
        let { scope, node } = path
        if (!(node.declarations[0].id.name == decrypt_func)) return
        let binding = scope.getBinding(decrypt_func)
        // 判断初始值是否被更改
        if (!binding || !binding.constant) return
        for (let referencePath of binding.referencePaths) {
            if (referencePath.parentPath.node.type == 'CallExpression') {
                // 替换操作
                value = eval(referencePath.parentPath.toString())
                referencePath.parentPath.replaceInline(t.valueToNode(value))
            }
        }
    }
})

// 删除大数组、数据位移、解密函数
ast.program.body.shift()
ast.program.body.shift()
ast.program.body.shift()

// 16进制转字符串: "\x49\x4d\x4b\x2b\x52\x41\x3d\x3d" --> "IMK+RA=="
traverse(ast, {
    StringLiteral(path) {
        if (path.node.extra) {
            delete path.node.extra
        }
    }
})

// 常量求值:  "jDu" + "wO" --> "jDuwO"
traverse(ast, {
    "BinaryExpression"(path) {
        const { confident, value } = path.evaluate();
        // 过滤
        if (value == "Infinity" || !confident) return;
        path.replaceInline(t.valueToNode(value));
    }
})


/**
 * 对象内容转换
 *    var d = {};                                var d = {
 *    d["TEpfG"] = "gger";       ---->               "TEpfG": "gger";
 *                                               };
 */
traverse(ast, {
    BlockStatement: {
        enter(path) {
            let { node } = path;
            // 判断第一部分是否为： var d = {}
            if (!t.isVariableDeclaration(node.body[0])) return;
            if (!t.isObjectExpression(node.body[0].declarations[0].init)) return; // 定义书否为对象: {}
            if (!node.body[0].declarations[0].init.properties.length === 0) return; // 判断对象中是否为空: {}

            // 判断第二部分是否为：d["TEpfG"] = "xxx";
            let obj_name = node.body[0].declarations[0].id.name
            if (!t.isExpressionStatement(node.body[1])) return;
            if (!node.body[1].expression.left.object.name == obj_name) return;

            let delete_index = 0 // 用来计算: d["TEpfG"] = "xxx" 有多少,后续根据这个索引进行删除
            node.body.forEach(v => {
                // 过滤不满足要求的节点
                if (!v.type === 'ExpressionStatement') return;
                if (!(v.expression && v.expression.left && v.expression.left.object && v.expression.left.object.name === obj_name)) return; // 判断左边部分的name是不是obj_name
                // 获取: d["TEpfG"] 中的 "TEpfG" 当作key
                key_ = v.expression.left.property
                // 获取右节点当作value
                value_ = v.expression.right
                // 构造节点
                new_node = t.ObjectProperty(key_, value_)
                // 添加到指定容器中
                node.body[0].declarations[0].init.properties.push(new_node)
                // 满足要求的索引自增1
                delete_index += 1
            })
            // 根据索引删除node.body中的指定内容
            node.body.splice(1, delete_index)
        }
    }
})

// 花指令重定向
traverse(ast, {
    VariableDeclarator: {
        enter(path) {
            let { node } = path;
            if (!(node.init && node.init.properties && node.init.properties[0].type === 'ObjectProperty')) return; // 过滤不满足要求的内容
            // 获取指令的对象名
            let obj_name = node.id.name
            // 获取后一个兄弟节点
            NextSibling = path.parentPath.getNextSibling()
            // 判断是否是对对象重新赋值 即: var f = d;
            if (!NextSibling.isVariableDeclaration()) return;
            if (!(NextSibling.node.declarations[0].init.name === obj_name)) return;

            // 获取变量, 即: var f = d; 中的 f
            let quote = NextSibling.node.declarations[0].id.name
            node.id.name = quote
            // 删除节点
            NextSibling.remove()
        }
    }
})

ast = parser.parse(generator(ast).code)
// 花指令嵌套解决
traverse(ast, {
    VariableDeclarator: {
        enter(path) {
            let { node, scope } = path;
            if (!(node.init && node.init.properties && node.init.properties[0].type === 'ObjectProperty')) return;

            let obj_name = node.id.name
            let bind = scope.getBinding(obj_name)

            bind.referencePaths.map(v => {
                if (v.parentPath.type == 'ReturnStatement') return;
                let key = v.parent.property.value
                let right = ''
                node.init.properties.map(q => {
                    if (q.key.value === key) { // 如果取出来的key与花指令中的key一样
                        right = q.value
                        return
                    }
                })

                if (right.type === 'StringLiteral') { // 字符串花指令
                    v.parentPath.replaceInline(t.StringLiteral(right.value))
                } else if (right.type === 'FunctionExpression') { // 函数花指令
                    // 过滤
                    if (!(v.parentPath.parentPath.parentPath.type === 'ReturnStatement')) return;
                    if (!(v.parentPath.parentPath.parentPath.parentPath.type === 'BlockStatement')) return;

                    if (right.body.body[0].argument.type === 'BinaryExpression') { // 判断是否是: n + o;
                        let operator = right.body.body[0].argument.operator
                        let lef = v.parentPath.parent.arguments[0].name
                        let rig = v.parentPath.parent.arguments[1].name
                        v.parentPath.parentPath.replaceWithSourceString(lef + operator + rig)

                    } else if (right.body.body[0].argument.type === 'CallExpression') { // 判断是否是: n() 、 n(o);
                        let arg = v.parentPath.parent.arguments
                        if (arg.length === 1) {
                            // 判断当传入一个参数的时候,是否是函数的调用
                            if (right.body.body[0].argument.callee) {
                                let arg0 = v.parentPath.parent.arguments[0].name
                                v.parentPath.parentPath.replaceWithSourceString(arg0 + '()')
                                return;
                            }
                            console.log('当花指令传入参数为1个的时候,不是返回调用的值');
                        } else if (arg.length === 2) {
                            let lef = v.parentPath.parent.arguments[0].name
                            let rig = v.parentPath.parent.arguments[1].name
                            v.parentPath.parentPath.replaceWithSourceString(lef + '(' + rig + ')')
                        } else {
                            console.log('花指令内容超过2个参数');
                        }
                    } else {
                        console.log('花指令含有其它类型(除字符串和函数)');
                    }

                } else {
                    // 都是一些不存在的内容
                    // console.log(generator(right).code);
                }
            })
        }
    }
})

// 花指令剔除
traverse(ast, {
    VariableDeclarator: { // 获取所有变量声明
        exit(path) {
            // 将对象进行替换
            let { node } = path; //获取路径节点
            if (!t.isObjectExpression(node.init)) // 不是对象表达式则退出
                return;
            var objPropertiesList = node.init.properties;   // 获取对象内所有属性
            if (objPropertiesList.length == 0) // 对象内属性列表为0(空)则退出
                return;
            var objName = node.id.name;  // 获取对象名
            let scope = path.scope; //获取路径的作用域
            let binding = scope.getBinding(objName); // 获取作用域绑定
            if (!binding || binding.constantViolations.length > 0) { //检查该变量的值是否被修改
                return;
            }
            let paths = binding.referencePaths; //绑定引用的路径
            let paths_sums = 0; //路径计数
            objPropertiesList.map(prop => {
                var key = prop.key.value; // 获取对象属性名
                // 剔除关键代码
                if (t.isStringLiteral(prop.value)) {  // 字符串花指令剔除
                    var retStmt = prop.value.value; // 属性值的值 即A:B中的B部分
                    path.scope.traverse(path.scope.block, { // 遍历当前标识符作用域下面的内容
                        MemberExpression: function (_path) { // 成员表达式
                            let _path_binding = _path.scope.getBinding(objName); //当前作用域获取绑定
                            if (_path_binding != binding) //两者绑定对比(可删)
                                return;
                            let _node = _path.node;
                            if (!t.isIdentifier(_node.object) || _node.object.name !== objName) //节点对象type|节点对象名验证
                                return;
                            if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property))) //节点属性可迭代字符验证|标识符验证
                                return;
                            if (!(_node.property.value == key || _node.property.name == key)) //节点属性值与名称等于指定值验证
                                return;
                            if (!t.isStringLiteral(_node.property) || _node.property.value != key) //节点属性可迭代字符判定|节点属性值等于指定值验证
                                return;
                            _path.replaceInline(t.stringLiteral(retStmt))//节点替换
                            paths_sums += 1; //删除计数标志
                        }
                    })
                } else if (t.isFunctionExpression(prop.value)) { // 函数花指令还原
                    var retStmt = prop.value.body.body[0]; //定位到ReturnStatement
                    path.scope.traverse(path.scope.block, {
                        CallExpression: function (_path) { //调用表达式匹配
                            let _path_binding = _path.scope.getBinding(objName);//当前作用域获取绑定
                            if (_path_binding != binding)  //两者绑定对比
                                return;
                            if (!t.isMemberExpression(_path.node.callee))//成员表达式判定
                                return;
                            var _node = _path.node.callee; //回调函数节点
                            if (!t.isIdentifier(_node.object) || _node.object.name !== objName)//非标识符检测||节点对象名全等验证
                                return;
                            if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property)))//节点属性非可迭代字符验证||节点属性标识符验证
                                return;
                            if (!(_node.property.value == key || _node.property.name == key))//节点属性值与名称等于指定值验证
                                return;
                            if (!t.isStringLiteral(_node.property) || _node.property.value != key)//节点属性可迭代字符验证与节点属性值与指定值等于验证
                                return;
                            var args = _path.node.arguments;//获取节点的参数
                            // 二元运算
                            if (t.isBinaryExpression(retStmt.argument) && args.length === 2) { //二进制表达式判定且参数为两个
                                _path.replaceInline(t.binaryExpression(retStmt.argument.operator, args[0], args[1]));//二进制表达式替换当前节点
                            }
                            // 逻辑运算
                            else if (t.isLogicalExpression(retStmt.argument) && args.length == 2) { //与二元运算一样
                                _path.replaceInline(t.logicalExpression(retStmt.argument.operator, args[0], args[1]));
                            }
                            // 函数调用
                            else if (t.isCallExpression(retStmt.argument) && t.isIdentifier(retStmt.argument.callee)) {//回调函数表达式判定及回调参数部分判定
                                _path.replaceInline(t.callExpression(args[0], args.slice(1)))
                            }
                            paths_sums += 1;//删除计数标志
                        }
                    })
                }
            });
            path.remove()
            // 删除obj定义
            // if (paths_sums == paths.length) {//若绑定的每个路径都已处理 ，则移除当前路径
            //     path.remove();//删除路径
            // }
        }
    },
});

// 删除冗余代码(用于删除花指令剔除之后,if判断语句一定不会走的分支)
traverse(ast, {
    IfStatement: {
        exit(path) {
            // 规范if语句,给if语句添加{} (如果前面处理过,则这边不需要处理)
            // let { test, consequent, alternate } = path.node;
            // if (!t.isBlockStatement(consequent)) {
            //     path.node.consequent = t.BlockStatement([consequent])
            // }
            // if (alternate !== null && !t.isBlockStatement(alternate)) {
            //     path.node.alternate = t.BlockStatement([alternate])
            // }
            let { node } = path;

            if (t.isStringLiteral(node.test.left) && t.isStringLiteral(node.test.right)) {
                // 获取节点在容器中的索引
                let index = path.key
                // 获取容器名字
                let container = path.listKey
                if (!(index !== undefined && container !== undefined)) throw '--------不存在容器中--------'

                // 构造新body节点
                let new_body = [];
                let bool = eval(generator(node.test).code)
                if (bool) { // 如果为真,则取if中的内容(consequent)
                    let old_body = node.consequent.body;
                    new_body = new_body.concat(old_body);
                } else { // 否则为假,取else中的内容(alternate)
                    let old_body = node.alternate.body;
                    new_body = new_body.concat(old_body);
                }
                // 添加到原节点的同级目录
                new_body.reverse().map(v => {
                    path.parent[container].splice(index, 0, v)
                })
                // 删除原节点
                path.remove();
            }
        }
    },
})

// 控制流还原
traverse(ast, {
    WhileStatement: {
        exit(path) {
            let { node } = path;
            // 判断是否是目标节点
            if (!(t.isUnaryExpression(node.test) || t.isBooleanLiteral(node.test))) return; // 判断类型:   while(!![])   while(true)
            if (!(node.test.value || node.test.prefix)) return; // 判断值: while中的值是否为true
            if (!t.isBlockStatement(node.body)) return; // 判断是否是块语句

            // 检查块语句中的内容是否满足要求
            let body = node.body.body;
            if (!(t.isSwitchStatement(body[0]) && t.isMemberExpression(body[0].discriminant) && t.isBreakStatement(body[1]))) return; // 判断switch \ switch(值) \ break

            // 获取数组名 和 自增变量名
            arrName = body[0].discriminant.object.name;
            argName = body[0].discriminant.property.argument.name;
            let arr = [] // split切割后的数组
            // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!如果在这之前,没有处理var赋值的逗号表达式,则无法使用该方法!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            let allPrevSiblings = path.getAllPrevSiblings();//获取所有的前兄弟节点
            allPrevSiblings.map(p => {
                let p_node = p.node.declarations[0]
                if (p_node.id.name == arrName) { // 数组节点
                    arr = p_node.init.callee.object.value.split('|');
                    p.remove()
                }
                if (p_node.id.name == argName) { // 自增变量节点
                    p.remove()
                }
            })
            // 控制流还原
            let cases = node.body.body[0].cases;//所有的case语句块
            // 创建存放新语句块的body
            let new_body = [];
            // 遍历查找并添加
            arr.map(index => {
                let body_fiag = false; // 如果取到满足case语句块,则会自动改为true
                cases.map(cas => {
                    let consequent_body = cas.consequent
                    if (cas.test.value == index) {
                        if (t.isContinueStatement(consequent_body[consequent_body.length - 1])) consequent_body.pop() // 删除continue语句
                        new_body = new_body.concat(consequent_body) // 数组拼接操作
                        body_fiag = true;
                    }
                })
                if (!body_fiag) throw '--------case语句块未找到--------'
            })
            // 替换原节点
            path.replaceInline(new_body)
        }
    }
})





/*-------------------------------------------------------------------------------------------------*/
// 生成新的js code，并保存到文件中输出
let output_code = generator(ast, {
    comments: false, // false为删除所有注释
    retainLines: false, // 是否保留多余空行: true为保留  false为不保留
    // compact: true, // 压缩代码
}).code;
fs.writeFile(writePath, output_code, (err) => { });