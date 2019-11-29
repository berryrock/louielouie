import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token)


def meal_info(chat, dish_info):
	inline_keyboard = types.InlineKeyboardMarkup()
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	add_button = types.InlineKeyboardButton(text="Add meal", callback_data=config.Step.MEAL_ADD.value)
	again_button = types.InlineKeyboardButton(text="Try another", callback_data=config.Step.MEAL.value)
	inline_keyboard.add(add_button,again_button)
	try:
		links = dish_info['links']
		for link in links:
			link_url = link['url'] + link['utm_tag']
			link_button = types.InlineKeyboardButton(text=link['service'], url=link['url'])
			inline_keyboard.add(link_button)
	except KeyError:
		pass
	menu_button = '/main_menu'
	reply_keyboard.add(menu_button)
	message = '{}\n\n{}'.format(dish_info['dish'],dish_info['message'])
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text='Add this dish as a meal or try another', reply_markup=reply_keyboard)

def loading(chat):
	message = "Updating, please wait..."
	bot.send_message(chat, message)

def choose_dish_from_list(chat,dish_list):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	for dish in dish_list:
		reply_keyboard.add(dish)
	message = 'I found too much similar dishes.\nChoose one from the list'
	bot.send_message(chat, message, reply_markup=reply_keyboard)

def dish_entered_correct(chat,dish):
	inline_keyboard = types.InlineKeyboardMarkup()
	exact_button = types.InlineKeyboardButton(text="No, I exactly mean that dish", callback_data=config.Step.MEAL_EXACT.value)
	inline_keyboard.add(exact_button)
	message = 'You entered dish {}'.format(dish)
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def meal_added(chat):
	message = 'Your meal added'
	bot.send_message(chat, message)

def enter_meal(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text="<- Back to main menu  ", callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = 'Please, enter dish that plan to eat or already ate'
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def main_menu(chat):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	buttons = ['/meal','/recomendations','/weight','/about_you']
	for button in buttons:
		reply_keyboard.add(button)
	message = 'You are in a main menu'
	bot.send_message(chat, message, reply_markup=reply_keyboard)

def add_weight(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text="<- Back to main menu  ", callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = 'Please, enter your weight'
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def	weight_added(chat):
	message = 'Your weight added'
	bot.send_message(chat, message)

def about_user(chat,user_info):
	inline_keyboard = types.InlineKeyboardMarkup()
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	name_button = types.InlineKeyboardButton(text="Edit name", callback_data=config.Step.ABOUT_NAME.value)
	birth_button = types.InlineKeyboardButton(text="Edit birthday", callback_data=config.Step.ABOUT_BIRTH.value)
	weight_button = types.InlineKeyboardButton(text="Edit weight", callback_data=config.Step.ABOUT_WEIGHT.value)
	lenght_button = types.InlineKeyboardButton(text="Edit lenght", callback_data=config.Step.ABOUT_LENGHT.value)
	inline_keyboard.add(name_button, birth_button)
	inline_keyboard.add(weight_button, lenght_button)
	menu_button = '/main_menu'
	reply_keyboard.add(menu_button)
	message = """Name: {}\nBirthday: {}\nWeight: {}\nLenght: {}\n""".format(user_info.get('name', 'Empty'),user_info.get('birthday', 'Empty'),user_info.get('weight', 'Empty'),user_info.get('lenght', 'Empty'))
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text='More information you add, more personalised recomendations will be', reply_markup=reply_keyboard)

def recomendations(chat,recomendations):
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	if recomendations == '':
		menu_button = '/main_menu'
		reply_keyboard.add(menu_button)
		message = 'Looks like you already eat too much for today. Take a break and drink water'
	else:
		dish_list = recomendations.split(';')
		n = 0
		for dish in dish_list:
			reply_keyboard.add(dish)
			n += 1
			if n == 6:
				break
		menu_button = '/main_menu'
		reply_keyboard.add(menu_button)
		message = 'Here is recomended dishes for you.\nChoose one from the list or add yours'
	bot.send_message(chat, message, reply_markup=reply_keyboard)

def edit_personal(chat, type_of_info):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text="<- Back to main menu  ", callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = 'Please, enter new {}'.format(type_of_info)
	bot.send_message(chat, message, reply_markup=inline_keyboard)

def wrong_data_format(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text="<- Back to main menu  ", callback_data=config.Step.MAIN_MENU.value)
	inline_keyboard.add(menu_button)
	message = 'Wrong format of data\nPlease enter your birthday like 14.11.2019'
	bot.send_message(chat, message, reply_markup=inline_keyboard)


def updated_user(chat, type_of_info):
	message = 'Your {} updated'.format(type_of_info)
	bot.send_message(chat, message)

def first_step(chat):
	inline_keyboard = types.InlineKeyboardMarkup()
	policy_button = add_button = types.InlineKeyboardButton(text="Private Policy", url='http://www.mealmapp.ru/')
	inline_keyboard.add(policy_button)
	reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	accept_button = 'I accept private policy'
	reply_keyboard.add(accept_button)
	message = '''Hi!\nI'm Louie-Louie personal nutrition assistant.\nI was developed by @berryrock to demostrate possibilities of Mealmapp, food management platform.'''
	bot.send_message(chat, message, reply_markup=inline_keyboard)
	bot.send_message(chat, text='Please accept Private Policy to continue', reply_markup=reply_keyboard)

def welcome_message(chat):
	message = 'Thank you for interest for the project. Hope your enjoy it'
	bot.send_message(chat, message)

def welcome_again(chat):
	message = '''Hi!\nI'm Louie-Louie personal nutrition assistant.\nI was developed by @berryrock to demostrate possibilities of Mealmapp, food management platform.\n\nI already know you so I saved all your previous data'''
	bot.send_message(chat, message)

def spamming(chat):
	message = "Looks like you are spamming. Just don't"
	bot.send_message(chat, message)

def error_message(chat):
	message = 'Something went wrong.\nTry again later or write your problem to @berryrock'
	bot.send_message(chat, message)
