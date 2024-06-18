import requests
import re
import time
from bs4 import BeautifulSoup


def get_page(url, headers, logger):
    # URL에서 HTML 페이지를 가져옵니다.
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
            "title": title,
            "price": price,
            "rating": rating,
            "review_count": review_count,
        }
        product_list.append(product_info)

    return product_list


def crawler(amazon_url, url, headers, logger):
    html = get_page(url, headers, logger)
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
        logger.info(f"best seller url: url")
        html = get_page(url, headers, logger)
        if html:
            product_list = extract_product_info(html)
            for product in product_list:
                logger.info(f"상품명: {product['title']}")
                logger.info(f"가격: {product['price']}")
                logger.info(f"평점: {product['rating']}")
                logger.info(f"리뷰 수: {product['review_count']}")
        else:
            logger.error("페이지를 가져올 수 없습니다.")
