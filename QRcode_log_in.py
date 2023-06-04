from time import sleep
import webbrowser
import requests
import json
import pip
import os

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.0.0"
}

while 1 :
    try :
        import qrcode as qr
        break
    except:
        pip.main( [ "install" , "qrcode" ] )

def log_in() :
    log_get = requests.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate").json()

    url = log_get["data"]["url"]
    qrcode_key = log_get["data"]["qrcode_key"]
    code = 1
    qrcode = qr.make( url )
    with open('qrcode.png', 'wb') as file :
        qrcode.save( file )
    webbrowser.open_new_tab( f"file:///{os.path.abspath( 'qrcode.png' )}" )

    while code != 0 :
        log_in = requests.get(f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}")
        code = log_in.json()["data"]["code"]
        sleep(10)
    print( log_in.json()["data"] )
    cookies = log_in.cookies
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)
    with open( "cookie.json" , "w" ) as f:
        f.write( json.dumps( cookies_dict ) )

def read_cookies( path = ".\\cookie.json" ) :
    while 1 :
        try :
            cookies = requests.cookies.RequestsCookieJar()
            with open( path , "r" ) as f :
                key = json.load( f )
                for i in range( len( key ) ) :
                    cookies.set( list( key.keys() ) [ i ] , list( key.values() ) [ i ] )
            break
        except FileNotFoundError :
            log_in()
    return cookies

def get( url , params = None , headers = header , path = ".\\cookie.json" ) :
    return requests.get( url , params , headers = headers , cookies = read_cookies( path ) )

class progress_bars :
    def __init__( self , max_value : int ) -> None :
        self.max_value = max_value
        self.long = 50
        self.finish = "█"
        self.none = "░" 

    def show( self , value : int ) -> None :
        long = self.long
        max_value = self.max_value
        if max_value // long < 1 :
            long = max_value
        piece = max_value // long
        finish = value // piece
        if finish < long :
            none = long - finish
        else :
            finish = long
            none = 0
        finish = int(finish)
        none = int(none)
        print( f"\r|{ finish * self.finish }{ none * self.none }|{max_value}/{value}" , end = "" )

def progress_bar( value : int , max_value : int ) :
    long = 50
    if max_value // long < 1 :
        long = max_value
    piece = max_value // long
    finish = value // piece
    if finish < long :
        none = long - finish
    else :
        finish = long
        none = 0
    print( f"\r|{finish * '█'}{none * '░' }|{max_value}/{value}" , end = "" )
