import datetime
import os
import pathlib
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.tinder import TinderAPI
from src.dialog import Dialog
from src.logger import logger
from src.ult import get_whitelist
from opencc import OpenCC
from flask import render_template
import pprint
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
import uvicorn
import json

load_dotenv('.env')

models = OpenAIModel(api_key=os.getenv('OPENAI_API'), model_engine=os.getenv('OPENAI_MODEL_ENGINE'))

chatgpt = ChatGPT(models)
dalle = DALLE(models)
dialog = Dialog()
app = FastAPI()
scheduler = AsyncIOScheduler()
cc = OpenCC('s2t')
templates = Jinja2Templates(directory="templates")
TINDER_TOKEN = os.getenv('TINDER_TOKEN')
PROJECT_DIR = pathlib.Path(__file__).absolute().parent
WHITELIST_PATH = PROJECT_DIR / 'whitelist.txt'


@scheduler.scheduled_job("cron", minute='*/6', second=0, id='reply_messages')
def reply_messages():
    tinder_api = TinderAPI(TINDER_TOKEN)
    profile = tinder_api.profile()

    user_id = profile.id

    whitelist = get_whitelist(WHITELIST_PATH)

    for match in tinder_api.matches(limit=50):
        girl = match.person
        if girl.id in whitelist:
            logger.info(f"skip girl in whitelist: {girl}")
            continue

        chatroom = tinder_api.get_messages(match.match_id)
        lastest_message = chatroom.get_lastest_message()
        if lastest_message:
            if lastest_message.from_id == user_id:
                from_user_id = lastest_message.from_id
                to_user_id = lastest_message.to_id
                last_message = 'me'

            else:
                from_user_id = lastest_message.to_id
                to_user_id = lastest_message.from_id
                last_message = 'other'

            sent_date = lastest_message.sent_date

            if last_message == 'other' or (sent_date + datetime.timedelta(days=1)) < datetime.datetime.now():
                content = dialog.generate_input(from_user_id, to_user_id, chatroom.messages[::-1])
                response = chatgpt.get_response(content)
                if response:
                    response = cc.convert(response)
                    if response.startswith('[Sender]'):
                        chatroom.send(response[8:], from_user_id, to_user_id)
                    else:
                        chatroom.send(response, from_user_id, to_user_id)

                logger.info(f'Content: {content}\nReply: {response}\nGirl:\n{girl.id} # {girl.name}')


@app.on_event("startup")
async def startup():
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    scheduler.remove_job('reply_messages')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/girls")
async def view_girls():
    tinder_api = TinderAPI(TINDER_TOKEN)
    girls = []
    for match in tinder_api.matches(limit=50):
        girl = match.person
        girls.append({"id": girl.id, "name": girl.name, "images": girl.images})
    # return pprint.pformat(json.dumps(girls), indent=4)  # works
    return templates.TemplateResponse("girls.html", girls)


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8080)
