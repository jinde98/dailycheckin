import asyncio
import aiohttp
import redis
import datetime
from config import message_tokens, ali_refresh_token, redis_info

# 常量定义
UPDATE_ACCESS_TOKEN_URL = "https://auth.aliyundrive.com/v2/account/token"
SIGN_IN_URL = "https://member.aliyundrive.com/v1/activity/sign_in_list"
REWARD_URL = "https://member.aliyundrive.com/v1/activity/sign_in_reward"
HEADERS = {"Content-Type": "application/json"}

class Ali:
    def __init__(self, ali_refresh_token: str = '', Redis_info: str = '') -> None:
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
            print("格式错误，请提供正确的Redis信息格式。")

    async def get_access_token(self, refresh_token):
        """异步获取访问令牌"""
        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(UPDATE_ACCESS_TOKEN_URL, json=body) as response:
                data = await response.json()
                return data.get("access_token"), data.get("refresh_token")

    async def sign_in(self, access_token):
        """异步执行签到流程"""
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {access_token}"

        async with aiohttp.ClientSession() as session:
            async with session.post(SIGN_IN_URL, params={'_rx-s': 'mobile'}, headers=headers, json={'isReward': False}) as response:
                data = await response.json()

        if data.get("success"):
            count = data.get("result", {}).get("signInCount", 0)
            reward = await self._get_sign_in_reward(access_token, count)
            print(f"阿里网盘签到成功,本月已签到{count}天, {reward}。")
            return f"阿里网盘签到成功,本月已签到{count}天, {reward}。"
        else:
            print(data.get("message", "阿里网盘签到未知原因失败。"))
            return data.get("message", "阿里网盘签到未知原因失败。")

    async def _get_sign_in_reward(self, access_token, count):
        """异步获取签到奖励"""
        timestamp = int(datetime.datetime.now().timestamp())
        print(timestamp)
        headers = {
            'User-Agent': "AliApp(AYSD/5.8.0) com.alicloud.databox/37029260 Channel/36176727979800@rimet_android_5.8.0 language/zh-CN /Android",
            'Content-Type': "application/json",
            # 'x-device-id': "0be6xxxxxxxxxxxxxxxxxxxxxxxxxxx7dac4",
            'x-canary': "client=Android,app=adrive,version=v5.8.0",
            'x-timestamp': f"{timestamp}",
            'x-nonce': "b9fd6ce6-a7ac-4d58-a419-f42a3aa31825",
            # 'x-signature-v2': "568xxxxxxxxxxxxxxxxxxxxx236",
            'authorization': f'Bearer {access_token}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(REWARD_URL, params={'_rx-s': 'mobile'}, headers=headers, json={'signInDay': count}) as response:
                data = await response.json()
                return '无奖励' if not data['result'] else data["result"]["notice"]
            
    async def _run_sync_in_executor(self, func, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func, *args)

    async def store_redis(self, refresh_token: str = None) -> str:
        try:
            if not self.redis_conn:
                print('未配置redis。')
                return '未配置redis。'
            if not refresh_token:
                print('未配置refresh_token。')
                return '未配置refresh_token。'
            redis_key_refresh = f"Ali_refresh_token"
            await self._run_sync_in_executor(self.redis_conn.set, redis_key_refresh, refresh_token)
            print(f"更新{redis_key_refresh}到redis。")
            return f"更新{redis_key_refresh}到redis。"
        except Exception as e:
            print(f"{redis_key_refresh}Store Redis error: {e}")
            return f"更新{redis_key_refresh}到redis失败,{e}。"

    async def get_redis(self) -> str:
        try:
            if self.redis_conn is None:
                print('未配置redis')
                return '未配置redis'
            redis_key_refresh = f"Ali_refresh_token"
            refresh_token = await self._run_sync_in_executor(self.redis_conn.get, redis_key_refresh)
            print("从redis取得阿里网盘token")
            return refresh_token
        except Exception as e:
            print(f"Get Redis error: {e}")
            return f"Get Redis error: {e}"

    async def run(self):
        refresh_token = await self.get_redis()
        if not refresh_token:
            return "未获取到refresh_token"
        access_token, refresh_token = await self.get_access_token(refresh_token)
        ali_content = await self.sign_in(access_token)
        today = datetime.datetime.now().day
        if today == 26 or today == 10:
            ali_content += await self.store_redis(refresh_token=refresh_token)
        return ali_content

if __name__ == "__main__":
    aliyun = Ali(ali_refresh_token=ali_refresh_token, Redis_info=redis_info)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(aliyun.run())
    print(result)