import datetime
import json
import logging
import os
import pathlib
import random
import time
from tqdm import tqdm

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from opencc import OpenCC

from src.line import line_notify_message
from src.tinder import TinderAPI, RecPerson, TAIPEI_TZ
from src.utils import get_whitelist, datetime_to_json_handler
from src.utils.log_tool import create_logger

PROJECT_DIR = pathlib.Path(__file__).parent
CHAT_GPT_TOKEN_FILE_PATH = PROJECT_DIR / 'local_settings/chat_gpt_token.txt'  # from https://chat.openai.com/api/auth/session
ENV_FILE_PATH = PROJECT_DIR / 'local_settings/local.env'
load_dotenv(ENV_FILE_PATH)

# models = OpenAIModel(api_key=os.getenv('OPENAI_API'), model_engine=os.getenv('OPENAI_MODEL_ENGINE'))
# chatgpt = ChatGPT(models)
# dalle = DALLE(models)
# dialog = Dialog()

app = FastAPI()
scheduler = AsyncIOScheduler()
cc = OpenCC('s2t')
templates = Jinja2Templates(directory='templates')
TINDER_TOKEN = os.getenv('TINDER_TOKEN')
CHAT_GPT_TOKEN = open(CHAT_GPT_TOKEN_FILE_PATH).read()

PROJECT_DIR = pathlib.Path(__file__).absolute().parent
WHITELIST_PATH = PROJECT_DIR / 'whitelist.txt'
MATCH_QUERY_COUNT = 60

# JOBS IDS
JOB_GET_TINDER_API = 'get_tinder_api 🔌'
JOB_LIKE_GIRLS = 'like_girls ❤️ '
JOB_ASK_HOOK_UP = 'ask_hook_up ❓'
JOB_FIND_GIRL_REPLY_ABOUT_HOOK_UP = 'find_girl_reply_about_hook_up 👀'

LOGGERS = {
    JOB_GET_TINDER_API: create_logger(JOB_GET_TINDER_API),
    JOB_LIKE_GIRLS: create_logger(JOB_LIKE_GIRLS),
    JOB_ASK_HOOK_UP: create_logger(JOB_ASK_HOOK_UP),
    JOB_FIND_GIRL_REPLY_ABOUT_HOOK_UP: create_logger(JOB_FIND_GIRL_REPLY_ABOUT_HOOK_UP),
}


@app.on_event('shutdown')
async def shutdown():
    # scheduler.remove_job('reply_messages')
    scheduler.remove_job(JOB_LIKE_GIRLS)
    scheduler.remove_job(JOB_ASK_HOOK_UP)
    scheduler.remove_job(JOB_FIND_GIRL_REPLY_ABOUT_HOOK_UP)


def get_logger(job_id) -> logging.Logger:
    return LOGGERS[job_id]


def get_tinder_api():
    try:
        return TinderAPI(TINDER_TOKEN)
    except Exception as e:
        msg = f"Failed to login with TD api, might need to update token"
        logger = get_logger(JOB_GET_TINDER_API)
        logger.warning(f"{msg}, Error: {e}")

        line_notify_message(msg)
        msg = f"line notify sent, msg: {msg}"
        logger.critical(msg)


# @scheduler.scheduled_job("cron", minute='*/6', second=0, id='reply_messages')
# def reply_messages():
#     tinder_api = TinderAPI(TINDER_TOKEN)
#     profile = tinder_api.profile()
#
#     user_id = profile.id
#
#     whitelist = get_whitelist(WHITELIST_PATH)
#
#     for match in tinder_api.matches(limit=50):
#         girl = match.person
#         if girl.id in whitelist:
#             logger.info(f"skip girl in whitelist: {girl}")
#             continue
#
#         chatroom = tinder_api.get_messages(match.match_id)
#         lastest_message = chatroom.get_lastest_message()
#         if lastest_message:
#             if lastest_message.from_id == user_id:
#                 from_user_id = lastest_message.from_id
#                 to_user_id = lastest_message.to_id
#                 last_message = 'me'
#
#             else:
#                 from_user_id = lastest_message.to_id
#                 to_user_id = lastest_message.from_id
#                 last_message = 'other'
#
#             sent_date = lastest_message.sent_date
#
#             if last_message == 'other' or (sent_date + datetime.timedelta(days=1)) < datetime.datetime.now():
#                 content = dialog.generate_input(from_user_id, to_user_id, chatroom.messages[::-1])
#                 response = chatgpt.get_response(content)
#                 if response:
#                     response = cc.convert(response)
#                     if response.startswith('[Sender]'):
#                         chatroom.send(response[8:], from_user_id, to_user_id)
#                     else:
#                         chatroom.send(response, from_user_id, to_user_id)
#
#                 logger.info(f'Content: {content}\nReply -> {response}\nGirl:\n{girl.id} # {girl.name}\n')


