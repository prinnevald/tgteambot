# -*- coding: utf-8 -*-

import telebot
#import sys
from logcreds import *
from user import *

bot = telebot.TeleBot(TOKEN)
players = []

#registered users = ['Shaneliya', 'treoa', 'prinnydood']

teama = []
teamb = []

def divideteams():  #divides into two teams
    i=0
    for v in players:
        if (thereisinteams(v) == False):
            if (i%2==0):
                teama.append(v)
            else:
                teamb.append(v)
        i=i+1

def thereis(usr):
    for element in players:
    	if (element == usr):
			return True
    return False

def thereisinteams(usr):
    for element in teama:
    	if (element == usr):
			return True
    for element in teamb:
    	if (element == usr):
			return True
    return False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Всем привет, друзья 🙂 Я бот созданный \
для вашего тимбилдинга. Регистрируясь у меня, ты обещаешь прийти на крутой \
тимбилдинг ксников 😉. Теперь давайте пройдемся по командам: \n \
    /reg - для твоей регистрации на тимбилдинг. Это нужно для будущего деления по командам. \n \
    /immaout - Если передумал идти на тимбилдинг 🙁 Но после все еще можешь присоединиться \n \
По вопросам обращаться к @treoa или @prinnydood")

@bot.message_handler(commands=['reg'])
def add_player(message):
	if (thereis(message.from_user.username) == False):
		players.append(message.from_user.username)
		bot.reply_to(message, "Теперь ты официальный КСер XD")
	else:
		bot.send_message(message.chat.id, "Я фсио видэль. Тебя точно видэль")

@bot.message_handler(commands = ['immaout'])
def remove_player(message):
    if (thereis(message.from_user.username) == True):
        bot.reply_to(message, "Ухади отсюда, мужик!")
        players.remove(message.from_user.username)
    else:
        bot.reply_to(message, "Котом Шрёдингера запахло")

@bot.message_handler(commands = ['print_all'])
def printing(message):
    #if (message.from_user.username == verified_users):
    for element in players:
        bot.send_message(message.chat.id, element)
    bot.send_message(message.chat.id, "Больше нит КСеров")
    #else:
    #    pass

@bot.message_handler(commands=['print_teams'])   #divides and prints into teams
def printteams(message):
    divideteams();
    bot.send_message(message.chat.id, "TEAM A:")
    for ta in teama:
        bot.send_message(message.chat.id, ta)
    bot.send_message(message.chat.id, "TEAM B:")
    for tb in teamb:
        bot.send_message(message.chat.id, tb)

bot.polling()
