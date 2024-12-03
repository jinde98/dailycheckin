# 每日签到 GitHub Action部署

## 功能简介

这个 GitHub Action 用于执行各种服务的每日签到任务，目前支持有道、阿里云盘、天翼云盘、茅台申购。
茅台申购自动生成配置文件，需要在本地运行imaotai_login.py。如果有redis，可以把配置文件保存到redis，这样可以再githu上运行。

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

其他签到内容.......

后续待增加.......

## 感谢

特别感谢以下贡献者为项目作出的重要贡献：

- [boci] - 提供了天翼云盘的签到代码。
- [libuke](https://github.com/libuke) - 提供了部分推送服务的代码。

如果有遗漏或其他贡献者，请提交 Pull Request 补充。
