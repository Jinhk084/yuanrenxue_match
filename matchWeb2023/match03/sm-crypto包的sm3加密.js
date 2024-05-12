/*
* npm install sm-crypto
* sm-crypto 包的代码,抠出来了
* */


// 消息扩展
const W = new Uint32Array(68)
const M = new Uint32Array(64) // W'

/**
 * 循环左移
 */
function rotl(x, n) {
    const s = n & 31
    return (x << s) | (x >>> (32 - s))
}

/**
 * 二进制异或运算
 */
function xor(x, y) {
    const result = []
    for (let i = x.length - 1; i >= 0; i--) result[i] = (x[i] ^ y[i]) & 0xff
    return result
}

/**
 * 压缩函数中的置换函数 P0(X) = X xor (X <<< 9) xor (X <<< 17)
 */
function P0(X) {
    return (X ^ rotl(X, 9)) ^ rotl(X, 17)
}

/**
 * 消息扩展中的置换函数 P1(X) = X xor (X <<< 15) xor (X <<< 23)
 */
function P1(X) {
    return (X ^ rotl(X, 15)) ^ rotl(X, 23)
}

/**
 * sm3 本体
 */
function sm3(array) {
    let len = array.length * 8

    // k 是满足 len + 1 + k = 448mod512 的最小的非负整数
    let k = len % 512
    // 如果 448 <= (512 % len) < 512，需要多补充 (len % 448) 比特'0'以满足总比特长度为512的倍数
    k = k >= 448 ? 512 - (k % 448) - 1 : 448 - k - 1

    // 填充
    const kArr = new Array((k - 7) / 8)
    const lenArr = new Array(8)
    for (let i = 0, len = kArr.length; i < len; i++) kArr[i] = 0
    for (let i = 0, len = lenArr.length; i < len; i++) lenArr[i] = 0
    len = len.toString(2)
    for (let i = 7; i >= 0; i--) {
        if (len.length > 8) {
            const start = len.length - 8
            lenArr[i] = parseInt(len.substr(start), 2)
            len = len.substr(0, start)
        } else if (len.length > 0) {
            lenArr[i] = parseInt(len, 2)
            len = ''
        }
    }
    const m = new Uint8Array([...array, 0x80, ...kArr, ...lenArr])
    const dataView = new DataView(m.buffer, 0)

    // 迭代压缩
    const n = m.length / 64
    const V = new Uint32Array([0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]) // 字节码
    for (let i = 0; i < n; i++) {
        W.fill(0)
        M.fill(0)

        // 将消息分组B划分为 16 个字 W0， W1，……，W15
        const start = 16 * i
        for (let j = 0; j < 16; j++) {
            W[j] = dataView.getUint32((start + j) * 4, false)
        }

        // W16 ～ W67：W[j] <- P1(W[j−16] xor W[j−9] xor (W[j−3] <<< 15)) xor (W[j−13] <<< 7) xor W[j−6]
        for (let j = 16; j < 68; j++) {
            W[j] = (P1((W[j - 16] ^ W[j - 9]) ^ rotl(W[j - 3], 15)) ^ rotl(W[j - 13], 7)) ^ W[j - 6]
        }

        // W′0 ～ W′63：W′[j] = W[j] xor W[j+4]
        for (let j = 0; j < 64; j++) {
            M[j] = W[j] ^ W[j + 4]
        }

        // 压缩
        const T1 = 0x79cc4519
        const T2 = 0x7a879d8a
        // 字寄存器
        let A = V[0]
        let B = V[1]
        let C = V[2]
        let D = V[3]
        let E = V[4]
        let F = V[5]
        let G = V[6]
        let H = V[7]
        // 中间变量
        let SS1
        let SS2
        let TT1
        let TT2
        let T
        for (let j = 0; j < 64; j++) {
            T = j >= 0 && j <= 15 ? T1 : T2
            SS1 = rotl(rotl(A, 12) + E + rotl(T, j), 7)
            SS2 = SS1 ^ rotl(A, 12)

            TT1 = (j >= 0 && j <= 15 ? ((A ^ B) ^ C) : (((A & B) | (A & C)) | (B & C))) + D + SS2 + M[j]
            TT2 = (j >= 0 && j <= 15 ? ((E ^ F) ^ G) : ((E & F) | ((~E) & G))) + H + SS1 + W[j]

            D = C
            C = rotl(B, 9)
            B = A
            A = TT1
            H = G
            G = rotl(F, 19)
            F = E
            E = P0(TT2)
        }

        V[0] ^= A
        V[1] ^= B
        V[2] ^= C
        V[3] ^= D
        V[4] ^= E
        V[5] ^= F
        V[6] ^= G
        V[7] ^= H
    }

    // 转回 uint8
    const result = []
    for (let i = 0, len = V.length; i < len; i++) {
        const word = V[i]
        result.push((word & 0xff000000) >>> 24, (word & 0xff0000) >>> 16, (word & 0xff00) >>> 8, word & 0xff)
    }

    return result
}

