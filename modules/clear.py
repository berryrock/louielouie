from vedis import Vedis

def get_step(user_id):
	with Vedis("database.vdb") as db:
		db[user_id] = {"acc": "x6cD#6O*73?L", "step": "mm", "call": None, "prev_call": None, "prev_prev_call": None, "dish": None, "recomendations": None, "info": {"user": 7, "registration": "2019-11-11T21:35:21.050174+03:00", "name": "Влад", "surname": None,
         "email": None, "phone": None, "region": None, "lenght": "178", "birthday": "1992-01-12", "weight": "65", "telegram": "275916740"}}
		print("{} Step getted".format(user_id))
		return True

if __name__ == '__main__':
    result = get_step(275916740)
