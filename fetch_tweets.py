# -*- coding: utf-8 -*-
"""
📢 Twitter 自动获取推文并发送邮件（HTML 格式）
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twitter_utils import get_latest_tweets
from twitter_config import TWITTER_AI_USERS, TWITTER_BIO  # ✅ Twitter 账号信息
from email_config import RECEIVER_EMAILS  # ✅ 读取收件人信息

# **📌 读取环境变量**
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = 465  # 默认 465 端口
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# **📌 发送邮件（HTML 格式）**
def send_email(content):
    if not content.strip():
        print("⚠️ 没有新推文，不发送邮件")
        return

    subject = "📢 AI 领域 Twitter 最新推文"

    # **📌 组装邮件**
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS)
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "html"))  # ✅ 发送 HTML 格式的邮件

    # **📌 发送邮件**
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
    server.quit()

    print("📩 邮件发送成功！")


# **📌 运行主函数**
if __name__ == "__main__":
    email_content = "<html><body>"
    email_content += "<h2>📢 AI 领域 Twitter 最新推文</h2>"
    email_content += "<hr style='border: 1px solid #ccc;'>"

    for screen_name in TWITTER_AI_USERS:
        result = get_latest_tweets(screen_name)
        if result:
            tweets = result["tweets"]

            # **📌 显示 Twitter 用户名**
            email_content += f"""
            <h3>🧑‍💻 <a href='https://twitter.com/{screen_name}' target='_blank'>{TWITTER_BIO.get(screen_name, screen_name)}</a></h3>
            <hr style='border: 1px dashed #ccc;'>
            """

            # **📌 显示最新推文**
            for tweet in tweets:
                email_content += f"""
                <p>🆕 <strong>{tweet['text']}</strong></p>
                <p>🕒 {tweet['created_at']}</p>
                <hr style='border: 1px solid #ddd;'>
                """

    email_content += "</body></html>"

    print(email_content)  # ✅ 在控制台打印
    send_email(email_content)  # ✅ 发送邮件
