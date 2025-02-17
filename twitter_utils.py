# -*- coding: utf-8 -*-
"""
Twitter API 相关功能
"""

import os
import requests
from dateutil import parser
from twitter_config import TWITTER_AI_USERS  # ✅ 引入配置文件

# **📌 读取环境变量**
TIKHUB_API_KEY = os.getenv("TIKHUB_API_KEY")

if not TIKHUB_API_KEY:
    print("❌ 未找到 API Key，请检查环境变量是否正确加载！")
    exit(1)

# **📌 API URL**
PROFILE_API_URL = "https://api.tikhub.io/api/v1/twitter/web/fetch_user_profile"
TWEET_API_URL = "https://api.tikhub.io/api/v1/twitter/web/fetch_user_post_tweet"

# **📌 通过 screen_name 获取用户信息**
def get_user_profile(screen_name):
    headers = {"Authorization": f"Bearer {TIKHUB_API_KEY}"}
    params = {"screen_name": screen_name}

    response = requests.get(PROFILE_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ 获取 {screen_name} 个人信息失败: {response.text}")
        return None

    data = response.json().get("data", {})
    return {
        "id": data.get("rest_id"),
        "name": data.get("name"),
        "screen_name": data.get("screen_name"),
        "bio": data.get("description"),
        "followers": data.get("followers_count"),
        "profile_image": data.get("profile_image_url")
    }

# **📌 通过 screen_name 获取最新推文**
def get_latest_tweets(screen_name):
    user_profile = get_user_profile(screen_name)
    if not user_profile:
        return None

    headers = {"Authorization": f"Bearer {TIKHUB_API_KEY}"}
    params = {"rest_id": user_profile["id"]}

    response = requests.get(TWEET_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ 获取 {screen_name} 推文失败: {response.text}")
        return None

    data = response.json().get("data", {}).get("timeline", [])
    tweets = []
    for tweet in data:
        tweet_time = parser.parse(tweet["created_at"]).strftime("%Y-%m-%d %H:%M")
        tweets.append({
            "text": tweet["text"],
            "created_at": tweet_time
        })

    return {"profile": user_profile, "tweets": tweets}
