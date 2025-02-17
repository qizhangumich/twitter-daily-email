# -*- coding: utf-8 -*-
"""
Twitter 自动获取推文并发送邮件
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twitter_utils import get_latest_tweets
from twitter_config import TWITTER_AI_USERS  # ✅ 直接引入配置文件

# **📌 读取环境变量**
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = 465  # 默认 465 端口
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS", "").split(",")

# **📌 发送邮件**
def send_email(content):
    if not content.strip():
        print("⚠️ 没有新推文，不发送邮件")
        return

    subject = "📢 AI 领域 Twitter 最新推文"
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

    for screen_name in TWITTER_AI_USERS:
        result = get_latest_tweets(screen_name)
        if result:
            profile = result["profile"]
            tweets = result["tweets"]

            email_content += f"🧑‍💻 {profile['name']} (@{profile['screen_name']})\n"
            email_content += f"📖 {profile['bio']}\n"
            email_content += f"👥 粉丝数: {profile['followers']}\n"
            email_content += f"🖼️ 头像: {profile['profile_image']}\n\n"

            for tweet in tweets:
                email_content += f"🆕 {tweet['text']}\n🕒 {tweet['created_at']}\n\n"

            email_content += "--------------------------\n"

    print(email_content)  # 打印到控制台
    send_email(email_content)  # 发送邮件
