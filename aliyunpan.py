import requests
from message_send import MessageSend
from config import message_tokens, ali_refresh_token
# 常量定义
UPDATE_ACCESS_TOKEN_URL = "https://auth.aliyundrive.com/v2/account/token"
SIGN_IN_URL = "https://member.aliyundrive.com/v1/activity/sign_in_list"
REWARD_URL = "https://member.aliyundrive.com/v1/activity/sign_in_reward"
HEADERS = {"Content-Type": "application/json"}

def get_access_token(REFRESH_TOKEN):
    """获取访问令牌"""
    body = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post(UPDATE_ACCESS_TOKEN_URL, json=body)
    data = response.json()
    return data.get("access_token"), data.get("refresh_token")

def sign_in(access_token):
    """执行签到流程"""
    headers = HEADERS.copy()  # 避免修改全局头部
    headers["Authorization"] = f"Bearer {access_token}"
    
    # 执行签到
    response = requests.post(SIGN_IN_URL, params={'_rx-s': 'mobile'}, headers=headers, json={'isReward': False})
    data = response.json()
    
    if data.get("success"):
        count = data.get("result", {}).get("signInCount", 0)
        reward = _get_sign_in_reward(access_token, count)
        print(f"阿里网盘签到成功,本月已签到{count}天, {reward}")
        return f"阿里网盘签到成功,本月已签到{count}天, {reward}"
    else:
        print(data.get("message", "阿里网盘签到未知原因失败"))
        return data.get("message", "阿里网盘签到未知原因失败")
    

def _get_sign_in_reward(access_token, count):
    """获取签到奖励"""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"
    
    response = requests.post(REWARD_URL, params={'_rx-s': 'mobile'}, headers=headers, json={'signInDay': count})
    data = response.json()
    return '无奖励' if not data['result'] else data["result"]["notice"]


if __name__ == "__main__":
    if ali_refresh_token != None :
        access_token, _ = get_access_token(ali_refresh_token)
        ali_content=sign_in(access_token)
        send = MessageSend()
        send.send_all(message_tokens,'阿里云盘签到', ali_content)
