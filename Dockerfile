FROM python:3.9-alpine

COPY ./ /DiscordBot
WORKDIR /DiscordBot

RUN apk add --no-cache tzdata
ENV TZ=Asia/Taipei

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
