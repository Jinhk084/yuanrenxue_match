
题目:
```
cookie检测加载完成，题目：当时间戳为 1587102734000（单位 ms） 时，cookie中sign对应的值是多少？
主要考察 hook cookie 相关操作
```


清除cookie中的sign值,打全局script断点之后刷新页面hook (Never pause here过掉无限debugger):
```javascript
Object.defineProperty(document, 'cookie', {
    set : function (value){
        if (value.indexOf("sign") !== -1) {
            debugger;
        }
    }
});
```

关键的js代码(js是动态的): 
```javascript
var c = new Date()[_$ob('0x4b')]();
token = window[_$ob('0x4e')](a['WedNs'](a[_$ob('0x12')], a[_$ob('0x4')](String, c)));
md = a[_$ob('0x4')](hex_md5, window[_$ob('0x4e')](a[_$ob('0x32')](a[_$ob('0x12')], a['ySGJp'](String, Math[_$ob('0x6')](a['qlfvf'](c, 0x3e8))))));
document['cookie'] = a[_$ob('0x32')](a[_$ob('0x11')](a[_$ob('0x1f')](a['zjciF'](a[_$ob('0xc')](a[_$ob('0x1b')](a['AOLCK'], Math[_$ob('0x6')](a[_$ob('0x22')](c, 0x3e8))), '~'), token), '|'), md), a[_$ob('0x16')]);
```

仿照上面的动态js代码,修改指定时间戳后执行即可:
```javascript
c = 1587102734000
token = window[_$ob('0x4e')](a['WedNs'](a[_$ob('0x12')], a[_$ob('0x4')](String, c)));
md = a[_$ob('0x4')](hex_md5, window[_$ob('0x4e')](a[_$ob('0x32')](a[_$ob('0x12')], a['ySGJp'](String, Math[_$ob('0x6')](a['qlfvf'](c, 0x3e8))))));
a[_$ob('0x32')](a[_$ob('0x11')](a[_$ob('0x1f')](a['zjciF'](a[_$ob('0xc')](a[_$ob('0x1b')](a['AOLCK'], Math[_$ob('0x6')](a[_$ob('0x22')](c, 0x3e8))), '~'), token), '|'), md), a[_$ob('0x16')]);
```
