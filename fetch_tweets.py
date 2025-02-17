import os
import requests
import datetime
from dateutil import parser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# **📌 读取环境变量**
TIKHUB_API_KEY = os.getenv("TIKHUB_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
#SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS").split(",")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))  # 默认 465 端口

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
        return None

    data = response.json()
    tweets_data = data.get("data", {})
    timeline = tweets_data.get("timeline", [])

    return timeline  # 直接返回推文列表

# **📌 发送邮件**
def send_email(content):
    subject = "📢 Twitter 最新推文"
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    for recipient in RECIPIENT_EMAILS:
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
