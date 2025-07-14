# 每日签到 GitHub Action 部署

## 功能简介

这个 GitHub Action 用于执行各种服务的每日签到任务，这样可以不用服务器来运行，目前支持有道、天翼云盘、茅台申购。
茅台申购自动生成配置文件，需要在本地运行imaotai_login.py。如果有redis，可以把配置文件保存到redis，这样可以再github上运行。

## 如何配置

1. **Fork 本仓库**: 点击本仓库右上角的 "Fork" 按钮。

2. **配置 Secrets**: 进入你 Fork 的仓库的 "Settings" > "Secrets" 页面，添加以下 Secrets：

   - `ALI_REFRESH_TOKEN`: 你的阿里云盘刷新令牌。这个链接教你如何获得 Refresh Token：https://alist.nn.ci/zh/guide/drivers/aliyundrive.html
   - `TY_USER`: 你的天翼云盘用户名。
   - `TY_PWD`: 你的天翼云盘密码。
   - `YOUDAO_COOKIE`: 你的有道云笔记签到 Cookie。登录有道网页版本，按F12后选择 网络network标签，刷新下网页随便点一个加载的页面，按下图内容复制
     
      ![image](https://github.com/jinde98/dailycheckin/assets/127750182/2fc6fc11-b1bd-4d6c-b4ff-f0f42d5d5ffe)
   - `REDIS_INFO` ：REDIS存储有道笔记cookie和阿里云盘的刷新令牌，保证自动更新令牌。（有道的笔记在Action中登录并获取cookie还有问题，但在本地运行没问题）可以去官网https://redis.io/try-free/ 申请一个账户，免费有30m空间，足够保存令牌信息了。茅台申购的config.json也放入redis了。
   - `AMAP_KEY `: 高德地图的key（用于茅台申购定位）

   - `PUSHPLUS_TOKEN`: 你的 Pushplus 令牌。
   - `SERVERCHAN_SENDKEY`: 你的 ServerChan 发送密钥。
   - `WECOM_TOKENS`: 你的企业微信令牌（如果有多个请用逗号分隔）。
   - `WECOM_WEBHOOK`: 你的企业微信 Webhook URL。
   - `BARK_DEVICEKEY`: 你的 Bark 设备密钥。
   - `FEISHU_DEVICEKEY`: 你的飞书设备密钥。
   - `TELEGRAM_TOKEN`: 你的 Telegram 机器人令牌。格式为 bot_token, chat_id （用英文逗号分隔）
   - `DINGTALK_WEBHOOK`: 你的钉钉机器人的 Webhook URL。

3. **运行 GitHub Action**: 该 Action 预定在每天 UTC 0:00 运行。你可以在 "Actions" 标签页中查看工作流的运行状态。


## 配置 GitHub Actions

1. 在您的 GitHub 仓库中，确保存在 `.github/workflows/` 目录。
2. 创建或编辑一个 YML 文件，本项目是run.yml
3. 修改启动时间，可以根据自己的要求来（不修改就是用默认的）。以下是示例
   on:
  schedule:
    - cron: '0 5 * * *' 这里的是UTC时间，换算北京时间就是13点
    - 
## 支持的服务
支持的签到
- **阿里云盘**: 暂时无法使用。
- **天翼云盘**: 每日签到。
  
最新：关于天翼云设备锁问题导致登陆失败或者提示登录错误：设备ID不存在，需要二次设备校验的解决办法！ 登陆这个网址：https://e.dlife.cn/user/index.do

会弹出新网页，默认显示【个人信息】，点左侧【帐号安全】

5、关闭【设备锁】，即可
<img width="1048" height="564" alt="image" src="https://github.com/user-attachments/assets/3529da36-b95f-4cd2-a969-12684441992b" />

- **有道云笔记**: 每日签到。
- **茅台申购**： 每日9-10点自动申购

支持的推送有
- **Pushplus**: 通知服务。
- **ServerChan**: 方糖通知服务。
- **企业微信（企业版微信）**: 通知服务。
- **Bark**: 通知服务。
- **飞书（Lark）**: 通知服务。
- **Telegram**: 通知服务。

## 待改进内容
- **有道云笔记** 自动更新cookies

后续待增加.......

## 本地开发

要在本地运行此项目，您需要：

1.  使用 `pip install -r requirements.txt` 安装所需的依赖项。
2.  基于 `.env.example` 文件创建 `.env` 文件，并填写所需的环境变量。
3.  运行 `imaotai_login.py` 脚本以生成茅台申购的 `config.json` 文件，如果配置的redis，会把config.json上传到redis。
4.  运行 `main.py` 脚本以执行每日签到任务。

## 项目依赖

项目的依赖项在 `requirements.txt` 文件中列出：

```
requests
redis
python-dotenv
```

## 项目配置

项目的配置位于 `config.py` 文件中。此文件包含各种服务和通知的设置。

## 项目结构

项目的入口点是 `main.py` 文件。其他重要文件包括：

-   `aliyunpan.py`: 包含阿里云盘签到的代码。
-   `tianyiyunpan.py`: 包含天翼云盘签到的代码。
-   `YouDao_user_login.py`: 包含有道云笔记签到的代码。
-   `imaotai.py`: 包含茅台申购的代码。
-   `message_send.py`: 包含发送通知的代码。
-   `.env.example`: 提供了需要设置的环境变量的示例。
-   `.gitignore`: 指定了 Git 应该忽略的未跟踪文件。

## 未来改进

我们计划在未来增加对更多签到服务和通知方式的支持。

## 感谢

特别感谢以下贡献者为项目作出的重要贡献：

- [boci] - 提供了天翼云盘的签到代码。
- [libuke](https://github.com/libuke) - 提供了部分推送服务的代码。

如果有遗漏或其他贡献者，请提交 Pull Request 补充。
