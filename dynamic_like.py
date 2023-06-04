from QRcode_log_in import *

def get( dynamic_id : str , func = None , sleep_time : float = 1.0 , show_code : bool = False ) -> list :
    ret = []
    i = 0
    has_more = 1
    while has_more :
        i += 1
        params = {
            "dynamic_id" : dynamic_id ,
            "pn" : str(i)
        }
        code = 1
        chance = 5
        while code != 0 :
            data = requests.get( "https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/spec_item_likes" , params = params ).json()
            code = data["code"]
            message = data["message"]
            if code != 0 :
                if show_code :
                    print(f"code {code}")
                    print(message)
                chance -= 1
                if chance <= 0 :
                    break
        if chance <= 0 :
            break
        data = data["data"]
        has_more = data["has_more"]
        item_likes = data["item_likes"]
        total_count = data["total_count"]
        page_num = total_count//20
        if total_count%20 :
            page_num += 1
        if func :
            func( item_likes , i , page_num )
        ret += item_likes
        sleep(sleep_time)
    return ret

def main() :
    while 1 :
        dynamic_id = input("dynamic_id>")
        try :
            int(dynamic_id)
            break
        except :
            pass
    #=======================================================================
    def func( items : list , page : int , total_page : int ) :
        print(f"page {page}")
        for i in items :
            uid = i["uid"]
            name = i["uname"]
            print(name,uid)

    def progress_bar( items : list , page : int , total_page : int ) :
        progress_bars(total_page).show(page)
    #=======================================================================
    info = []
    for i in get(dynamic_id,progress_bar,show_code=1) :
        uid = i["uid"]
        name = i["uname"]
        info.append({
            "uid" : uid ,
            "name" : name
        })

    if len(info) :
        with open( f"{dynamic_id}.json" , "w+" , encoding = "utf-8" ) as file :
            file.write( json.dumps( info , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False ) )

if __name__ == "__main__" :
    main()