@scheduler.scheduled_job('cron', minute='*/3', second=0, id=JOB_LIKE_GIRLS)
def like_girls():
    logger = get_logger(JOB_LIKE_GIRLS)
    msg = 'prepare to like girls ...'
    logger.info(msg)
    tinder_api = get_tinder_api()
    if tinder_api is None:
        msg = 'failed to like girls'
        logger.warning(msg)
        return

    remaining_likes = tinder_api.get_remaining_likes()
    if remaining_likes:
        skip_count = 0
        rec_user_ls = tinder_api.get_recommendations()
        msg = f"get {len(rec_user_ls)} recommendation user"
        logger.info(msg)
        for rec_idx, rec_user in enumerate(rec_user_ls, start=1):
            if rec_user.is_unwanted:
                swipe_left_res = rec_user.swipe_her_left()
                msg = f"({rec_idx}/{len(rec_user_ls)}) SWIPED LEFT {rec_user}, status: {swipe_left_res.get('status')}"
                logger.info(msg)
                time.sleep(random.uniform(3, 6))
            else:
                if remaining_likes > 0:
                    if rec_user.is_girl or rec_user.is_valid_so:
                        like_res = rec_user.like_her()
                        msg = f"({rec_idx}/{len(rec_user_ls)}) LIKED {rec_user}, dist: {rec_user.distance_km} km, " \
                              f"status: {like_res.get('status')}, " \
                              f"match: {like_res.get('match')}, " \
                              f"like: {like_res.get('likes_remaining')}"
                        logger.critical(msg)
                        time.sleep(random.uniform(3, 6))
                        remaining_likes = tinder_api.get_remaining_likes()
                    else:
                        msg = f"({rec_idx}/{len(rec_user_ls)}) skip {rec_user}"
                        logger.info(msg)
                        skip_count += 1
                else:
                    msg = f"({rec_idx}/{len(rec_user_ls)}) No likes left :("
                    logger.critical(msg)

        if skip_count == len(rec_user_ls):
            msg = f'skip all at first round, prepare to do second round'
            logger.info(msg)
            remaining_likes = tinder_api.get_remaining_likes()
            for rec_idx, rec_user in enumerate(rec_user_ls, start=1):
                if not rec_user.is_unwanted and remaining_likes > 0:
                    like_res = rec_user.like_her()
                    msg = f"({rec_idx}/{len(rec_user_ls)}) LIKED {rec_user}, dist: {rec_user.distance_km} km, " \
                          f"status: {like_res.get('status')}, " \
                          f"match: {like_res.get('match')}, " \
                          f"like: {like_res.get('likes_remaining')}"
                    logger.critical(msg)
                    time.sleep(random.uniform(3, 6))
                    remaining_likes = tinder_api.get_remaining_likes()

    else:
        msg = f"No likes left :("
        logger.info(msg)

    msg = 'finish liking \n'
    logger.info(msg)


@scheduler.scheduled_job('cron', minute='*/6', second=0, id=JOB_ASK_HOOK_UP)
def ask_hook_up():
    logger = get_logger(JOB_ASK_HOOK_UP)
    msg = 'prepare to ask hook up ...'
    logger.info(msg)
    tinder_api = get_tinder_api()
    if tinder_api is None:
        msg = 'failed to ask hook up'
        logger.warning(msg)
        return

    for match in tinder_api.get_matches(limit=MATCH_QUERY_COUNT):
        chatroom = tinder_api.get_chatroom(match)
        if not chatroom.has_asked_hook_up:
            tinder_api.ask_hook_up(chatroom)
            msg = f"ASKED hook up to {chatroom}\n"
            logger.critical(msg)
            time.sleep(random.uniform(6, 9))
        else:
            msg = f"Already asked for hook up: {chatroom}\n"
            logger.info(msg)

    msg = f"finish asking hook up \n"
    logger.info(msg)


