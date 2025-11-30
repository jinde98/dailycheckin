from message_send import MessageSend
from config import message_tokens, youdao_cookie,ali_refresh_token,ty_pwd,ty_user,youdao_user, redis_info, RedisUtil
import aliyunpan, tianyiyunpan,YouDao_user_login, imaotai

def run():
    content =''
    title = ""
    if youdao_user != None:
        try:
            youdao_sign=YouDao_user_login.Youdao(youdao_user, redis_info)
            content += youdao_sign.run() + '\n\n'
            title += "【有道】"
        except Exception as e:
            content += f"有道签到失败: {e}\n\n"
            title += "【有道-失败】"
            
    # if ali_refresh_token != None :
    #     try:
    #         Aliyun=aliyunpan.Ali(ali_refresh_token, redis_info)
    #         content += Aliyun.run() + '\n\n'
    #         title += "【阿里】"
    #     except Exception as e:
    #         content += f"阿里签到失败: {e}\n\n"
    #         title += "【阿里-失败】"

    if ty_user != None and ty_pwd != None:
        try:
            content += tianyiyunpan.main(ty_user, ty_pwd)+'\n\n'
            title += "【天翼】"
        except Exception as e:
            content += f"天翼签到失败: {e}\n\n"
            title += "【天翼-失败】"

    # if redis_info != None:
    #     try:
    #         datas = RedisUtil(redis_info).get('IMAOTAI') # 获取Redis取得茅台配置数据
    #         _check_item = datas.get("IMAOTAI", [])[0]
    #         content+= imaotai.IMAOTAI(check_item=_check_item).main()
    #         title += "【茅台】"
    #     except Exception as e:
    #         content += f"茅台签到失败: {e}\n\n"
    #         title += "【茅台-失败】"

    send = MessageSend()
    send.send_all(message_tokens,title+'每日签到',content)

if __name__ == "__main__":
    run()
