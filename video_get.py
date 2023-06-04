from QRcode_log_in import *

# bvid = ""
# file_name = ""

bvid = input( "bvid>" )
file_name = input( "file_name>" )
try :
    while 1 :
        chunk_size = int( input("chunk_size(KiB)>") )
        break
except ValueError :
    pass

cid_get = requests.get( "https://api.bilibili.com/x/player/pagelist" , params = {"bvid":bvid} ).json()
cid = cid_get["data"][0]["cid"]
params = {
    "bvid" : bvid ,
    "cid": cid
}
header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.0.0" ,
    "referer" : "https://www.bilibili.com/video/" + bvid
}

video = get( "https://api.bilibili.com/x/player/playurl" , params = params ).json()

the_file = requests.get( video["data"]["durl"][0]["url"] , headers = header )
size = 0
content_size = int( the_file.headers["content-length"] )
with open( file_name , "wb+" ) as file :
    for data in the_file.iter_content(chunk_size=chunk_size) :
        file.write(data)
        size += len(data)
        progress_bars(content_size).show(size)