# @scheduler.scheduled_job('cron', minute='*/9', second=0, id='find_girl_with_high_hook_up_intention')
# def find_girl_with_high_hook_up_intention():
#     tinder_api = TinderAPI(TINDER_TOKEN)
#     for match in tinder_api.get_matches(limit=MATCH_QUERY_COUNT):
#         chatroom = tinder_api.get_chatroom(match)
#         if chatroom.has_replied_about_hook_up and not chatroom.has_ensured_girls_reply:
#             msg = f"find replied chat room, {chatroom}"
#             print(msg)
#
#             intention = predict_hook_up_intention(chatroom.gen_hook_up_intention_inference_prompt(), CHAT_GPT_TOKEN)
#             print(f"intention = {intention}")
#
#             notify_msg = f"{chatroom.person.name} ({chatroom.person.age}) has {intention} intention, " \
#                          f"go to ensure her reply!"
#             line_notify_message(notify_msg)
#
#             msg = f"line notify sent"
#             print(msg)


@scheduler.scheduled_job('cron', minute='*/9', second=0, id='find_girl_reply_about_hook_up')
def find_girl_reply_about_hook_up():
    logger = get_logger(JOB_FIND_GIRL_REPLY_ABOUT_HOOK_UP)
    msg = 'prepare to find girl who replied about hook up ...'
    logger.info(msg)
    tinder_api = get_tinder_api()
    if tinder_api is None:
        msg = 'failed to find girl who replied about hook up'
        logger.warning(msg)
        return

    for match in tinder_api.get_matches(limit=MATCH_QUERY_COUNT):
        chatroom = tinder_api.get_chatroom(match)
        if chatroom.has_replied_about_hook_up and not chatroom.has_ensured_girls_reply:
            msg = f"find girl replied about hook up, {chatroom}"
            logger.critical(msg)

            notify_msg = f"{chatroom.person.name} ({chatroom.person.age}) has replied, go to ensure her reply!"
            line_notify_message(notify_msg)

            line_notify_message(msg)
            msg = f"line notify sent, msg: {msg}"
            logger.critical(msg)

    msg = 'finish finding girl who replied about hook up \n'
    logger.info(msg)


@app.on_event('startup')
async def startup():
    scheduler.start()


@app.get('/')
async def root():
    now = datetime.datetime.now(tz=TAIPEI_TZ)
    return {'message': f"GTBot Server is Alive! access date = {now.strftime('%Y-%m-%d %H:%M:%S')}"}


@app.get('/matches')
async def view_matches(request: Request):
    tinder_api = get_tinder_api()
    if tinder_api is None:
        return 'Failed to login with tinder api.'

    girls = list()
    for match in tinder_api.get_matches(limit=60):
        # print(match.person.infos())
        girl = match.person
        girls.append({'id': girl.id, 'name': girl.name, 'images': girl.images})

    # return pprint.pformat(json.dumps(girls), indent=4)  # works

    data = {'request': request, 'girls': girls, 'girl_count': len(girls)}
    return templates.TemplateResponse('girls.html', data)


@app.get('/recs')
async def view_recs(request: Request):
    tinder_api = get_tinder_api()
    if tinder_api is None:
        return 'Failed to login with tinder api.'

    girls = list()
    for girl in tinder_api.get_recommendations():
        girl: RecPerson
        girls.append(
            {
                'id': girl.id,
                'name': girl.name,
                'images': girl.images,
                'city': girl.city,
                'distance_km': girl.distance_km,
            }
        )

    # return pprint.pformat(json.dumps(girls), indent=4)  # works
    # msg = f"recs girls count = {len(girls)}"
    # print(msg)

    data = {'request': request, 'girls': girls, 'girl_count': len(girls)}
    return templates.TemplateResponse('recs.html', data)


@app.get('/profile')
async def view_profile(request: Request):
    tinder_api = get_tinder_api()
    if tinder_api is None:
        return 'Failed to login with tinder api.'
    profile = tinder_api.profile()
    return profile.infos()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080)
    # uvicorn.run('main:app', host='localhost', port=8080)
