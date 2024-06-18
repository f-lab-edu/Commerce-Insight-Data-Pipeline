from src.database import Base
from sqlalchemy import Column, Integer, String


class AmazonProduct(Base):
    __tablename__ = "amazon_product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String)
    price = Column(String)
    rating = Column(String)
    review_count = Column(String)
    url = Column(String)


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
