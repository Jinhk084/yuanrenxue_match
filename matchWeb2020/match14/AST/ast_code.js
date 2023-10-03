const fs = require('fs');
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const types = require("@babel/types");
const generator = require("@babel/generator").default;

// 读取文件
let input_code = fs.readFileSync('input_code.js', { encoding: "utf-8" });

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


// 解密函数还原: $_0x2b10('\x30\x78\x38\x65', '\x31\x21\x68\x78') --> iZz
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
                referencePath.parentPath.replaceInline(types.valueToNode(value))
            }
        }
    }
})


// 16进制转换成为字符串: '\x4e\x6b\x58\x43\x6d\x51\x3d\x3d' --> "NkXCmQ=="
traverse(ast, {
    StringLiteral(path) {
        let { node } = path
        if (node.extra) {
            delete node.extra
        }
    }
})


// 常量求值:  "con" + "sol" + "e" --> "console"
traverse(ast, {
    "BinaryExpression"(path) {
        const { confident, value } = path.evaluate();
        // 过滤
        if (value == "Infinity" || !confident) return;
        path.replaceInline(types.valueToNode(value));
    }
})






/*-------------------------------------------------------------------------------------------------*/
// 生成新的js code，并保存到文件中输出
let output_code = generator(ast, {
    comments: false, // false为删除所有注释
    retainLines: false, // 是否保留多余空行: true为保留  false为不保留
    // compact: true, // 压缩代码
}).code;
fs.writeFile('output_code.js', output_code, (err) => { });