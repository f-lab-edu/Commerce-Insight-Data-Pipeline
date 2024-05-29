from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime, timedelta
import pytz

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


def main(start_time, end_time, replace=False):
    keyword = "icecream"
    response = get_info_from_twitter_api(keyword)
    tweet_generator = generate_tweet_data(response, keyword)
    user_generator = generate_tweet_user(response, keyword)

    save_tweet_info(tweet_generator, user_generator)


def get_input_time(prompt, timezone, default_time=None, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            time_str = input(prompt)
            if not time_str.strip() and default_time is not None:
                return default_time
            time = timezone.localize(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
            return time
        except ValueError:
            attempts += 1
            if attempts < max_attempts:
                print(
                    f"잘못된 형식입니다. 다시 입력해주세요. ({attempts}/{max_attempts})"
                )
            else:
                print("입력 횟수를 초과했습니다. 기본값을 사용합니다.")
                return default_time


if __name__ == "__main__":
    korea_tz = pytz.timezone("Asia/Seoul")

    start_time_default = korea_tz.localize(datetime.now())
    start_time = get_input_time(
        "(twitter) 시작 시간을 입력하세요 (YYYY-MM-DD HH:MM:SS): ",
        korea_tz,
        start_time_default,
    )

    end_time_default = start_time + timedelta(minutes=1)
    end_time = get_input_time(
        "(twitter) 끝 시간을 입력하세요 (YYYY-MM-DD HH:MM:SS): ",
        korea_tz,
        end_time_default,
    )

    # replace_str = input("replace 하십니까? Y/N: ")
    # replace = True if replace_str == "Y" else False

    main(start_time, end_time)
