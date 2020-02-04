import telebot
from telebot import types
from modules.messages import translation
import config

bot = telebot.TeleBot(config.token)


def meal_info(chat, dish_info):
	inline_keyboard = types.InlineKeyboardMarkup()
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	add_button = types.InlineKeyboardButton(text=translation["rus"].button_add_meal, callback_data=config.Step.MEAL_ADD.value)
	again_button = types.InlineKeyboardButton(text=translation["rus"].button_try_another, callback_data=config.Step.MEAL.value)
	inline_keyboard.add(add_button,again_button)
	try:
		links = dish_info['links']
		for link in links:
			link_url = link['url'] + link['utm_tag']
			link_button = types.InlineKeyboardButton(text=link['service'], url=link['url'])
			inline_keyboard.add(link_button)
	except KeyError:
		pass
	menu_button = config.Menu_RU.MAIN_MENU.value
	reply_keyboard.add(menu_button)
	message = '{}\n\n{}'.format(dish_info['dish'],dish_info['message'])
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text=translation["rus"].text_meal_info, reply_markup=reply_keyboard)

def loading(chat):
	message = translation["rus"].text_loading
	bot.send_message(chat, message)

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

def main_menu(chat):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	buttons = [config.Menu_RU.MEAL.value,config.Menu_RU.RECOMENDATIONS.value,config.Menu_RU.WEIGHT.value,config.Menu_RU.ABOUT.value,config.Menu_RU.SETTINGS.value]
	for button in buttons:
		reply_keyboard.add(button)
	message = translation["rus"].text_main_menu
	bot.send_message(chat, message, reply_markup=reply_keyboard)

def add_weight(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_back_main_menu, callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = translation["rus"].text_enter_weight
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def	weight_added(chat):
	message = translation["rus"].text_weight_added
	bot.send_message(chat, message)

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
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text=translation["rus"].text_more_inforamtion_add, reply_markup=reply_keyboard)

def diet_on(chat):
	message = translation["rus"].text_diet_on
	bot.send_message(chat, message)

def diet_off(chat):
	message = translation["rus"].text_diet_off
	bot.send_message(chat, message)

def recomendations(chat,recomendations):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	if recomendations == '':
		menu_button = config.Menu_RU.MAIN_MENU.value
		reply_keyboard.add(menu_button)
		message = translation["rus"].text_eat_too_much
	else:
		dish_list = recomendations.split(';')
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

def settings(chat, settings):
	inline_keyboard = types.InlineKeyboardMarkup()
	if settings["notification"]:
		notification_button = types.InlineKeyboardButton(text=translation["rus"].button_notication_off, callback_data=config.Step.NOTIFICATION_OFF.value)
	else:
		notification_button = types.InlineKeyboardButton(text=translation["rus"].button_notication_on, callback_data=config.Step.NOTIFICATION_ON.value)
	inline_keyboard.add(notification_button)
	message = translation["rus"].text_settings
	if settings["gmail_account"]:
		gmail_button = types.InlineKeyboardButton(text=translation["rus"].button_gmail_off, callback_data=config.Step.GMAIL_OFF.value)
	else:
		gmail_button = types.InlineKeyboardButton(text=translation["rus"].button_gmail_on, url=config.google_connect_url.format(chat))
		message = message + "\n\n" + translation["rus"].text_connect_gmail
	inline_keyboard.add(gmail_button)
	menu_button = types.InlineKeyboardButton(text=translation["rus"].button_back_main_menu, callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def notification_update(chat):
	message = translation["rus"].text_notification_update
	bot.send_message(chat, message)

def gmail_update(chat):
	message = translation["rus"].text_gmail_update
	bot.send_message(chat, message)

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

def spamming(chat):
	message = translation["rus"].text_spamming
	bot.send_message(chat, message)

def error_message(chat):
	message = translation["rus"].text_error
	bot.send_message(chat, message)
