# Commerce-Insight-Data-Pipeline

### 개요
트위터 인플루언서의 트윗이 아마존 제품 판매에 미치는 영향 분석을 위한 데이터 파이프라인을 구축한 리포지토리입니다.

### 개발환경
* Docker
* Python 3.12 (Poetry)

### 실행방법
```
git clone https://github.com/f-lab-edu/Commerce-Insight-Data-Pipeline.git
docker-compose up -d
```
* 호스트에서 http://localhost:5000/test 접속 시 "hi" 반환

### 데이터 생성 
웹 크롤러 API를 개발
* flask

*reference*
1. [트위터 API](https://rapidapi.com/omarmhaimdat/api/twitter154)
2. [아마존 API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data)

