const fs = require('fs');
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;

// 读取文件
readPath = 'js_part1.js'
writePath = 'part1_encode.js'
let input_code = fs.readFileSync(readPath, { encoding: "utf-8" });

// 转换为ast树
let ast = parser.parse(input_code);

/*-----------------------------------------------------------------------------------------------------------------------------------------------------------*/

// 删除多余空行
traverse(ast, {
    EmptyStatement(path) {
        path.remove()
    }
})
console.log('finish--> 删除多余空行');

// 16进制还原
traverse(ast, {
    "StringLiteral|NumericLiteral"(path) {
        if (path.node.extra) delete path.node.extra;
    }
})
console.log('finish--> 字符串/常量还原');

// 规范语句,给语句加{}
traverse(ast, {
    // if语句
    IfStatement: {
        exit(path) {
            let { test, consequent, alternate } = path.node;
            if (!t.isBlockStatement(consequent)) {
                path.node.consequent = t.BlockStatement([consequent])
            }
            if (alternate !== null && !t.isBlockStatement(alternate)) {
                path.node.alternate = t.BlockStatement([alternate])
            }
        }
    },
    // for 和 while
    "ForStatement|WhileStatement": {
        exit(path) {
            let { body } = path.node;
            if (!t.isBlockStatement(body)) {
                path.node.body = t.BlockStatement([body])
            }
        }
    },
})
console.log('finish--> 规范语句,给语句加{}');

// 逗号表达式还原
traverse(ast, {
    // var 赋值语句的逗号表达式情况
    VariableDeclaration: {
        exit(path) {
            let { node } = path;
            // 排除var只有一个初始化的节点情况
            if (node.declarations.length == 1) return;
            // 排除for循环中的逗号表达式情况
            if (path.parentPath.isForStatement()) return;
            // 获取节点在容器冲的索引
            let index = path.key
            // 获取容器名字
            let container = path.listKey
            // 节点替换操作start
            let new_array = [];  // 创建用来存放node节点的数组
            // 取出原本在列表中的node节点(splice会默认删除取出的内容)
            let new_var = node.declarations.splice(1)
            new_var.map(v => {
                // 创建节点
                let create_node = t.VariableDeclaration('var', [v])
                // 将节点添加到数组中去
                new_array.push(create_node)
            })
            // 将取出来的节点添加到指定位置
            new_array.reverse().map(q => {
                path.parent[container].splice(index + 1, 0, q)
            })
        }
    },
    // return语句逗号还原
    ReturnStatement: {
        exit(path) {
            let { node } = path;
            if (node.argument.expressions instanceof Array && node.argument.expressions.length > 1) {
                // 获取节点在容器冲的索引
                let index = path.key
                // 获取容器名字
                let container = path.listKey
                // 保留数组中的最后一个值
                let return_body = node.argument.expressions

                // 如果return中含有自执行函数,则不便利此次逗号表达式(情况可能有很多种,需要维护!!!!!!!!!!!!!!!!!!!!!!!!!)
                let flag;
                return_body.map(v => {
                    if (v.type == 'CallExpression' && v.callee && v.callee.type == 'FunctionExpression' && v.arguments) {
                        // console.log(generator(v).code)
                        flag = true;
                    }
                })
                if (flag) return;

                // 替换操作
                let new_return = return_body.splice(0, return_body.length - 1)
                new_return.reverse().map(v => {
                    // 特殊(不全)的自执行函数需要特殊处理
                    if (v.type == 'CallExpression' && v.callee && v.callee.type == 'FunctionExpression' && v.arguments) {
                        v = t.ExpressionStatement(v) // 给自执行函数头尾添加()
                        path.parent[container].splice(index + 1, 0, v);
                        return;
                    }
                    path.parent[container].splice(index + 1, 0, v);
                })
                // 构造最后一个return语句,并添加到父级容器中
                let last_node = t.ReturnStatement(return_body[0])
                path.parent[container].push(last_node)
                // 删除原来的整个return节点
                path.remove()
            }
        }
    },
    // 序列表达式
    ExpressionStatement: {
        exit(path) {
            let { node } = path;
            if (node.expression.expressions instanceof Array && node.expression.expressions.length > 1) {
                // 获取节点在容器中的索引
                let index = path.key
                // 获取容器名字
                let container = path.listKey
                // 替换操作
                node.expression.expressions.reverse().map(v => {
                    path.parent[container].splice(index + 1, 0, v);
                })
                // 直接path.remove()删除原节点
                path.remove();
            }
        }
    },
})
console.log('finish--> 逗号表达式还原');


// 加载解密函数
let bigArray_name, bigArray_index, index = 0;
let arrayMove_index;
let decrypt_func, decrypt_index, flag = false;
ast.program.body.map(v => {
    // 数组移位操作
    if (v.type === 'VariableDeclaration' && v.declarations[0].init && v.declarations[0].init.elements && v.declarations[0].init.elements.length > 500) {
        bigArray_name = v.declarations[0].id.name;
        bigArray_index = index;
    }
    if (index + 1 == ast.program.body.length && bigArray_name == undefined) throw '---------大数组获取失败---------';
    // 根据数组名字,匹配出数组位移的函数
    if (v.type == 'ExpressionStatement' && bigArray_name != undefined && v.expression && v.expression.arguments && v.expression.arguments[0].name === bigArray_name) {
        arrayMove_index = index;
    }
    if (index + 1 == ast.program.body.length && arrayMove_index == undefined) throw '---------数组位移函数获取失败---------';
    // 解密函数
    if (bigArray_index != undefined && arrayMove_index != undefined && arrayMove_index + 1 == index && !flag) {
        try {
            decrypt_func = v.declarations[0].id.name;
            decrypt_index = index;
            flag = true; // 解密函数标志
        } catch { console.log('---------解密函数名获取失败---------'); }
    }
    index += 1;
})

let newAst = parser.parse('');
newAst.program.body.push(ast.program.body[bigArray_index]) // 大数组
newAst.program.body.push(ast.program.body[arrayMove_index]) // 数组位移
newAst.program.body.push(ast.program.body[arrayMove_index + 1]) // 解密函数(采用+1的方式可能会有问题)
let eval_js = generator(newAst, { compact: true }).code; // 将3部分转换成js代码
eval(eval_js) // 执行加载到node内存

// 解密函数还原
traverse(ast, {
    VariableDeclaration(path) {
        let { scope, node } = path
        if (!(node.declarations[0].id.name == decrypt_func)) return;
        // 当变量名与解密函数名相同的时候,就执行相应的操作
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

// 删除解密函数3部分
ast.program.body.splice(bigArray_index, 1);
ast.program.body.splice(arrayMove_index - 1, 1);
ast.program.body.splice(decrypt_index - 2, 1);
console.log('finish--> 解密函数解密完成');
// console.log('-----本地文件替换成功-----', 'https://match.yuanrenxue.com/static/match/safety/match9/udc.js');


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
            // 删除obj定义
            if (paths_sums == paths.length) {//若绑定的每个路径都已处理 ，则移除当前路径
                path.remove();//删除路径
            }
        }
    },
});
console.log('finish--> 花指令剔除');

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
console.log('finish--> 控制流还原');

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
console.log('finish--> 冗余代码删除(if)');





/*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/
// 生成新的js code，并保存到文件中输出
let output_code = generator(ast, {
    comments: false, // false为删除所有注释
    retainLines: false, // 是否保留多余空行: true为保留  false为不保留
    // compact: true, // 压缩代码
}).code;
fs.writeFile(writePath, output_code, (err) => { });