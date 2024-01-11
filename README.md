# AliyunDrive Sign-in

## 功能简介

`AliyunDrive Sign-in` 是一个基于 GitHub Actions 的自动签到工具，它可以帮助您自动完成阿里云盘的签到操作，并通过 PushPlus 进行通知。

### 主要功能：

1. **自动签到**：每天自动在指定时间进行阿里云盘的签到操作。
2. **通知功能**：使用 PushPlus 来通知您签到的结果。

## 如何配置

### 1. 获取 RefreshToken

这个链接教你如何获得 Refresh Token：https://alist.nn.ci/zh/guide/drivers/aliyundrive.html

### 2. 设置 PushPlus Token

1. 访问 [PushPlus 官网](https://www.pushplus.plus/) 并登录。
2. 在用户中心找到您的 Token。

### 3. 在 GitHub 仓库中设置 Secrets

1. 打开您的 GitHub 仓库。
2. 转到 `Settings` > `Secrets`。
3. 添加两个新的 secrets：
   - `REFRESH_TOKEN`：粘贴您从阿里云盘获取的 `refresh_token`。
   - `PUSHPLUS_TOKEN`：粘贴您从 PushPlus 获取的 Token。没有pushplus，也可以正常运行签到，只是没有通知了

## 配置 GitHub Actions

1. 在您的 GitHub 仓库中，确保存在 `.github/workflows/` 目录。
2. 创建或编辑一个 YAML 文件，本项目是run.yaml
3. 修改启动时间，可以根据自己的要求来改。以下是示例
   on:
  schedule:
    - cron: '0 5 * * *' 这里的是UTC时间，换算北京时间就是13点
