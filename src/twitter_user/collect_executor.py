import requests
import logging
from logging.handlers import RotatingFileHandler
import os
from src.models.db_table import TweetInfo, TweetUser, AmazonProduct
from src.database import session
import time


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
    log_dir = "../log"
    log_file = os.path.join(log_dir, "twitter.log")
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
            if isinstance(response, dict) and "results" in response.keys():
                tweet_generator = generate_tweet_data(response, keyword)
                user_generator = generate_tweet_user(response, keyword)

                save_tweet_info(tweet_generator, user_generator)


if __name__ == "__main__":
    main()