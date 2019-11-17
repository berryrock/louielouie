import random

chars = '/*&#?=abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def generate():
	password =''
	for i in range(12):
		password += random.choice(chars)
	return password