from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

engine = create_engine('sqlite:////twitter_user/tweet_info.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class TweetInfo(Base):
    __tablename__ = 'tweet_info'

    tweet_id = Column(String, primary_key=True)
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

def get_info_from_twitter_api(hashtag):
    url = "https://twitter154.p.rapidapi.com/hashtag/hashtag"
    querystring = {"hashtag":f"#{hashtag}","limit":"20","section":"top"}
    headers = {
        "X-RapidAPI-Key": "8aa777509amsha8662f9648509b0p158304jsn868af5491a28",
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def generate_tweet_data(response, hashtag):
    for data in response['results']:
        tweet_info = {
            'tweet_id': data['tweet_id'],
            'tweet_text': data['text'],
            'tweet_created_at': data['creation_date'],
            'tweet_language': data['language'],
            'tweet_favorite_count': data['favorite_count'],
            'tweet_retweet_count': data['retweet_count'],
            'tweet_reply_count': data['reply_count'],
            'tweet_quote_count': data['quote_count'],
            'tweet_retweet': data['retweet'],
            'tweet_timestamp': data['timestamp'],
            'hashtag': hashtag,
            'tweet_views': data['views']
        }
        yield tweet_info

def save_tweet_info(tweet_generator):
    for tweet_info in tweet_generator:
        tweet = TweetInfo(**tweet_info)
        session.add(tweet)
        session.commit()
        

def main():
    keyword = "poetry"
    response = get_info_from_twitter_api(keyword)
    tweet_generator = generate_tweet_data(response, keyword)
    save_tweet_info(tweet_generator)

if __name__ == '__main__':
    main()
