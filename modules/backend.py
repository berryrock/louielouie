import config
import requests
from modules import dbhelper
import json
from modules.password import generate
from requests.auth import HTTPBasicAuth


def dish_info(user, dish):
	user_acc = dbhelper.get_data(user,"acc")
	url = config.url + config.region + "user/dish_message/"
	data = {"dish": dish}
	answer = requests.get(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	try:
		dish = answer["dish"]
		return [answer, True]
	except KeyError:
		return [answer, False]

def exact_dish(user, dish):
	user_acc = dbhelper.get_data(user,"acc")
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
	user_acc = dbhelper.get_data(user,"acc")
	url = config.url + config.users + "user/info/"
	answer = requests.get(url, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return answer


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
	user_acc = dbhelper.get_data(user,"acc")
	url = config.url + config.region + "user/preference_vector/"
	answer = requests.get(url, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return answer["dishes"]

def send_weight(user, weight):
	user_acc = dbhelper.get_data(user,"acc")
	url = config.url + config.region + "mealmap/"
	data = {"weight": weight, "accepted": True}
	answer = requests.post(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return True

def send_meal(user, dish):
	print(dish)
	user_acc = dbhelper.get_data(user,"acc")
	url = config.url + config.region + "mealmap/"
	data = {"dish": dish, "accepted": true}
	answer = requests.post(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return True

def update_info(user,type_of_data,value):
	print('updating')
	user_acc = dbhelper.get_data(user,"acc")
	url = config.url + config.users + "user/info/"
	data = {type_of_data: value}
	print(data)
	answer = requests.put(url, data=data, auth=HTTPBasicAuth(user,user_acc))
	answer = answer.json()
	print(answer)
	return answer
