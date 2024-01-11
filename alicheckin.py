import requests
import json
import os

# 常量定义
UPDATE_ACCESS_TOKEN_URL = "https://auth.aliyundrive.com/v2/account/token"
SIGN_IN_URL = "https://member.aliyundrive.com/v1/activity/sign_in_list"
REWARD_URL = "https://member.aliyundrive.com/v1/activity/sign_in_reward"
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")

HEADERS = {"Content-Type": "application/json"}

def get_access_token():
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
        _print_and_notify_success(count, reward)
    else:
        _handle_sign_in_failure(data)

def _get_sign_in_reward(access_token, count):
    """获取签到奖励"""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"
    
    response = requests.post(REWARD_URL, params={'_rx-s': 'mobile'}, headers=headers, json={'signInDay': count})
    data = response.json()
    return '无奖励' if not data['result'] else data["result"]["notice"]

def _print_and_notify_success(count, reward):
    """打印签到成功信息并通知"""
    message = f"签到成功,本月已签到{count}天, {reward}"
    print(message)
    _notify(message)

def _handle_sign_in_failure(data):
    """处理签到失败情况"""
    message = data.get("message", "未知原因")
    print(message)
    _notify(f"签到失败: {message}")

def _notify(content):
    """使用PushPlus进行通知"""
    if PUSHPLUS_TOKEN:
        url = f"http://www.pushplus.plus/send?token={PUSHPLUS_TOKEN}&title=阿里云盘签到&content={content}"
        requests.get(url)
    else:
        print('推送失败: 未配置PUSHPLUS_TOKEN')

if __name__ == "__main__":
    access_token, _ = get_access_token()
    sign_in(access_token)
