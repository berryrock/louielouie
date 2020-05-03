import os
import time
import logging

import flask

import telebot
from telebot import apihelper

import config

from modules.dbhelper import DBhelper

from modules.message_handler import message_handler
from modules.callback_handler import callback_handler

from json.decoder import JSONDecodeError

from modules import uihelper, backend
import datetime

dbhelper = DBhelper()

API_TOKEN = config.token

WEBHOOK_HOST = config.host
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = "https://{}".format(WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/{}/".format(config.page)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(API_TOKEN, threaded=False)

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
	return ''

# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
	if flask.request.headers.get('content-type') == 'application/json':
		json_string = flask.request.get_data().decode('utf-8')
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])
		return "ok", 200
	else:
		flask.abort(403)


@bot.message_handler(commands=["start"])
def cmd_start(message):
	print()
	print('start', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	uihelper.shut_down(message.chat.id)
	#uihelper.first_step(message.chat.id)



@bot.message_handler(commands=["reset"])
def cmd_reset(message):
	print()
	print('reset', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	uihelper.shut_down(message.chat.id)
	'''
	dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
	uihelper.welcome_again(message.chat.id)
	uihelper.main_menu(message.chat.id)'''



@bot.message_handler(commands=["meal"])
def cmd_meal(message):
	print()
	print('meal', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	step = dbhelper.get_step(message.chat.id)
	dbhelper.set_step(message.chat.id, config.Step.MEAL.value)
	uihelper.enter_meal(message.chat.id)



@bot.message_handler(commands=["recomendations"])
def cmd_recomendations(message):
	print()
	print('recomendations', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	step = dbhelper.get_step(message.chat.id)
	dbhelper.set_step(message.chat.id, config.Step.MEAL.value)
	uihelper.loading(message.chat.id)
	recomendations = backend.recomendations(message.chat.id)
	dbhelper.set_data(message.chat.id, config.UserData.RECOMENDATIONS.value, recomendations)
	uihelper.recomendations(message.chat.id, recomendations)



@bot.message_handler(commands=["weight"])
def cmd_weight(message):
	print()
	print('weight', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	dbhelper.set_step(message.chat.id, config.Step.WEIGHT.value)
	uihelper.add_weight(message.chat.id)



@bot.message_handler(commands=["about_you"])
def cmd_about(message):
	print()
	print('about', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	step = dbhelper.get_step(message.chat.id)[0]
	dbhelper.set_step(message.chat.id, config.Step.ABOUT.value)
	user_info = backend.user_info(message.chat.id)
	user_name = user_info.get('name', 'Empty')
	user_weight = user_info.get('weight', 'Empty')
	user_lenght = user_info.get('lenght', 'Empty')
	user_birth = user_info.get('birthday', 'Empty')
	dbhelper.set_data(message.chat.id, config.UserData.NAME.value, user_name)
	dbhelper.set_data(message.chat.id, config.UserData.WEIGHT.value, user_weight)
	dbhelper.set_data(message.chat.id, config.UserData.LENGHT.value, user_lenght)
	dbhelper.set_data(message.chat.id, config.UserData.BIRTH.value, user_birth)
	uihelper.about_user(message.chat.id, user_info)



@bot.message_handler(commands=["main_menu"])
def cmd_menu(message):
	print()
	print('main_menu', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	step = dbhelper.get_step(message.chat.id)[0]
	dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
	uihelper.main_menu(message.chat.id)



@bot.message_handler(content_types=['text'])
def answer_to_user(message):
	print()
	print('text', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	uihelper.shut_down(message.chat.id)
	'''message_handler(message, dbhelper, uihelper, backend)'''



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	print()
	print('call', call.message.chat.id)
	print(str(datetime.datetime.now()), call.data)
	uihelper.shut_down(call.message.chat.id)
	'''callback_handler(call, dbhelper, uihelper, backend)'''


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(0.1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

# Start flask server
if __name__ == '__main__':
	app.run(host=WEBHOOK_LISTEN,
		debug=True)
