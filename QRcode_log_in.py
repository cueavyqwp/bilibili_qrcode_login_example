import webbrowser
import requests
import socket
import json
import pip

while 1 :
    try :
        import qrcode
        break
    except:
        pip.main( [ "install" , "qrcode" ] )

def log_in() :
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

    log_in = requests.get(f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}")
    cookies = log_in.cookies
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)
    with open( "cookie.json" , "w" ) as f:
        f.write( json.dumps( cookies_dict ) )

def read_cookies( path = ".\\cookie.json" ) :
    cookies = requests.cookies.RequestsCookieJar()
    with open( ".\\cookie.json" , "r" ) as f :
        key = json.load( f )
        for i in range( len( key ) ) :
            cookies.set( list( key.keys() ) [ i ] , list( key.values() ) [ i ] )
    return cookies

def get( url , params = None , path = ".\\cookie.json" ) : return requests.get( url , params , cookies = read_cookies( path ) )