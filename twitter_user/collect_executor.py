from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import logging
from logging.handlers import RotatingFileHandler

# from datetime import datetime, timedelta
# import pytz
import sys

sys.path.append("../")
from amazon_product.collect_executor import AmazonProduct
import time

local_path = "sqlite:///../tweet_info.db"
engine = create_engine(local_path, echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class TweetInfo(Base):
    __tablename__ = "tweet_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(String)
    tweet_text = Column(String)
    tweet_created_at = Column(String)
    tweet_language = Column(String)
    tweet_favorite_count = Column(Integer)
    tweet_retweet_count = Column(Integer)
    tweet_reply_count = Column(Integer)
    tweet_quote_count = Column(Integer)
    tweet_retweet = Column(String)
    tweet_timestamp = Column(String)
    hashtag = Column(String)
    tweet_views = Column(Integer)


class TweetUser(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hashtag = Column(String)
    user_id = Column(String)
    user_created_at = Column(String)
    username = Column(String)
    name = Column(String)
    user_follower_count = Column(Integer)
    user_following_count = Column(Integer)
    user_is_private = Column(String)
    user_is_verified = Column(String)
    user_location = Column(String)
    user_description = Column(String)
    user_external_url = Column(String)
    user_number_of_tweets = Column(Integer)
    user_bot = Column(String)
    user_timestamp = Column(String)


def get_info_from_twitter_api(hashtag):
    url = "https://twitter154.p.rapidapi.com/hashtag/hashtag"
    querystring = {"hashtag": f"#{hashtag}", "limit": "20", "section": "top"}
    headers = {
        "X-RapidAPI-Key": "8aa777509amsha8662f9648509b0p158304jsn868af5491a28",
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def generate_tweet_data(response, hashtag):
    for data in response["results"]:
        tweet_info = {
            "tweet_id": data["tweet_id"],
            "tweet_text": data["text"],
            "tweet_created_at": data["creation_date"],
            "tweet_language": data["language"],
            "tweet_favorite_count": data["favorite_count"],
            "tweet_retweet_count": data["retweet_count"],
            "tweet_reply_count": data["reply_count"],
            "tweet_quote_count": data["quote_count"],
            "tweet_retweet": data["retweet"],
            "tweet_timestamp": data["timestamp"],
            "hashtag": hashtag,
            "tweet_views": data["views"],
        }
        yield tweet_info


def generate_tweet_user(response, hashtag):
    for data in response["results"]:
        data = data["user"]
        user_info = {
            "hashtag": hashtag,
            "user_id": data["user_id"],
            "user_created_at": data["creation_date"],
            "username": data["username"],
            "name": data["name"],
            "user_follower_count": data["follower_count"],
            "user_following_count": data["following_count"],
            "user_is_private": data["is_private"],
            "user_is_verified": data["is_verified"],
            "user_location": data["location"],
            "user_description": data["description"],
            "user_external_url": data["external_url"],
            "user_number_of_tweets": data["number_of_tweets"],
            "user_bot": data["bot"],
            "user_timestamp": data["timestamp"],
        }
        yield user_info


def save_tweet_info(tweet_generator, user_generator):
    for tweet_info in tweet_generator:
        tweet = TweetInfo(**tweet_info)
        session.add(tweet)
        session.commit()

    for user_info in user_generator:
        user = TweetUser(**user_info)
        session.add(user)
        session.commit()


def get_amazon_product(batch_size, offset):
    log_file = "../log/twitter.log"
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

    while True:
        pn = (
            session.query(AmazonProduct.product_name)
            .limit(batch_size)
            .offset(offset)
            .all()
        )
        if not pn:
            logger.info("No more products to fetch.")
            break

        logger.info(f"Next batch: {len(pn)}..")
        keywords = [product_name[0] for product_name in pn]

        offset += batch_size
        time.sleep(3)

        yield keywords


def main():
    for keywords in get_amazon_product(50, 0):
        for keyword in keywords:
            response = get_info_from_twitter_api(keyword)
            tweet_generator = generate_tweet_data(response, keyword)
            user_generator = generate_tweet_user(response, keyword)

            save_tweet_info(tweet_generator, user_generator)


if __name__ == "__main__":
    main()
