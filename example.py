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