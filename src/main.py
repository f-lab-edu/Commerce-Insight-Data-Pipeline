import sys

sys.path.append(".")
from datetime import datetime, timedelta
from amazon_product import collect_executor as amazon_executor

# from twitter_user import collect_executor as twitter_executor

if __name__ == "__main__":
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=1)
    amazon_executor.main(start_time, end_time, chunk_minutes=1)
    # twitter_executor.main()
