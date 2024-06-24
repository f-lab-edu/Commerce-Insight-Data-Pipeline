from google.cloud import bigquery
from google.api_core import exceptions

key_path = "../../teak-kit-424413-m1-b3f5816fcc56.json"

# BigQuery 클라이언트 생성
client = bigquery.Client.from_service_account_json(key_path)

# 데이터셋 및 테이블 ID 설정
dataset_id = "cidp"
amazon_product_table_id = "amazon_product"
tweet_info_table_id = "tweet_info"
user_info_table_id = "user_info"

# 데이터셋 생성 (이미 존재하는 경우 건너뜀)
dataset = bigquery.Dataset(f"{client.project}.{dataset_id}")
dataset = client.create_dataset(dataset, exists_ok=True)

# 테이블 스키마 정의
amazon_product_schema = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("product_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("price", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("rating", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("review_count", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("url", "STRING", mode="NULLABLE"),
]

tweet_info_schema = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("tweet_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("tweet_text", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("tweet_created_at", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("tweet_language", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("tweet_favorite_count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("tweet_retweet_count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("tweet_reply_count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("tweet_quote_count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("tweet_retweet", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("tweet_timestamp", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("hashtag", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("tweet_views", "INTEGER", mode="NULLABLE"),
]

user_info_schema = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("hashtag", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_created_at", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("username", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_follower_count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("user_following_count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("user_is_private", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_is_verified", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_location", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_description", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_external_url", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_number_of_tweets", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("user_bot", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_timestamp", "STRING", mode="NULLABLE"),
]


# 테이블 존재 여부 확인 및 생성
def create_table_if_not_exists(table_id, schema):
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        table = client.get_table(table_ref)
        print(
            f"테이블이 이미 존재합니다: {table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}"
        )
    except exceptions.NotFound:
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"테이블 생성 완료: {table.project}.{table.dataset_id}.{table.table_id}")
    return table


# 테이블 생성 함수 호출
amazon_product_table = create_table_if_not_exists(
    amazon_product_table_id, amazon_product_schema
)
tweet_info_table = create_table_if_not_exists(tweet_info_table_id, tweet_info_schema)
user_info_table = create_table_if_not_exists(user_info_table_id, user_info_schema)
