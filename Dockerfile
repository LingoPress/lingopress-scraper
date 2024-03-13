FROM python:3.12-slim
# pip install packages
WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
# copy script to docker path
COPY *.py ./

# create the log file
# host의 tmp와 볼륨을 공유할 거기 때문에 tmp에 log 파일을 만들어 둡니다.
RUN touch /scraping.log
# excute command
# simple_request의 표준출력과 에러를 위에서 만든 로그 파일로 리다이렉트
CMD python3 -u ./main.py