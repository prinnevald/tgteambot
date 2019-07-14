# -*- coding: utf-8 -*-

import telebot
import sqlite3

from random import shuffle
from string import ascii_uppercase
from logcreds import *

bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('players.sqlite')
cur = conn.cursor()

def divideteams(players):
    shuffle(players)
    mid = len(players) // 2
    return players[:mid], players[mid:]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, intromsg)


@bot.message_handler(commands=['reg'])
def add_player(message):
    if message.from_user.username in players:
        bot.send_message(message.chat.id, "Я фсио видэль. Тебя точно видэль")
    else:
        players.append(message.from_user.username)
        bot.reply_to(message, "Теперь ты официальный КСер XD")

@bot.message_handler(commands=['add'])  # adds dummy players
def add_dummies(message):
    for ch in ascii_uppercase:
        players.append(ch * 8)

@bot.message_handler(commands=['immaout'])
def remove_player(message):
    if message.from_user.username in players:
        bot.reply_to(message, "Ухади отсюда, мужик!")
        players.remove(message.from_user.username)
    else:
        bot.reply_to(message, "Котом Шрёдингера запахло")

@bot.message_handler(commands=['print_all'])
def printing(message):
    if message.from_user.username in verified_users:
        for player in players:
            bot.send_message(message.chat.id, "@" + player)
        bot.send_message(message.chat.id, "Больше нит КСеров")

@bot.message_handler(commands=['print_teams'])
def printteams(message):
    team_a, team_b = divideteams(players)

    bot.send_message(message.chat.id, "TEAM A: " + str(len(team_a)) + " players")
    for ta in team_a:
        bot.send_message(message.chat.id, ta)

    bot.send_message(message.chat.id, "TEAM B: " + str(len(team_b)) + " players")
    for tb in team_b:
        bot.send_message(message.chat.id, tb)

bot.polling()
