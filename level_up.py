from QRcode_log_in import *

get_info = get( "https://api.bilibili.com/x/web-interface/nav" )
data = get_info.json()["data"]
level = data[ "level_info" ][ "current_level" ]
coin = data[ "money" ]
exp = data[ "level_info" ][ "current_exp" ]
senior_member = data[ "is_senior_member" ]
max_exp = 28800 # lv6

if level == 6 :
    print("已经满级了ヾ(≧▽≦*)o")
    if not senior_member :
        print("还没通过硬核会员\n快去尝试吧\^o^/\nhttps://www.bilibili.com/h5/senior-newbie")
else :
    need_day = 0
    exp_old = exp
    coin_old = coin
    while max_exp > exp :
        need_day += 1
        exp += 15 # 登录+看视频+分享
        coin += 1
        if coin >= 5 :
            # coin -= 5
            exp += 50
        elif coin >= 1 :
            have_coin = int(coin)
            # coin -= have_coin
            exp += have_coin * 10
    print( f"当前等级 { level }\n当前经验 { exp_old }\n当前硬币 { coin_old }\n还需经验 { max_exp - exp_old }\n还需天数 { need_day }" )
