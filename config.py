import os

ali_refresh_token =  os.environ.get('ALI_REFRESH_TOKEN')
ty_user = os.environ.get('TY_USER')
ty_pwd = os.environ.get('TY_PWD')
youdao_user = os.environ.get('YOUDAO_USER')
redis_info = os.environ.get('REDIS_INFO')
youdao_cookie = os.environ.get('YOUDAO_COOKIE')


pushplus_token = os.environ.get('PUSHPLUS_TOKEN') 
serverChan_sendkey = os.environ.get('SERVERCHAN_SENDKEY')
weCom_tokens = os.environ.get('WECOM_TOKENS')
weCom_webhook = os.environ.get('WECOM_WEBHOOK')
bark_deviceKey = os.environ.get('BARK_DEVICEKEY')
feishu_deviceKey = os.environ.get('FEISHU_DEVICEKEY')
telegram_token = os.environ.get('TELEGRAM_TOKEN')

message_tokens = {
    'pushplus_token': pushplus_token,
    'serverChan_token': serverChan_sendkey,
    'weCom_tokens': weCom_tokens,
    'weCom_webhook': weCom_webhook,
    'bark_deviceKey': bark_deviceKey,
    'feishu_deviceKey': feishu_deviceKey,
    'telegram_token': telegram_token,
}
