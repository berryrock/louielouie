from vedis import Vedis
import config
import json
import ast

def add_user(user_id, value):
	with Vedis(config.db_file) as db:
		try:
			try:
				user_data = db[user_id].decode()
				print("{} already in database".format(user_id))
			except:
				db[user_id] = {"acc": value}
			return True
		except:
			# тут желательно как-то обработать ситуацию
			print("Can't add user {}".format(user_id))
			return False

def print_user_data(user_id):
	with Vedis(config.db_file) as db:
		try:
			user_data = db[user_id].decode()
			print(user_data)
		except:
			print('Error with {} data'.format(user_id))


def set_step(user_id, value):
	with Vedis(config.db_file) as db:
		try:
			data = db[user_id].decode()
			#print('44444', data)
			data = data.replace("""'""",'''"''')
			data = ast.literal_eval(data)
			data.update({config.UserData.STEP.value: value})
			db[user_id] = data
			print("{} Step added".format(value))
			return True
		except:
			# тут желательно как-то обработать ситуацию
			print("Can't add step for user {}".format(user_id))
			return False

def set_call(user_id, value):
	with Vedis(config.db_file) as db:
		try:
			data = db[user_id].decode()
			#print('44444', data)
			data = data.replace("""'""",'''"''')
			data = ast.literal_eval(data)
			previous_call = data.get(config.UserData.CALL.value, None)
			previous_previous_call = data.get(config.UserData.PREVIOUS_CALL.value, None)
			data.update({config.UserData.CALL.value: value, config.UserData.PREVIOUS_CALL.value: previous_call, config.UserData.PREVIOUS_PREVIOUS_CALL.value: previous_previous_call})
			db[user_id] = data
			print("{} Call added".format(value))
			return True
		except:
			# тут желательно как-то обработать ситуацию
			print("Can't add CALL for user {}".format(user_id))
			return False

def get_step(user_id):
	with Vedis(config.db_file) as db:
		try:
			user_data = db[user_id].decode()
			#print('11111', user_data)
			user_data = user_data.replace("""'""",'''"''')
			user_data = ast.literal_eval(user_data)
			db[user_id] = user_data
			print("{} Step getted".format(user_data[config.UserData.STEP.value]))
			return user_data[config.UserData.STEP.value]
		except:
			# тут желательно как-то обработать ситуацию
			return config.Step.MAIN_MENU.value

def get_call(user_id):
	with Vedis(config.db_file) as db:
		try:
			user_data = db[user_id].decode()
			#print('11111', user_data)
			user_data = user_data.replace("""'""",'''"''')
			user_data = ast.literal_eval(user_data)
			db[user_id] = user_data
			print("{} CALL getted".format(user_data[config.UserData.STEP.value]))
			calls = [user_data[config.UserData.CALL.value], user_data[config.UserData.PREVIOUS_CALL.value], user_data[config.UserData.PREVIOUS_PREVIOUS_CALL.value]]
			return calls
		except:
			# тут желательно как-то обработать ситуацию
			return config.Step.MAIN_MENU.value

def clear_call(user_id):
	with Vedis(config.db_file) as db:
		try:
			data = db[user_id].decode()
			#print('44444', data)
			data = data.replace("""'""",'''"''')
			data = ast.literal_eval(data)
			previous_call = data.get(config.UserData.CALL.value, None)
			previous_previous_call = data.get(config.UserData.PREVIOUS_CALL.value, None)
			data.update({config.UserData.CALL.value: None, config.UserData.PREVIOUS_CALL.value: None, config.UserData.PREVIOUS_PREVIOUS_CALL.value: None})
			db[user_id] = data
			print("{} Call added".format(value))
			return True
		except:
			# тут желательно как-то обработать ситуацию
			print("Can't add CALL for user {}".format(user_id))
			return False


def set_data(user_id, type_of_data, value):
	with Vedis(config.db_file) as db:
		try:
			data = db[user_id].decode()
			#print('101010101', data)
			data = data.replace("""'""",'''"''')
			data = ast.literal_eval(data)
			data.update({type_of_data: value})
			db[user_id] = data
			print("{} added".format(type_of_data))
			return True
		except:
			# тут желательно как-то обработать ситуацию
			print("Can't add {} for user {}".format(type_of_data,user_id))
			return False

def get_data(user_id, type_of_data):
	with Vedis(config.db_file) as db:
		try:
			user_data = db[user_id].decode()
			#print('777777777', user_data)
			user_data = user_data.replace("""'""",'''"''')
			user_data = ast.literal_eval(user_data)
			db[user_id] = user_data
			#print(user_data)
			print("{} getted".format(type_of_data))
			return user_data[type_of_data]
		except:
			print('Cant return user data {}'.format(type_of_data))