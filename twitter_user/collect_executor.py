import logging
from logging.handlers import RotatingFileHandler

def get_twitter_user_related_hashtag():
    # amazon_url = "https://www.amazon.com"
    # amazon_best_seller_url = "https://www.amazon.com/Best-Sellers/zgbs"

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    # }

    
    log_file = '../log/twitter_user.log'
    max_file_size = 1024 * 1024 * 10  # 10MB
    backup_count = 5

    handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  
    logger.addHandler(handler)

    # amazon_product.crawler(amazon_url, amazon_best_seller_url, headers, logger)
    logger.info(f"twitter user test")

if __name__ == '__main__':
    get_twitter_user_related_hashtag()