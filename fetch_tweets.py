import requests
import datetime
from dateutil import parser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAILS, TIKHUB_API_KEY, TWITTER_USERS

API_URL = "https://api.tikhub.io/api/v1/twitter/web/fetch_user_post_tweet"

# **📌 获取推文数据**
def get_latest_tweets(user_id):
    headers = {"Authorization": f"Bearer {TIKHUB_API_KEY}"}
    params = {"rest_id": user_id}

    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ 获取 {TWITTER_USERS[user_id]} 推文失败: {response.text}")
        return None

    data = response.json()
    tweets_data = data.get("data", {})

    # **📌 提取最新推文**
    timeline = tweets_data.get("timeline", [])
    latest_tweet = timeline[0] if timeline else None
    latest = {
        "text": latest_tweet.get("text", "无"),
        "created_at": format_time(latest_tweet.get("created_at"))
    } if latest_tweet else None

    return latest

# **📌 格式化时间**
def format_time(time_str):
    if not time_str:
        return "未知"
    parsed_time = parser.parse(time_str)
    return parsed_time.strftime("%Y-%m-%d %H:%M")

# **📌 发送邮件**
def send_email(content):
    subject = "Twitter 最新推文"

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
        tweet = get_latest_tweets(user_id)
        if tweet:
            email_content += f"----- {user_name} -----\n"
            email_content += f"🆕 最新推文:\n{tweet['text']}\n🕒 发布时间: {tweet['created_at']}\n\n"

    print(email_content)  # 打印到控制台
    send_email(email_content)  # 发送邮件
