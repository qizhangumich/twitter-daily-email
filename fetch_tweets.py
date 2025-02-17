# -*- coding: utf-8 -*-
"""
Twitter 自动获取推文并发送邮件
"""

import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dateutil import parser  # ✅ 确保正确导入 python-dateutil

# **📌 读取环境变量**
TIKHUB_API_KEY = os.getenv("TIKHUB_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = 465  # 默认 465 端口
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS", "").split(",")

# 🔍 Debug: 打印 API Key 长度
print(f"TIKHUB_API_KEY 获取结果: {'存在' if TIKHUB_API_KEY else '未找到'}，长度: {len(TIKHUB_API_KEY) if TIKHUB_API_KEY else 'None'}")

# 🔥 测试 API Key 是否正确传递
if not TIKHUB_API_KEY:
    print("❌ 未找到 API Key，请检查环境变量是否正确加载！")
    exit(1)

# 🔥 发送测试请求
API_URL = "https://api.tikhub.io/api/v1/twitter/web/fetch_user_post_tweet"
headers = {"Authorization": f"Bearer {TIKHUB_API_KEY}"}
params = {"rest_id": "44196397"}

response = requests.get(API_URL, headers=headers, params=params)
print(f"🔍 API 响应状态码: {response.status_code}")
print(f"🔍 API 返回数据: {response.text}")

if response.status_code == 401:
    print("❌ API Key 无效，请检查密钥是否正确！")
    exit(1)

# **📌 Twitter API 配置**
API_URL = "https://api.tikhub.io/api/v1/twitter/web/fetch_user_post_tweet"

# **📌 目标 Twitter 账号**
TWITTER_USERS = {
    "44196397": "Elon Musk",
    "1367531": "Fox News",
    "1652541": "Reuters"
}

# **📌 获取推文**
def get_latest_tweets(user_id):
    headers = {"Authorization": f"Bearer {TIKHUB_API_KEY}"}
    params = {"rest_id": user_id}

    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ 获取 {TWITTER_USERS[user_id]} 推文失败: {response.text}")
        return []

    data = response.json()
    return data.get("data", {}).get("timeline", [])  # 直接返回推文列表

# **📌 发送邮件**
def send_email(content):
    if not content.strip():
        print("⚠️ 没有新推文，不发送邮件")
        return

    subject = "📢 Twitter 最新推文"
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    for recipient in RECIPIENT_EMAILS:
        if recipient.strip():
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(content, "plain"))

            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
            print(f"📩 邮件已发送至 {recipient}")

    server.quit()

# **📌 运行主函数**
if __name__ == "__main__":
    email_content = ""

    for user_id, user_name in TWITTER_USERS.items():
        tweets = get_latest_tweets(user_id)
        if tweets:
            email_content += f"----- {user_name} -----\n"
            for tweet in tweets:
                tweet_time = parser.parse(tweet["created_at"]).strftime("%Y-%m-%d %H:%M")
                email_content += f"🆕 {tweet['text']}\n🕒 {tweet_time}\n\n"

    print(email_content)  # 打印到控制台
    send_email(email_content)  # 发送邮件
