import telebot
from telebot import types
from modules.messages import translation
import config

import datetime

bot = telebot.TeleBot(config.token)

''' MEAL, MEAL_ADD and MEAL_INFO'''
def meal_info(chat, dish_info):
	inline_keyboard = types.InlineKeyboardMarkup()
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	add_button = types.InlineKeyboardButton(text=translation["rus"].button_add_meal, callback_data=config.Step.MEAL_ADD.value)
	again_button = types.InlineKeyboardButton(text=translation["rus"].button_try_another, callback_data=config.Step.MEAL.value)
	inline_keyboard.add(add_button,again_button)
	try:
		links = dish_info['links']
		for link in list(links):
			link_url = link['url'] + '?' + link['utm_tag']
			link_button = types.InlineKeyboardButton(text=link['service']['cta_word'], url=link_url)
			inline_keyboard.add(link_button)
	except KeyError:
		pass
	menu_button = config.Menu_RU.MAIN_MENU.value
	reply_keyboard.add(menu_button)
	message = '{}\n\n{}'.format(dish_info['dish'],dish_info['message'])
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text=translation["rus"].text_meal_info, reply_markup=reply_keyboard)

def choose_dish_from_list(chat,dish_list):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	for dish in dish_list:
		reply_keyboard.add(dish)
	message = translation["rus"].text_too_much_similar
	bot.send_message(chat, message, reply_markup=reply_keyboard)

def dish_entered_correct(chat,dish):
	inline_keyboard = types.InlineKeyboardMarkup()
	exact_button = types.InlineKeyboardButton(text=translation["rus"].button_exact_dish, callback_data=config.Step.MEAL_EXACT.value)
	inline_keyboard.add(exact_button)
	message = translation["rus"].text_entered_dish.format(dish)
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def meal_added(chat):
	message = translation["rus"].text_meal_added
	bot.send_message(chat, message)

