FROM python:3.9-slim

COPY ./ /DiscordBot
WORKDIR /DiscordBot

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata

RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
