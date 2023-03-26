# 哔哩哔哩二维码登入

用python简单实现了B站二维码登入

API文档由 [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 提供

# 流程

参考章目 [二维码登录](https://socialsisteryi.github.io/bilibili-API-collect/docs/login/login_action/QR.html)

## 获取密钥

>https://passport.bilibili.com/x/passport-login/web/qrcode/generate

使用 `requests.get()` 来请求

## 示例返回

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "url": "https://passport.bilibili.com/h5-app/passport/login/scan?navhide=1\u0026qrcode_key=\u0026from=",
        "qrcode_key": ""
    }
}
```

### data字典

| 字段 | 类型 | 内容 |
|:---:|:---:|:---:|
| `url` | `str` | 待会要生成为二维码的链接
| `qrcode_key` | `str` | 扫码登录秘钥

## 生成二维码

使用 `qrcode` 模块

使用`pip`来安装 `pip install qrcode` 或 `pip3 install qrcode`

简单示例

```python
import qrcode
img=qrcode.make("www.bilibili.com")
img.save('log_in.png')
```

在当前目录找到`log_in.png`并扫码就可以打开B站网页端了

## 打开浏览器

使用 `webbrowser` 模块

简单示例

- QRcode_log_in.py
- QR.html

### QRcode_log_in.py
```python
import webbrowser
import requests
import socket
import json

log_get = requests.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate").json()

url = log_get["data"]["url"]
qrcode_key = log_get["data"]["qrcode_key"]
img=qrcode.make(url)
img.save('log_in.png')
webbrowser.open('QR.html')
```

### QR.html
```html
<!DOCTYPE html>
<html lang="zh-cn">

<head>
    <meta charset="UTF-8">
    <title>QR</title>
    <script>
        function OK(){
            new WebSocket("ws://localhost:22332");

            var div = document.getElementById("QRCode");
            div.parentNode.removeChild(div);

            var OK = document.getElementById("OK");
            OK.style.display = "block";

        }
    </script>
</head>

<body>
    <div id = "QRCode" >
        <p style = "text-align: center;" >
            <img src="log_in.png" alt="QRCode">
        </p>
        <p align='center' >
            <button type = "button" onclick= "OK()" >确定</button>
        </p>
    </div>
    <div id = "OK" style = "display:none;text-align: center;" >
        <h1>已完成</h1>
        <p>现在可以退出了</p>
    </div>
</body>

</html>
```

运行后打开了`QR.html`

并且显示了一个二维码

## 确定扫描成功

查看`QR.html`可以知道

我这里是使用 在本地开启一个服务器 来确定是否成功扫描二维码的

当然 也可以使用其它方法

### QRcode_log_in.py
```python
import webbrowser
import requests
import socket
import json

log_get = requests.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate").json()

url = log_get["data"]["url"]
qrcode_key = log_get["data"]["qrcode_key"]
img=qrcode.make(url)
img.save('log_in.png')
webbrowser.open('QR.html')

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(("", 22332))
tcp_server_socket.listen(1)
user = tcp_server_socket.accept()[0]
user.recv(1024)
```

## 获取cookie

```python
log_in = requests.get(f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}")
```

`qrcode_key`即当时获取的 扫码登录秘钥

## 其它

然后就是保存`cookie`还有示例代码等

具体参照源代码

## 示例代码
```python
from QRcode_log_in import *

get_info = get( "https://api.bilibili.com/x/web-interface/nav" )

i = get_info.json()["data"]

print(
f"""{ "===" * 60 }
昵称 { i[ "uname" ] }
mid { i[ "mid" ] }
等级 { i[ "level_info" ][ "current_level" ] }
经验 { i[ "level_info" ][ "current_exp" ] }
头像 { i[ "face" ] }
硬币 { i[ "money" ] }
B币 { i[ "wallet" ][ "bcoin_balance" ] }
{ "===" * 60 }"""
)

get_stat = get( "https://api.bilibili.com/x/web-interface/nav/stat" )

s = get_stat.json()["data"]

print(
f"""关注数 { s[ "following" ] }
订阅数 { s[ "follower" ] }
动态数 { s[ "dynamic_count" ] }
{ "===" * 60 }"""
)
```

获取了一些基本信息