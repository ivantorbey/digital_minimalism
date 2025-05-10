#!/usr/bin/env python3

import praw
import datetime
import re
import smtplib
from email.message import EmailMessage

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"       # Replace with your Gmail address
EMAIL_PASSWORD = "your_email_app_password"   # Replace with your Gmail app password
TO_EMAIL = "recipient_email@gmail.com"        # Replace with recipient email address

def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print("✅ Email sent successfully")

def clean_text(text):
    return re.sub(r'[^\w\s.,!?;:\-()]', '', text)

def get_top_posts_from_subreddit(subreddit_name, target_date, limit=3):
    reddit = praw.Reddit(
        client_id="your_client_id",
        client_secret="your_client_secret",
        user_agent="top_posts_emailer by /u/your_username"
    )
    subreddit = reddit.subreddit(subreddit_name)

    start = datetime.datetime.combine(target_date, datetime.time.min).timestamp()
    end = datetime.datetime.combine(target_date, datetime.time.max).timestamp()

    posts = []
    for post in subreddit.top(time_filter="week", limit=200):
        if start <= post.created_utc <= end:
            title = clean_text(post.title or "No Title")
            body = clean_text(post.selftext.strip())
            posts.append((post.score, f"{title}\n{body}"))

    posts.sort(key=lambda x: x[0], reverse=True)
    return [post[1] for post in posts[:limit]]

def reddit_top_posts_emailer():
    target_date = datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=2)
    subreddits = ["cleanjokes", "nosurf", "quotes", "jokes", "askscience"]

    messages = []
    for sub in subreddits:
        top_posts = get_top_posts_from_subreddit(sub, target_date)
        formatted_posts = '\n\n'.join([f"{i+1}. {post}" for i, post in enumerate(top_posts)])
        messages.append(f"Top 3 {sub.capitalize()} posts from {target_date} :\n\n{formatted_posts}")

    final_message = '\n\n'.join(messages)
    send_email(f"Top Reddit Posts from {target_date}", final_message)

if __name__ == "__main__":
    reddit_top_posts_emailer()
