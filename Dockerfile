FROM python:3.12-slim
# pip install packages
WORKDIR /app

# cron 패키지 설치
RUN apt-get update && apt-get -y install cron && apt-get -y install dos2unix

COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
# copy script to docker path
COPY *.py ./

ENV TZ=Asia/Seoul

# 파일 복사
COPY crontab /etc/cron.d/crontab
# 개행 타입 변환
RUN dos2unix /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab

# crontab 등록
RUN crontab /etc/cron.d/crontab

# excute command
CMD ["/bin/bash", "-c", "printenv > /etc/environment && cron -f"]