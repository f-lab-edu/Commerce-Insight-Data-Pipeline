import requests
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from src.log import amazon_logger as logger
from src.db_init import client, amazon_product_table


def get_page(url, headers, logger):
    response = requests.get(url, headers=headers)
    html = response.text
    logger.debug(f"url: {url}")
    logger.debug(f"status code: {response.status_code}")

    if response.status_code == 429:
        time.sleep(1)
        return get_page(url, headers, logger)
    return html


def extract_product_info(html):
    soup = BeautifulSoup(html, "html.parser")
    product_list = []

    for product in soup.select("div[data-asin]"):
        # 상품명 추출
        title_element = product.select_one(
            'div[class*="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"]'
        )
        if title_element:
            title = title_element.get_text(strip=True)
        else:
            title = ""

        # 가격 추출
        price_element = product.select_one('span[class*="p13n-sc-price"]')
        if price_element:
            price = price_element.get_text(strip=True)
        else:
            price = ""

        # 평점 추출
        rating_element = product.select_one('i[class*="a-icon-star"]')
        if rating_element:
            rating = rating_element.get_text(strip=True)
        else:
            rating = ""

        # 리뷰 수 추출
        review_count_element = product.select_one('span[class*="a-size-small"]')
        if review_count_element:
            review_count = review_count_element.get_text(strip=True)
        else:
            review_count = ""

        product_info = {
            "product_name": title,
            "price": price,
            "rating": rating,
            "review_count": review_count,
        }
        product_list.append(product_info)

    return product_list


def get_amazon_best_sellers(current_time, end_time, chunk_minutes=1):
    amazon_url = "https://www.amazon.com"
    amazon_best_seller_url = "https://www.amazon.com/Best-Sellers/zgbs"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    logger.info(f"Start.. current time: {current_time}, end time: {end_time} ")
    while True:
        if current_time >= end_time:
            logger.info(
                f"Data collection has reached the end time. current time: {current_time}, end time: {end_time}  "
            )
            break

        html = get_page(amazon_best_seller_url, headers, logger)
        soup = BeautifulSoup(html, "html.parser")

        # 카테고리 div
        for _ in range(5):
            category_div = soup.find(
                "div", class_="_p13n-zg-nav-tree-all_style_zg-browse-root__-jwNv"
            )

            if category_div:
                html_content = str(category_div)
                url_pattern = re.compile(r'href="(.*?)"')
                best_seller_urls = url_pattern.findall(html_content)
                break

            else:
                logger.error("Amazon Category div not found.")
            time.sleep(3)

        chunk_start_time = current_time
        chunk_end_time = current_time + timedelta(minutes=chunk_minutes)

        for url in best_seller_urls:

            if current_time >= chunk_end_time:
                logger.info(f"Chunk time limit reached. Moving to the next chunk.")
                break

            url = amazon_url + url
            logger.info(f"best seller url: {url}")
            html = get_page(url, headers, logger)
            if html:
                product_list = extract_product_info(html)
                for product in product_list:
                    logger.info(f"상품명: {product['product_name']}")
                    logger.info(f"가격: {product['price']}")
                    logger.info(f"평점: {product['rating']}")
                    logger.info(f"리뷰 수: {product['review_count']}")

                    amazon_product = {
                        "product_name": product["product_name"],
                        "price": product["price"],
                        "rating": product["rating"],
                        "review_count": product["review_count"],
                        "url": url,
                    }
                    yield amazon_product
            else:
                logger.error("페이지를 가져올 수 없습니다.")

        elapsed_time = datetime.now() - chunk_start_time
        remaining_time = timedelta(minutes=chunk_minutes) - elapsed_time
        if remaining_time > timedelta(seconds=0):
            logger.info(f"Sleeping for {remaining_time} until the next chunk.")
            time.sleep(remaining_time.total_seconds())
        current_time = datetime.now()


def save_amazon_product(amazon_generator):
    for amazon_product in amazon_generator:
        errors = client.insert_rows_json(amazon_product_table, amazon_product)
        if not errors:
            print("데이터가 성공적으로 삽입되었습니다.")
        else:
            print("데이터 삽입 중 오류가 발생했습니다:", errors)


def main(start_time, end_time, chunk_minutes=1, replace=False):
    amazon_generator = get_amazon_best_sellers(start_time, end_time, chunk_minutes)
    save_amazon_product(amazon_generator)


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
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=1)
    main(start_time, end_time, chunk_minutes=1)
