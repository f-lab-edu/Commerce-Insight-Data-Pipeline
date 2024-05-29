#!/bin/bash


db_init="./db_init.py"
amazon_collect="./collect_executor.py"

echo "실행 중인 Python 파일: $db_init"
python "$db_init"
exit_status=$?

if [ $exit_status -eq 0 ]; then
    echo "Python 파일이 성공적으로 실행되었습니다."
else
    echo "Python 파일 실행 중 오류가 발생했습니다."
fi

cd amazon_product
echo "실행 중인 Python 파일: $amazon_collect"
python "$amazon_collect"
exit_status=$?
if [ $exit_status -eq 0 ]; then
    echo "Python 파일이 성공적으로 실행되었습니다."
else
    echo "Python 파일 실행 중 오류가 발생했습니다."
fi