import requests
import time
from src.log import twitter_logger as logger
from src.db_init import (
    client,
    dataset_id,
    amazon_product_table_id,
    tweet_info_table,
    user_info_table,
)
import uuid


def get_info_from_twitter_api(hashtag):
    url = "https://twitter154.p.rapidapi.com/hashtag/hashtag"
    querystring = {"hashtag": f"#{hashtag}", "limit": "20", "section": "top"}
    headers = {
        "X-RapidAPI-Key": "1b811fe99cmsh9814008f488ce6cp11527djsnd045279efa81",
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def generate_tweet_data(response, hashtag):
    for data in response["results"]:
        tweet_info = {
            "id": str(uuid.uuid4()),
            "tweet_id": data["tweet_id"],
            "tweet_text": data["text"],
            "tweet_created_at": data["creation_date"],
            "tweet_language": data["language"],
            "tweet_favorite_count": data["favorite_count"],
            "tweet_retweet_count": data["retweet_count"],
            "tweet_reply_count": data["reply_count"],
            "tweet_quote_count": data["quote_count"],
            "tweet_retweet": str(data["retweet"]),
            "tweet_timestamp": data["timestamp"],
            "hashtag": hashtag,
            "tweet_views": data["views"],
        }
        yield tweet_info


def generate_tweet_user(response, hashtag):
    for data in response["results"]:
        data = data["user"]
        user_info = {
            "id": str(uuid.uuid4()),
            "hashtag": hashtag,
            "user_id": data["user_id"],
            "user_created_at": data["creation_date"],
            "username": data["username"],
            "name": data["name"],
            "user_follower_count": data["follower_count"],
            "user_following_count": data["following_count"],
            "user_is_private": data["is_private"],
            "user_is_verified": str(data["is_verified"]),
            "user_location": data["location"],
            "user_description": data["description"],
            "user_external_url": data["external_url"],
            "user_number_of_tweets": data["number_of_tweets"],
            "user_bot": str(data["bot"]),
            "user_timestamp": data["timestamp"],
        }
        yield user_info


def save_tweet_info(tweet_generator, user_generator):
    for tweet_info in tweet_generator:
        errors = client.insert_rows_json(tweet_info_table, [tweet_info])
        if not errors:
            logger.info("트위터 트윗 데이터가 성공적으로 삽입되었습니다.")
        else:
            logger.error("트위터 트윗 데이터 삽입 중 오류가 발생했습니다:", errors)

    for user_info in user_generator:
        errors = client.insert_rows_json(user_info_table, [user_info])
        if not errors:
            logger.info("트위터 유저 데이터가 성공적으로 삽입되었습니다.")
        else:
            logger.error("트위터 유저 데이터 삽입 중 오류가 발생했습니다:", errors)


def get_amazon_product(client, table_id, batch_size, offset):
    query = f"""
        SELECT product_name
        FROM `{table_id}`
        LIMIT {batch_size}
        OFFSET {offset}
    """
    idx = 0
    while True:
        query_job = client.query(query)
        results = query_job.result()

        pn = [row["product_name"] for row in results]

        if len(pn) == 0 or set(pn) == {""}:
            logger.info("No more products to fetch.")
            break
        if idx == 5:
            logger.info("There's no products. (5/5)")

        if offset == 0 and (len(pn) == 0 or set(pn) == {""}):
            logger.info("There's no products yet..")
            time.sleep(5)
            idx += 1

        logger.info(f"Next batch: {len(pn)}..")

        offset += batch_size
        time.sleep(3)

        yield pn


def main():
    amazon_tid = f"{client.project}.{dataset_id}.{amazon_product_table_id}"
    for keywords in get_amazon_product(client, amazon_tid, 50, 0):
        for keyword in keywords:
            response = get_info_from_twitter_api(keyword)
            if isinstance(response, dict) and "results" in response.keys():
                tweet_generator = generate_tweet_data(response, keyword)
                user_generator = generate_tweet_user(response, keyword)

                save_tweet_info(tweet_generator, user_generator)


if __name__ == "__main__":
    main()
"""
airflow로 동시 돌릴때 offset은 어떻게 해결할지 고민 
"""
