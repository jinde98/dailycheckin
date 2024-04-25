import requests, redis, datetime
from message_send import MessageSend
from config import message_tokens, ali_refresh_token
# 常量定义
UPDATE_ACCESS_TOKEN_URL = "https://auth.aliyundrive.com/v2/account/token"
SIGN_IN_URL = "https://member.aliyundrive.com/v1/activity/sign_in_list"
REWARD_URL = "https://member.aliyundrive.com/v1/activity/sign_in_reward"
HEADERS = {"Content-Type": "application/json"}
class Ali:
    def __init__(self, ali_refresh_token:str ='', Redis_info:str = '') -> None:
        self.redis_host = None
        self.redis_port = None
        self.redis_passwd = None
        self.redis_conn = None
        self.refresh_token = ali_refresh_token
        try:
            if Redis_info:
                self.redis_host, self.redis_port, self.redis_passwd = Redis_info.replace(" ", "").split(',')
                self.redis_conn = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    password=self.redis_passwd,
                    decode_responses=True
                )
        except ValueError:
            print("格式错误，请提供正确的有道用户和Redis信息格式。")
    def get_access_token(self, refresh_token):
        """获取访问令牌"""
        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        response = requests.post(UPDATE_ACCESS_TOKEN_URL, json=body)
        data = response.json()
        return data.get("access_token"), data.get("refresh_token")

    def sign_in(self, access_token)->str:
        """执行签到流程"""
        headers = HEADERS.copy()  # 避免修改全局头部
        headers["Authorization"] = f"Bearer {access_token}"
        
        # 执行签到
        response = requests.post(SIGN_IN_URL, params={'_rx-s': 'mobile'}, headers=headers, json={'isReward': False})
        data = response.json()
        
        if data.get("success"):
            count = data.get("result", {}).get("signInCount", 0)
            reward = self._get_sign_in_reward(access_token, count)
            print(f"阿里网盘签到成功,本月已签到{count}天, {reward}")
            return f"阿里网盘签到成功,本月已签到{count}天, {reward}"
        else:
            print(data.get("message", "阿里网盘签到未知原因失败"))
            return data.get("message", "阿里网盘签到未知原因失败")
        
    def _get_sign_in_reward(self, access_token, count):
        """获取签到奖励"""
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        
        response = requests.post(REWARD_URL, params={'_rx-s': 'mobile'}, headers=headers, json={'signInDay': count})
        data = response.json()
        return '无奖励' if not data['result'] else data["result"]["notice"]

    def store_redis(self, access_token:str = None, refresh_token:str = None) -> str:
        try:
            if not self.redis_conn:
                print('未配置redis。')
                return '未配置redis。'
            if not refresh_token:
                print('未配置refresh_token。')
                return '未配置refresh_token。'
            if refresh_token:
                redis_key_refresh = f"Ali_refresh_token"
                self.redis_conn.set(redis_key_refresh, refresh_token)
            print(f"更新{redis_key_refresh}到redis。")
            return f"更新{redis_key_refresh}到redis。"
        except Exception as e:
            print(f"{redis_key_refresh}Store Redis error: {e}")
            return f"更新{redis_key_refresh}到redis失败,{e}。"
    def get_redis(self) -> str:
        try:
            if self.redis_conn is None:
                print('未配置redis')
                return '未配置redis'
            redis_key_refresh = f"Ali_refresh_token"
            refresh_token = self.redis_conn.get(redis_key_refresh)
            print("从redis取得阿里网盘token")
            return refresh_token
        except Exception as e:
            print(f"Get Redis error: {e}")
            return f"Get Redis error: {e}"
        
    def run(self):
        refresh_token =self.get_redis()
        access_token, refresh_token =self.get_access_token(refresh_token)
        ali_content = self.sign_in(access_token)
        today = datetime.datetime.now().day
        if today == '26' or today== '10':
            ali_content += self.store_redis(refresh_token = refresh_token)
        return ali_content
            
if __name__ == "__main__":
    Aliyun=aliyunpan.Ali(ali_refresh_token, redis_info)
    Aliyun.run()
