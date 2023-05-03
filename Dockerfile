FROM python:3.9-alpine

COPY ./ /DiscordBot
WORKDIR /DiscordBot

RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime \
    && echo "Asia/Taipei" > /etc/timezone \
    && apk del tzdata

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
