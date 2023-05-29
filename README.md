# 哔哩哔哩二维码登入

用python简单实现了B站二维码登入

> 并写了几个示例

API文档由 [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 提供

# 流程

>参考章目 [二维码登录](https://socialsisteryi.github.io/bilibili-API-collect/docs/login/login_action/QR.html)

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
img = qrcode.make("www.bilibili.com")
img.save('log_in.png')
```

在当前目录找到`log_in.png`并扫码就可以打开B站网页端了

## 打开图片

使用 `webbrowser` 模块

```python
import webbrowser
import os
webbrowser.open_new_tab( f"file:///{os.path.abspath( 'qrcode.png' )}" )
```

## 确定扫描成功

使用`while`和`sleep`确定扫码成功

```python
code = 1
while code != 0 :
    log_in = requests.get(f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}")
    code = log_in.json()["data"]["code"]
    sleep(10)
```

## 获取cookie

```python
log_in = requests.get(f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}")
```

`qrcode_key`即当时获取的 扫码登录秘钥
