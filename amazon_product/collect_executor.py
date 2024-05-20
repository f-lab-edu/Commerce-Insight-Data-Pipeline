from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import re
import time
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler

engine = create_engine("sqlite:////amazon_product/amazon_product.db", echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class AmazonProduct(Base):
    __tablename__ = "amazon_product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String)
    price = Column(String)
    rating = Column(String)
    review_count = Column(String)
    url = Column(String)


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


def get_amazon_best_sellers():
    amazon_url = "https://www.amazon.com"
    amazon_best_seller_url = "https://www.amazon.com/Best-Sellers/zgbs"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    log_file = "../log/amazon_product.log"
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

    for url in best_seller_urls:
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


def save_amazon_product(amazon_generator):
    for amazon_product in amazon_generator:
        amazon = AmazonProduct(**amazon_product)
        session.add(amazon)
        session.commit()


def main():
    amazon_generator = get_amazon_best_sellers()
    save_amazon_product(amazon_generator)


if __name__ == "__main__":
    main()
