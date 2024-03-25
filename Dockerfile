FROM python:3.12-slim
# pip install packages
WORKDIR /app

# cron 패키지 설치
RUN apt-get update && apt-get -y install cron

COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
# copy script to docker path
COPY *.py ./

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab

# excute command
# simple_request의 표준출력과 에러를 위에서 만든 로그 파일로 리다이렉트
# CMD python3 -u ./main.py
CMD ["cron" , "-f"]