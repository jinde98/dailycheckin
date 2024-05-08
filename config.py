from dotenv import load_dotenv
load_dotenv()
import os

ali_refresh_token =  os.environ.get('ALI_REFRESH_TOKEN')
ty_user = os.environ.get('TY_USER')
ty_pwd = os.environ.get('TY_PWD')
youdao_user = os.environ.get('YOUDAO_USER')
redis_info = os.environ.get('REDIS_INFO')
youdao_cookie = os.environ.get('YOUDAO_COOKIE')

message_tokens = {
    'pushplus_token': os.environ.get('PUSHPLUS_TOKEN') ,
    'serverChan_token': os.environ.get('SERVERCHAN_SENDKEY'),
    'weCom_tokens': os.environ.get('WECOM_TOKENS'),
    'weCom_webhook': os.environ.get('WECOM_WEBHOOK'),
    'bark_deviceKey': os.environ.get('BARK_DEVICEKEY'),
    'feishu_deviceKey': os.environ.get('FEISHU_DEVICEKEY'),
    'telegram_token': os.environ.get('TELEGRAM_TOKEN'),
}
