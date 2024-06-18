import sqlite3
import os
import logging
from logging.handlers import RotatingFileHandler

log_dir = "./log"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "db_init.log")

max_file_size = 1024 * 1024 * 10  # 10MB
backup_count = 5

handler = RotatingFileHandler(
    log_file, maxBytes=max_file_size, backupCount=backup_count
)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

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
    logger.info("tweet_info.db was created, and the table was initialized.")
else:
    logger.info("tweet_info.db already exists.")
