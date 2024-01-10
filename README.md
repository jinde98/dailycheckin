# AliyunDrive Sign-in

## 功能简介

`AliyunDrive Sign-in` 是一个基于 GitHub Actions 的自动签到工具，它可以帮助您自动完成阿里云盘的签到操作，并通过 PushPlus 进行通知。

### 主要功能：

1. **自动签到**：每天自动在指定时间进行阿里云盘的签到操作。
2. **通知功能**：使用 PushPlus 来通知您签到的结果。

## 如何配置

### 1. 获取 RefreshToken

1. 打开浏览器并登录阿里云盘网站。
2. 在浏览器的开发者工具中（通常可以通过 `F12` 键打开），查找网络请求。
3. 执行一次签到操作，然后在开发者工具的网络选项卡中找到对应的请求。
4. 在请求头或请求体中查找 `refresh_token` 字段，复制该值。

### 2. 设置 PushPlus Token

1. 访问 [PushPlus 官网](https://www.pushplus.plus/) 并登录。
2. 在用户中心找到您的 Token。

### 3. 在 GitHub 仓库中设置 Secrets

1. 打开您的 GitHub 仓库。
2. 转到 `Settings` > `Secrets`。
3. 添加两个新的 secrets：
   - `REFRESH_TOKEN`：粘贴您从阿里云盘获取的 `refresh_token`。
   - `PUSHPLUS_TOKEN`：粘贴您从 PushPlus 获取的 Token。没有pushplus，也可以运行，只是没有通知了

## 配置 GitHub Actions

1. 在您的 GitHub 仓库中，确保存在 `.github/workflows/` 目录。
2. 创建或编辑一个 YAML 文件，本项目是run.yaml
3. 修改启动时间，可以根据自己的要求来改。以下是示例
   on:
  schedule:
    - cron: '0 5 * * *'
