import sqlite3
import os

# SQL 문 준비
create_amazon_product_table = """
CREATE TABLE amazon_product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    price TEXT,
    rating TEXT,
    review_count TEXT,
    url TEXT
);
"""

create_tweet_info_table = """
CREATE TABLE tweet_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT,
    tweet_text TEXT,
    tweet_created_at TEXT,
    tweet_language TEXT,
    tweet_favorite_count INTEGER,
    tweet_retweet_count INTEGER,
    tweet_reply_count INTEGER,
    tweet_quote_count INTEGER,
    tweet_retweet TEXT,
    tweet_timestamp TEXT,
    hashtag TEXT,
    tweet_views INTEGER
);
"""

create_user_info_table = """
CREATE TABLE user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hashtag TEXT,
    user_id TEXT,
    user_created_at TEXT,
    username TEXT,
    name TEXT,
    user_follower_count INTEGER,
    user_following_count INTEGER,
    user_is_private TEXT,
    user_is_verified TEXT,
    user_location TEXT,
    user_description TEXT,
    user_external_url TEXT,
    user_number_of_tweets INTEGER,
    user_bot TEXT,
    user_timestamp TEXT
);
"""

# 현재 경로에 tweet_info.db 파일이 존재하는지 확인
db_file = "./tweet_info.db"

if not os.path.exists(db_file):
    # tweet_info.db 파일이 없는 경우에만 테이블 생성
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(create_amazon_product_table)
    cursor.execute(create_tweet_info_table)
    cursor.execute(create_user_info_table)

    conn.commit()
    conn.close()
    print("tweet_info.db 파일이 생성되었고, 테이블이 초기화되었습니다.")
else:
    print("tweet_info.db 파일이 이미 존재합니다.")
