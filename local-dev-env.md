# Environment

### Create conda env
```shell
conda create -y --name=gtbot python=3.9
```

### Remove conda env
```shell
conda env remove -y --name gtbot
```

### add jupyter kernel
```shell
conda activate gtbot
pip install ipykernel
python -m ipykernel install --user --name gtbot --display-name "GTBot"
```

### remove jupyter kernel
```shell
jupyter kernelspec uninstall -y gtbot
```

### python:3.9-alpine
```dockerfile
FROM python:3.9-alpine

COPY ./ /DiscordBot
WORKDIR /DiscordBot

RUN apk add --no-cache tzdata
ENV TZ=Asia/Taipei

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
```
