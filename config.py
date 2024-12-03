from dotenv import load_dotenv
load_dotenv()
import os

ali_refresh_token =  os.environ.get('ALI_REFRESH_TOKEN')
ty_user = os.environ.get('TY_USER')
ty_pwd = os.environ.get('TY_PWD')
youdao_user = os.environ.get('YOUDAO_USER')
redis_info = os.environ.get('REDIS_INFO')
youdao_cookie = os.environ.get('YOUDAO_COOKIE')
amap_key = os.environ.get('AMAP_KEY')

message_tokens = {
    'pushplus_token': os.environ.get('PUSHPLUS_TOKEN') ,
    'serverChan_token': os.environ.get('SERVERCHAN_SENDKEY'),
    'weCom_tokens': os.environ.get('WECOM_TOKENS'),
    'weCom_webhook': os.environ.get('WECOM_WEBHOOK'),
    'bark_deviceKey': os.environ.get('BARK_DEVICEKEY'),
    'feishu_deviceKey': os.environ.get('FEISHU_DEVICEKEY'),
    'telegram_token': os.environ.get('TELEGRAM_TOKEN'),
}

import redis
import json

class RedisUtil:
    def __init__(self, Redis_info:str = '') -> None:
        self.redis_host = None
        self.redis_port = None
        self.redis_passwd = None
        self.redis_conn = None
        try:
            if Redis_info:
                self.redis_host, self.redis_port, self.redis_passwd = Redis_info.replace(" ", "").split(',')
                self.redis_conn = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    password=self.redis_passwd,
                    decode_responses=True
                )
        except Exception as e:
            print(f"连接 Redis 失败: {e}")
            self.redis_conn = None

    def get(self, key: str):
        """通过键从 Redis 获取值。"""
        try:
            if self.redis_conn is None:
                print("Redis 未配置连接。")
                return None
            value = self.redis_conn.get(key)
            if value:
                return json.loads(value)
            else:
                print(f"键 '{key}' 在 Redis 中未找到。")
                return None
        except Exception as e:
            print(f"从 Redis 获取键 '{key}' 时出错: {e}")
            return None

    def set(self, key: str, value: dict) -> str:
        """通过键将值存储到 Redis。"""
        try:
            if self.redis_conn is None:
                print("Redis 未配置连接。")
                return "Redis 未配置连接。"
            if isinstance(value, dict):
                value = json.dumps(value)
            self.redis_conn.set(key, value)
            print(f"键 '{key}' 在 Redis 中更新成功。")
            return f"键 '{key}' 在 Redis 中更新成功。"
        except Exception as e:
            print(f"将键 '{key}' 存储到 Redis 时出错: {e}")
            return f"键 '{key}' 在 Redis 中更新失败。"

if __name__ == '__main__':
    test=RedisUtil(redis_info)
    print(test.get('IMAOTAI'))
    # with open('config.json', 'r', encoding='utf-8') as f:
    #    config_data = json.load(f)
    # test.set('IMAOTAI',config_data)      

