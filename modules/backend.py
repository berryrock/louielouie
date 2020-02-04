import config
import requests
from modules.dbhelper import DBhelper
import json
from modules.password import generate
from requests.auth import HTTPBasicAuth

dbhelper = DBhelper()

def dish_info(user, dish):
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.region + "user/dish_message/"
	data = {"dish": dish}
	answer = requests.get(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	try:
		dish = answer["dish"]
		"""if "No message to display" in dish["message"]:
			dish.update({"message":"Нет сообщения для показа"})
		elif "not found in database." in dish["message"]:
			dish.update({"message":"Не найдено в базе данных. Мы обязательно добавим его"})"""
		return [answer, True]
	except KeyError:
		return [answer, False]

def exact_dish(user, dish):
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.region + "user/dish_message/"
	data = {"dish": dish, "accepted": True}
	answer = requests.get(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	try:
		dish = answer["dish"]
		return [answer, True]
	except KeyError:
		return [answer, False]

def user_info(user):
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.users + "user/info/"
	answer = requests.get(url, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return answer

def user_diet(user,status):
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.users + "user/diet/"
	data = {"id": 1}
	if status == config.Step.DIET_ON.value:
		answer = requests.put(url, data=data, auth=HTTPBasicAuth(user,user_acc))
		answer = answer.json()
		print(answer)
		return True
	elif status == config.Step.DIET_OFF.value:
		answer = requests.delete(url, data=data, auth=HTTPBasicAuth(user,user_acc))
		answer = answer.json()
		print(answer)
		return True
	else:
		print(answer)
		return False

def add_user(user):
	url = config.url + config.users + "user/create/telegram/"
	password = generate()
	print(password)
	data = {"username": user, "password": password}
	answer = requests.post(url, data=data)
	answer = answer.json()
	print(answer)
	result = dbhelper.add_user(user, data["password"])
	return result


def recomendations(user):
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.region + "user/preference_vector/"
	answer = requests.get(url, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return answer["dishes"]

def send_weight(user, weight):
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.region + "mealmap/"
	data = {"weight": weight, "accepted": True}
	answer = requests.post(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return True

def send_meal(user, dish):
	print(dish)
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.region + "mealmap/"
	data = {"dish": dish, "accepted": True}
	answer = requests.post(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return True

def update_info(user,type_of_data,value):
	print('updating')
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.users + "user/info/"
	data = {type_of_data: value}
	print(data)
	answer = requests.put(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return answer

def user_settings(user):
	print('settings')
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.users + "user/info/"
	answer = requests.get(url, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	settings = {"notification": answer.get("notification",None)}
	connected_accounts = answer.get("connected_accounts", None)
	if connected_accounts:
		for account in connected_accounts:
			if account['name'] == "Gmail":
				settings.update({"gmail_account": True})
			elif ccount['name'] == "WiThings":
				settings.update({"withings": True})
	return settings

def notifications_turn(user, status):
	if status == config.Step.NOTIFICATION_ON.value:
		data = {"notification": True}
	else:
		data = {"notification": False}
	user_acc = dbhelper.get_data(user,"acc")[0]
	url = config.url + config.users + "user/info/"
	answer = requests.put(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return answer

def clear_gmail(user):
	user_acc = dbhelper.get_data(user,"acc")[0]
	url_info = config.url + config.users + "user/info/"
	answer = requests.get(url_info, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	connected_accounts = answer.get('connected_accounts', None)
	if connected_accounts:
		connected_accounts.remove(config.GMAIL_SERVICE)
		url = config.url + config.users + "user/connected_service/"
		data = {"connected_accounts": connected_accounts}
		answer = requests.put(url, data=data, auth=HTTPBasicAuth(user,user_acc))
		answer = answer.json()
		print(answer)
		settings = {"notification": answer.get("notification",None)}
		connected_accounts = answer.get("connected_accounts", None)
		for account in connected_accounts:
			if account['name'] == "Gmail":
				settings.update({"gmail_account": True})
			elif ccount['name'] == "WiThings":
				settings.update({"withings": True})
	return answer
