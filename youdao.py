import requests
from message_send import MessageSend
from config import message_tokens, youdao_cookie 

def signin(cookie):
    headers = {
    "Cookie":cookie,
    "User-Agent":"you dao yun bi ji/7.0.6 (iPhone; iOS 14.3; Scale/2.00)",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept-Encoding":"gzip, deflate, br"
}
    ad_space = 0
    refresh_cookies_res = requests.get("http://note.youdao.com/login/acc/pe/getsess?product=YNOTE", headers=headers)
    cookies = dict(refresh_cookies_res.cookies)

    url = "https://note.youdao.com/yws/api/daupromotion?method=sync"
    res = requests.post(url=url, cookies=cookies)
    if "error" not in res.text:
        checkin_response = requests.post(
            url="https://note.youdao.com/yws/mapi/user?method=checkin", cookies=cookies,)
        for i in range(3):
            ad_response = requests.post(
                url="https://note.youdao.com/yws/mapi/user?method=adRandomPrompt",cookies=cookies,)
            ad_space += ad_response.json().get("space", 0) // 1048576
        if "reward" in res.text:
            sync_space = res.json().get("rewardSpace", 0) // 1048576
            checkin_space = checkin_response.json().get("space", 0) // 1048576
            space = sync_space + checkin_space + ad_space
            youdao_message = f"有道签到获得{sync_space}m+{checkin_space}m+{ad_space}m={space}m空间"
            print(f"有道签到获得{sync_space}m+{checkin_space}m+{ad_space}m={space}M")
        else:
            youdao_message = "有道获取失败"
            print("有道获取失败")
    else:
        youdao_message = "有道Cookie 可能过期"
        print("有道Cookie 可能过期")
    return youdao_message

if __name__ == "__main__":
    if youdao_cookie != None:
        youdao = signin(youdao_cookie)
        send = MessageSend()
        send.send_all(message_tokens,'有道笔记签到',youdao)