/**
 * hmac 实现
 */
const blockLen = 64
const iPad = new Uint8Array(blockLen)
const oPad = new Uint8Array(blockLen)
for (let i = 0; i < blockLen; i++) {
    iPad[i] = 0x36
    oPad[i] = 0x5c
}

function hmac(input, key) {
    // 密钥填充
    if (key.length > blockLen) key = sm3(key)
    while (key.length < blockLen) key.push(0)

    const iPadKey = xor(key, iPad)
    const oPadKey = xor(key, oPad)

    const hash = sm3([...iPadKey, ...input])
    return sm3([...oPadKey, ...hash])
}




/**
 * 补全16进制字符串
 */
function leftPad(input, num) {
    if (input.length >= num) return input

    return (new Array(num - input.length + 1)).join('0') + input
}

/**
 * 字节数组转 16 进制串
 */
function ArrayToHex(arr) {
    return arr.map(item => {
        item = item.toString(16)
        return item.length === 1 ? '0' + item : item
    }).join('')
}

/**
 * 转成字节数组
 */
function hexToArray(hexStr) {
    const words = []
    let hexStrLength = hexStr.length

    if (hexStrLength % 2 !== 0) {
        hexStr = leftPad(hexStr, hexStrLength + 1)
    }

    hexStrLength = hexStr.length

    for (let i = 0; i < hexStrLength; i += 2) {
        words.push(parseInt(hexStr.substr(i, 2), 16))
    }
    return words
}

/**
 * utf8 串转字节数组
 */
function utf8ToArray(str) {
    const arr = []

    for (let i = 0, len = str.length; i < len; i++) {
        const point = str.codePointAt(i)

        if (point <= 0x007f) {
            // 单字节，标量值：00000000 00000000 0zzzzzzz
            arr.push(point)
        } else if (point <= 0x07ff) {
            // 双字节，标量值：00000000 00000yyy yyzzzzzz
            arr.push(0xc0 | (point >>> 6)) // 110yyyyy（0xc0-0xdf）
            arr.push(0x80 | (point & 0x3f)) // 10zzzzzz（0x80-0xbf）
        } else if (point <= 0xD7FF || (point >= 0xE000 && point <= 0xFFFF)) {
            // 三字节：标量值：00000000 xxxxyyyy yyzzzzzz
            arr.push(0xe0 | (point >>> 12)) // 1110xxxx（0xe0-0xef）
            arr.push(0x80 | ((point >>> 6) & 0x3f)) // 10yyyyyy（0x80-0xbf）
            arr.push(0x80 | (point & 0x3f)) // 10zzzzzz（0x80-0xbf）
        } else if (point >= 0x010000 && point <= 0x10FFFF) {
            // 四字节：标量值：000wwwxx xxxxyyyy yyzzzzzz
            i++
            arr.push((0xf0 | (point >>> 18) & 0x1c)) // 11110www（0xf0-0xf7）
            arr.push((0x80 | ((point >>> 12) & 0x3f))) // 10xxxxxx（0x80-0xbf）
            arr.push((0x80 | ((point >>> 6) & 0x3f))) // 10yyyyyy（0x80-0xbf）
            arr.push((0x80 | (point & 0x3f))) // 10zzzzzz（0x80-0xbf）
        } else {
            // 五、六字节，暂时不支持
            arr.push(point)
            throw new Error('input is not supported')
        }
    }

    return arr
}

function SM3(input, options) {
    input = typeof input === 'string' ? utf8ToArray(input) : Array.prototype.slice.call(input)

    if (options) {
        const mode = options.mode || 'hmac'
        if (mode !== 'hmac') throw new Error('invalid mode')

        let key = options.key
        if (!key) throw new Error('invalid key')

        key = typeof key === 'string' ? hexToArray(key) : Array.prototype.slice.call(key)
        return ArrayToHex(hmac(input, key))
    }

    return ArrayToHex(sm3(input))
}

//
let hashData = SM3('abc');
console.log(hashData);


