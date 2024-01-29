import requests,redis,json,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from message_send import MessageSend
from config import message_tokens, youdao_user,redis_info 

class Youdao:
    def __init__(self, Youdao_user:str ='', Redis_info:str = '') -> None:
        self.user = None
        self.passwd = None
        self.redis_host = None
        self.redis_port = None
        self.redis_passwd = None
        self.redis_conn = None
        try:
            if Youdao_user:
                self.user, self.passwd = Youdao_user.replace(" ", "").split(',')
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

    def login(self):
        if self.user == None and self.passwd == None:
            print('有道未配置账户。')
            return 
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://note.youdao.com/mobileSignIn/login_mobile.html?&back_url=https://note.youdao.com/web/&from=web')  # 打开网页
        driver.maximize_window()  # 最大化浏览器窗口
        time.sleep(1)  # 等待页面加载
        driver.find_element(By.XPATH, '//*[@id="netease-login"]/div').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="user"]').send_keys(self.user)
        driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys(self.passwd)
        driver.find_element(By.XPATH, '//*[@id="loginbtn"]').click()
        time.sleep(10)
        driver.save_screenshot('screenshot_after_login.png')
        print("截图保存成功")
        #WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "personal-container"))) 
        cookies=driver.get_cookies()
        specific_cookies = {}
        for cookie in cookies:
            if cookie['name'] == 'YNOTE_SESS' or cookie['name'] == 'YNOTE_LOGIN':
                specific_cookies[cookie['name']] = cookie['value']
        print(specific_cookies)
        driver.quit()
        return specific_cookies

    def get_redis(self):
        try:
            if self.redis_conn is None:
                print('未配置redis')
                return None
            redis_key = f"Note163_{self.user}"
            cookie = self.redis_conn.get(redis_key)
            if cookie:
                cookie_json = json.loads(cookie)
                print('从redis取得有道cookie')
                return cookie_json
            else:
                print('redis有道cookie为空')
                return None
        except Exception as e:
            print(f"Get Redis error: {e}")
            return None
       
    def store_redis(self,cookie) -> str:
        try:
            if self.redis_conn is None:
                print('未配置redis。')
                return '未配置redis。'
            if cookie is None:
                print('有道cookie为空，不更新到redis。')
                return '有道cookie为空，不更新到redis。'
            redis_key = f"Note163_{self.user}"
            if isinstance(cookie, dict):
                cookie = json.dumps(cookie)
            self.redis_conn.set(redis_key, cookie)
            print("更新cookie到redis。")
            return "更新cookie到redis。"
        except Exception as e:
            print(f"Store Redis error: {e}")
            return '更新cookie到redis失败。'
    
    def signin(self, cookies) -> str:
        try:
            if cookies is None:
                return "有道cookie为空。"
            ad_space = 0
            url = "https://note.youdao.com/yws/api/daupromotion?method=sync"
            res = requests.post(url=url, cookies=cookies)
            if "error" not in res.text:
                checkin_response = requests.post(
                    url="https://note.youdao.com/yws/mapi/user?method=checkin", cookies=cookies)
                for i in range(3):
                    ad_response = requests.post(
                        url="https://note.youdao.com/yws/mapi/user?method=adRandomPrompt", cookies=cookies)
                    ad_space += ad_response.json().get("space", 0) // 1048576
                if "reward" in res.text:
                    sync_space = res.json().get("rewardSpace", 0) // 1048576
                    checkin_space = checkin_response.json().get("space", 0) // 1048576
                    space = sync_space + checkin_space + ad_space
                    youdao_message = f"有道签到获得{sync_space}m+{checkin_space}m+{ad_space}m={space}m空间。"
                    print(youdao_message)
                else:
                    youdao_message = "有道获取失败。"
                    print(youdao_message)
            else:
                youdao_message = "有道Cookie 可能过期。"
                print(youdao_message)
            return youdao_message
        except Exception as e:
            print(f"Signin error: {e}")
            return '有道签到失败。'

    def run(self) -> str:
        cookie= self.get_redis()
        massage=self.signin(cookie)
        if "有道签到获得" in massage:
            return massage
        cookie= self.login()
        massage= self.signin(cookie)
        massage+= self.store_redis(cookie)
        return massage

if __name__ == "__main__":
    # if youdao_cookie != None:
    youdao=Youdao(youdao_user,redis_info)
    print(youdao.run()) 
    # send= MessageSend()
    # send.send_all(message_tokens,'有道笔记签到',msg)
