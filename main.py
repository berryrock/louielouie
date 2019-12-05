import os
import time
import logging

import flask

import telebot
from telebot import apihelper

import config

from modules.dbhelper import DBhelper

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

from json.decoder import JSONDecodeError

from modules import uihelper, backend
import datetime

@bot.message_handler(commands=["start"])
def cmd_start(message):
	print()
	print('start', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	uihelper.first_step(message.chat.id)



@bot.message_handler(commands=["reset"])
def cmd_reset(message):
	print()
	print('reset', message.chat.id)
	print(str(datetime.datetime.now()), message.text)
	dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
	uihelper.welcome_again(message.chat.id)
	uihelper.main_menu(message.chat.id)



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
	step = dbhelper.get_step(message.chat.id)[0]
	dbhelper.clear_call(message.chat.id)
	try:
		if message.text == config.Step.START_ACCEPT.value:
			backend.add_user(message.chat.id)
			uihelper.welcome_message(message.chat.id)
			uihelper.main_menu(message.chat.id)

		elif step == config.Step.MAIN_MENU.value:
			if message.text == "test_user_data":
				dbhelper.print_user_data(message.chat.id)
			else:
				dish_info = backend.dish_info(message.chat.id, message.text)
				dbhelper.set_data(message.chat.id, config.UserData.DISH.value, message.text)
				if dish_info[1] == True:
					dbhelper.set_step(message.chat.id, config.Step.MEAL_INFO.value)
					uihelper.meal_info(message.chat.id, dish_info[0])

				elif dish_info[1] == False:
					similar_dishes = dish_info[0]['similar_dishes'].split(';')
					uihelper.choose_dish_from_list(message.chat.id, similar_dishes)
					uihelper.dish_entered_correct(message.chat.id, message.text)

		elif step == config.Step.ABOUT.value:
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

		elif step == config.Step.ABOUT_NAME.value:
			user_info = backend.update_info(message.chat.id, 'name', message.text)
			dbhelper.set_data(message.chat.id, config.UserData.NAME.value, message.text)
			uihelper.updated_user(message.chat.id, 'name')
			uihelper.about_user(message.chat.id, user_info)

		elif step == config.Step.ABOUT_LENGHT.value:
			user_info = backend.update_info(message.chat.id, 'lenght', message.text)
			dbhelper.set_data(message.chat.id, config.UserData.LENGHT.value, message.text)
			uihelper.updated_user(message.chat.id, 'lenght')
			uihelper.about_user(message.chat.id, user_info)

		elif step == config.Step.ABOUT_BIRTH.value:
			try:
				birthday = message.text.split('.')
				birthday = "{}-{}-{}".format(birthday[2],birthday[1],birthday[0])
				user_info = backend.update_info(message.chat.id, 'birthday', birthday)
				dbhelper.set_data(message.chat.id, config.UserData.BIRTH.value, birthday)
				uihelper.updated_user(message.chat.id, 'birthday')
				uihelper.about_user(message.chat.id, user_info)
			except IndexError:
				uihelper.wrong_data_format(message.chat.id)

		elif step == config.Step.ABOUT_WEIGHT.value:
			backend.send_weight(message.chat.id, message.text)
			user_info = backend.user_info(message.chat.id)
			dbhelper.set_data(message.chat.id, config.UserData.WEIGHT.value, user_info.get('name','Empty'))
			uihelper.updated_user(message.chat.id, 'weight')
			uihelper.about_user(message.chat.id, user_info)

		elif step == config.Step.WEIGHT.value:
			dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
			#dbhelper.set_data(message.chat.id, config.UserData.WEIGHT.value, message.text)
			backend.send_weight(message.chat.id, message.text)
			uihelper.weight_added(message.chat.id)
			uihelper.main_menu(message.chat.id)

		elif step == config.Step.MEAL.value:
			dish_info = backend.dish_info(message.chat.id, message.text)
			if dish_info[1] == True:
				print(dish_info)
				dbhelper.set_step(message.chat.id, config.Step.MEAL_INFO.value)
				dbhelper.set_data(message.chat.id, config.UserData.DISH.value, dish_info[0]["dish"])
				uihelper.meal_info(message.chat.id, dish_info[0])

			elif dish_info[1] == False:
				similar_dishes = dish_info[0]['similar_dishes'].split(';')
				dbhelper.set_data(message.chat.id, config.UserData.DISH.value, message.text)
				dbhelper.set_step(message.chat.id, config.Step.MEAL.value)
				uihelper.choose_dish_from_list(message.chat.id, similar_dishes)
				uihelper.dish_entered_correct(message.chat.id, message.text)

		elif step == config.Step.START_LOG.value:
			dbhelper.add_user(message.chat.id, message.text)

	except KeyError:
		dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
		uihelper.error_message(message.chat.id)
		uihelper.main_menu(message.chat.id)

	except JSONDecodeError:
		dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
		uihelper.error_message(message.chat.id)
		uihelper.main_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	print()
	print('call', call.message.chat.id)
	print(str(datetime.datetime.now()), call.data)
	step = dbhelper.get_step(call.message.chat.id)[0]
	print(str(datetime.datetime.now()), step)
	previous_calls = dbhelper.get_call(call.message.chat.id)
	print('previous calls', previous_calls)
	if len(previous_calls) < 3:
		previous_calls.append(None)
		previous_calls.append(None)
	if call.data == previous_calls[0] and call.data == previous_calls[1] and call.data == previous_calls[2]:
		print(call.message.chat.id, 'spamming')
		pass
	elif call.data == previous_calls[0] and call.data == previous_calls[1]:
		dbhelper.set_call(call.message.chat.id, call.data)
		uihelper.spamming(call.message.chat.id)
	else:
		dbhelper.set_call(call.message.chat.id, call.data)
		try:
			if call.data == config.Step.MEAL_ADD.value:
				if step == config.Step.MEAL_INFO.value:
					dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
					data = dbhelper.get_data(call.message.chat.id, config.UserData.DISH.value)[0]
					print(data)
					try:
						dish = data['dish']
					except TypeError:
						dish = data
					backend.send_meal(call.message.chat.id, dish)
					uihelper.meal_added(call.message.chat.id)
					uihelper.main_menu(call.message.chat.id)

			elif call.data == config.Step.MEAL.value:
				dbhelper.set_step(call.message.chat.id, config.Step.MEAL.value)
				uihelper.enter_meal(call.message.chat.id)

			elif call.data == config.Step.MEAL_EXACT.value:
				dbhelper.set_step(call.message.chat.id, config.Step.MEAL_INFO.value)
				dish_data = dbhelper.get_data(call.message.chat.id, config.UserData.DISH.value)[0]
				dish_info = backend.exact_dish(call.message.chat.id, dish_data)
				uihelper.meal_info(call.message.chat.id, dish_info[0])

			elif call.data[:4] == 'rec_':
				recomended_dishes = dbhelper.get_data(call.message.chat.id, config.UserData.RECOMENDATIONS.value)[0]
				recomended_dishes = recomended_dishes.split(';')
				dish = recomended_dishes[int(call.data[4]) - 1]
				dish_info = backend.dish_info(call.message.chat.id, dish)
				dbhelper.set_data(call.message.chat.id, config.UserData.DISH.value, call.message.text)
				if dish_info[1] == True:
					dbhelper.set_step(call.message.chat.id, config.Step.MEAL_INFO.value)
					uihelper.meal_info(call.message.chat.id, dish_info[0])

				elif dish_info[1] == False:
					similar_dishes = dish_info[0]['similar_dishes'].split(';')
					uihelper.choose_dish_from_list(call.message.chat.id, similar_dishes)
					uihelper.dish_entered_correct(call.message.chat.id, call.message.text)

			elif call.data == config.Step.RECOMENDATIONS_REFRESH.value:
				dbhelper.set_step(call.message.chat.id, config.Step.MEAL.value)
				recomendations = backend.recomendations(message.chat.id)
				dbhelper.set_data(call.message.chat.id, config.UserData.RECOMENDATIONS.value, recomendations)
				uihelper.recomendations(call.message.chat.id)

			elif call.data == config.Step.MAIN_MENU.value:
				dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
				uihelper.main_menu(call.message.chat.id)

			elif call.data == config.Step.ABOUT_NAME.value:
				dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_NAME.value)
				uihelper.edit_personal(call.message.chat.id, 'name')

			elif call.data == config.Step.ABOUT_LENGHT.value:
				dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_LENGHT.value)
				uihelper.edit_personal(call.message.chat.id, 'lenght')

			elif call.data == config.Step.ABOUT_WEIGHT.value:
				dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_WEIGHT.value)
				uihelper.edit_personal(call.message.chat.id, 'weight')

			elif call.data == config.Step.ABOUT_BIRTH.value:
				dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_BIRTH.value)
				uihelper.edit_personal(call.message.chat.id, 'birth')

			elif call.data == config.Step.DIET_ON.value:
				dbhelper.set_step(call.message.chat.id, config.Step.ABOUT.value)
				uihelper.diet_on(message.chat.id)
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

			elif call.data == config.Step.DIET_OFF.value:
				dbhelper.set_step(call.message.chat.id, config.Step.ABOUT.value)
				uihelper.diet_off(message.chat.id)
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

			else:
				dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
				uihelper.error_message(call.message.chat.id)
				uihelper.main_menu(call.message.chat.id)

		except JSONDecodeError:
			dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
			uihelper.error_message(call.message.chat.id)
			uihelper.main_menu(call.message.chat.id)



# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(0.1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

# Start flask server
if __name__ == '__main__':
	app.run(host=WEBHOOK_LISTEN,
		debug=True)
