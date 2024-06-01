#!/bin/bash


db_init="./db_init.py"
collect_executor="./collect_executor.py"

echo "실행 중인 Python 파일: $db_init"
python "$db_init"
exit_status=$?

if [ $exit_status -eq 0 ]; then
    echo "$db_init 파일이 성공적으로 실행되었습니다."
else
    echo "$db_init 파일 실행 중 오류가 발생했습니다."
    exit 1
fi

cd amazon_product
echo "실행 중인 Python 파일: amazon_collect"
python "$collect_executor" &
amazon_pid=$!

cd twitter_user
echo "실행 중인 Python 파일: twiiter_collect"
python "$collect_executor" &
twitter_pid=$!

wait $amazon_pid
amazon_status=$?
if [ $amazon_status -eq 0 ]; then
    echo "$collect_executor 파일이 성공적으로 실행되었습니다."
else
    echo "amazon $collect_executor 파일 실행 중 오류가 발생했습니다."
    exit 1
fi

wait $twitter_pid
twitter_status=$?
if [ $twitter_status -eq 0 ]; then
    echo "$collect_executor 파일이 성공적으로 실행되었습니다."
else
    echo "twitter $collect_executor 파일 실행 중 오류가 발생했습니다."
    exit 1
fi

if [ $amazon_status -eq 0 ] && [ $twitter_status -eq 0 ]; then
    exit 0
else
    exit 1
fi