def enter_meal(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_back_main_menu, callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = translation["rus"].text_enter_dish
	bot.send_message(chat, message, reply_markup=inline_keyboard)



'''
MAIN_MENU
'''
def main_menu(chat, diets=None, kcal_consumpted=None, kcal_daily=None):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	buttons = [config.Menu_RU.MEAL.value,config.Menu_RU.RECOMENDATIONS.value,config.Menu_RU.WEIGHT.value,config.Menu_RU.ABOUT.value,config.Menu_RU.SETTINGS.value]
	for button in buttons:
		reply_keyboard.add(button)
	message = translation["rus"].text_main_menu
	if diets:
		message += '\n\n' + translation["rus"].text_daily_diets
		n = 0
		for diet in diets:
			n += 1
			message += ' {}'.format(diet["name"])
			if n < (len(diets)):
				message += ','
	if kcal_consumpted and kcal_daily:
		message += '\n\n' + translation["rus"].text_daily_kcal.format(kcal_consumpted, kcal_daily)
	bot.send_message(chat, message, reply_markup=reply_keyboard)

def spamming(chat):
	message = translation["rus"].text_spamming
	bot.send_message(chat, message)

def error_message(chat):
	message = translation["rus"].text_error
	bot.send_message(chat, message)

def alleged_message(chat):
	message = translation["rus"].text_alleged
	bot.send_message(chat, message)

def alleged(chat, item):
	inline_keyboard = types.InlineKeyboardMarkup()
	accept_button = types.InlineKeyboardButton(text=translation["rus"].button_alleged_accept, callback_data=(config.Step.ALLEGED_ACCEPT.value + str(item["id"])))
	decline_button = types.InlineKeyboardButton(text=translation["rus"].button_alleged_decline, callback_data=(config.Step.ALLEGED_DECLINE.value + str(item["id"])))
	inline_keyboard.add(accept_button,decline_button)
	date_time = item.get("date_time", None)
	if date_time:
		date_time = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%f%z').strftime('%d-%m-%Y, %H:%M:%S')
	else:
		date_time = 'unknown'
	message = translation["rus"].text_alleged_meal.format(item["dish"]["name"],date_time)
	try:
		message += translation["rus"].text_alleged_source.format(item["source"])
	except KeyError:
		pass
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def alleged_accept(chat):
	message = translation["rus"].text_alleged_accept
	bot.send_message(chat, message)

def alleged_decline(chat):
	message = translation["rus"].text_alleged_decline
	bot.send_message(chat, message)


'''
WEIGHT_ADD
'''
def add_weight(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_back_main_menu, callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = translation["rus"].text_enter_weight
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def	weight_added(chat):
	message = translation["rus"].text_weight_added
	bot.send_message(chat, message)



'''
USER_INFO
'''
def about_user(chat,user_info):
	inline_keyboard = types.InlineKeyboardMarkup()
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	name_button = types.InlineKeyboardButton(text=translation["rus"].button_edit_name, callback_data=config.Step.ABOUT_NAME.value)
	birth_button = types.InlineKeyboardButton(text=translation["rus"].button_edit_birthday, callback_data=config.Step.ABOUT_BIRTH.value)
	weight_button = types.InlineKeyboardButton(text=translation["rus"].button_edit_weight, callback_data=config.Step.ABOUT_WEIGHT.value)
	lenght_button = types.InlineKeyboardButton(text=translation["rus"].button_edit_lenght, callback_data=config.Step.ABOUT_LENGHT.value)
	inline_keyboard.add(name_button, birth_button)
	inline_keyboard.add(weight_button, lenght_button)
	menu_button = config.Menu_RU.MAIN_MENU.value
	reply_keyboard.add(menu_button)
	user_diets = user_info.get('diets', None)
	if len(user_diets) < 1:
		message = translation["rus"].text_about_user.format(user_info.get('name', 'Empty'),user_info.get('birthday', 'Empty'),user_info.get('weight', 'Empty'),user_info.get('lenght', 'Empty'))
		diet_button = types.InlineKeyboardButton(text=translation["rus"].button_turn_on_diet, callback_data=config.Step.DIET_ON.value)
	else:
		message = translation["rus"].text_about_user.format(user_info.get('name', 'Empty'),user_info.get('birthday', 'Empty'),user_info.get('weight', 'Empty'),user_info.get('lenght', 'Empty'))
		diet_button = types.InlineKeyboardButton(text=translation["rus"].button_turn_off_diet, callback_data=config.Step.DIET_OFF.value)
	inline_keyboard.add(diet_button)
	mealhistory_button = types.InlineKeyboardButton(text=translation["rus"].button_meal_history, callback_data=config.Step.MEAL_HISTORY.value)
	inline_keyboard.add(mealhistory_button)
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text=translation["rus"].text_more_inforamtion_add, reply_markup=reply_keyboard)

def diet_on(chat):
	message = translation["rus"].text_diet_on
	bot.send_message(chat, message)

def diet_off(chat):
	message = translation["rus"].text_diet_off
	bot.send_message(chat, message)

def edit_personal(chat, type_of_info):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_back_main_menu, callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = translation["rus"].text_enter_info.format(translation["rus"].edit_personal.get(type_of_info,""))
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def wrong_data_format(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_back_main_menu, callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = translation["rus"].text_wrong_birthday_format
	bot.send_message(chat, message, reply_markup=inline_keyboard)


def updated_user(chat, type_of_info):
	message = translation["rus"].text_updated_info.format(translation["rus"].edit_personal.get(type_of_info,""))
	bot.send_message(chat, message)


def meal_in_histroy(chat, meal):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_meal_history_delete, callback_data=(config.Step.MEAL_HISTORY_DELETE.value + str(meal['id'])))
	inline_keyboard.add(delete_button)
	message = translation["rus"].text_meal_in_histroy
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def meal_deleted(chat):
	message = translation["rus"].text_meal_deleted
	bot.send_message(chat, message)

def history_navigation(chat, days):
	inline_keyboard = types.InlineKeyboardMarkup()
	forward_button = types.InlineKeyboardButton(text=translation["rus"].button_meal_history_forward, callback_data=(config.Step.MEAL_HISTORY_FORWARD.value + str(days + 7)))
	if days > 7:
		back_button = types.InlineKeyboardButton(text=translation["rus"].button_meal_history_back, callback_data=(config.Step.MEAL_HISTORY_BACK.value + str(days - 7)))
		inline_keyboard.add(back_button,forward_button)
	else:
		inline_keyboard.add(forward_button)
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_back_main_menu, callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = translation["rus"].text_meal_history_navigation
	bot.send_message(chat, message, reply_markup=inline_keyboard)


'''
RECOMENDATION
'''
def recomendations(chat,recomendations):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	if recomendations == '':
		menu_button = config.Menu_RU.MAIN_MENU.value
		reply_keyboard.add(menu_button)
		message = translation["rus"].text_eat_too_much
	else:
		dish_list = recomendations.split(';')
		dish_list.reverse()
		n = 0
		for dish in dish_list:
			reply_keyboard.add(dish)
			n += 1
			if n == 6:
				break
		menu_button = config.Menu_RU.MAIN_MENU.value
		reply_keyboard.add(menu_button)
		message = translation["rus"].text_recomended_dishes
	bot.send_message(chat, message, reply_markup=reply_keyboard)

def loading(chat):
	message = translation["rus"].text_loading
	bot.send_message(chat, message)




'''
SETTINGS
'''
def settings(chat, settings):
	inline_keyboard = types.InlineKeyboardMarkup()
	notification = settings.get("notification", None)
	if notification:
		notification_button = types.InlineKeyboardButton(text=translation["rus"].button_notication_off, callback_data=config.Step.NOTIFICATION_OFF.value)
	else:
		notification_button = types.InlineKeyboardButton(text=translation["rus"].button_notication_on, callback_data=config.Step.NOTIFICATION_ON.value)
	inline_keyboard.add(notification_button)
	message = translation["rus"].text_settings
	gmail_account = settings.get("gmail_account", None)
	if gmail_account:
		gmail_button = types.InlineKeyboardButton(text=translation["rus"].button_gmail_off, callback_data=config.Step.GMAIL_OFF.value)
	else:
		gmail_button = types.InlineKeyboardButton(text=translation["rus"].button_gmail_on, url=config.google_connect_url.format(chat))
		message = message + "\n\n" + translation["rus"].text_connect_gmail
	inline_keyboard.add(gmail_button)
	withings_account = settings.get("withings", None)
	if withings_account:
		withings_button = types.InlineKeyboardButton(text=translation["rus"].button_withings_off, callback_data=config.Step.WITHINGS_OFF.value)
	else:
		withings_button = types.InlineKeyboardButton(text=translation["rus"].button_withings_on, url=config.withings_connect_url.format(chat))
		message = message + "\n\n" + translation["rus"].text_connect_withings
	inline_keyboard.add(withings_button)
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	message_two = translation["rus"].text_connected_services
	menu_button = config.Menu_RU.MAIN_MENU.value
	reply_keyboard.add(menu_button)
	bot.send_message(chat, message_two, reply_markup=reply_keyboard)

def notification_update(chat):
	message = translation["rus"].text_notification_update
	bot.send_message(chat, message)

def gmail_update(chat):
	message = translation["rus"].text_gmail_update
	bot.send_message(chat, message)

def withings_update(chat):
	message = translation["rus"].text_withings_update
	bot.send_message(chat, message)



'''
START'''
def first_step(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	policy_button = types.InlineKeyboardButton(text=translation["rus"].button_private_policy, url='http://www.mealmapp.ru/private-policy/')
	inline_keyboard.add(policy_button)
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	accept_button = translation["rus"].button_accept_policy
	reply_keyboard.add(accept_button)
	message = translation["rus"].text_hello
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text=translation["rus"].text_accept_policy, reply_markup=reply_keyboard)

def welcome_message(chat):
	message = translation["rus"].text_welcome
	bot.send_message(chat, message)

def welcome_again(chat):
	message = translation["rus"].text_welcome
	bot.send_message(chat, message)
