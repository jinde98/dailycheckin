
from message_send import MessageSend
from config import message_tokens, youdao_cookie,ali_refresh_token,ty_pwd,ty_user,youdao_user, redis_info, RedisUtil
import aliyunpan, tianyiyunpan,YouDao_user_login, imaotai

def run():
    content =''
    title = ""
    if youdao_user != None:
        youdao_sign=YouDao_user_login.Youdao(youdao_user, redis_info)
        content= youdao_sign.run() + '\n\n'
        title = "【有道】"
    # if ali_refresh_token != None :
    #     Aliyun=aliyunpan.Ali(ali_refresh_token, redis_info)
    #     content += Aliyun.run() + '\n\n'
    #     title += "【阿里】"
    if ty_user != None and ty_pwd != None:
        content += tianyiyunpan.main(ty_user, ty_pwd)
        title += "【天翼】"
    if redis_info != None:
        datas = RedisUtil(redis_info).get('IMAOTAI') # 获取Redis取得茅台配置数据
        _check_item = datas.get("IMAOTAI", [])[0]
        content+= imaotai.IMAOTAI(check_item=_check_item).main()+'\n\n'
        title += "【茅台】"

    send = MessageSend()
    send.send_all(message_tokens,title+'每日签到',content)
if __name__ == "__main__":
    run()


    


