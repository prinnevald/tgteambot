# -*- coding: utf-8 -*-

import telebot
import sqlite3

from random import shuffle
from string import ascii_uppercase
from logcreds import *

bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('players.sqlite')#, check_same_thread = False)
cur = conn.cursor()

#bot.threaded = False

# def divideteams(players):
#     shuffle(players)
#     mid = len(players) // 2
#     return players[:mid], players[mid:]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, intromsg)

@bot.message_handler(commands=['reg'])
def add_player(message):
    if cur.execute("SELECT EXISTS(SELECT * FROM data WHERE username = '?')", ("@" + message.from_user.username)) == 1:
        bot.send_message(message.chat.id, "Я фсио видэль. Тебя точно видэль")
    else:
        cur.execute("INSERT INTO data (username) VALUES '?'",("@" + message.from_user.username))
        conn.commit()
        bot.reply_to(message, "Теперь ты официальный КСер XD")
    cur.cancel()
        
@bot.message_handler(commands=['immaout'])
def remove_player(message):
    if cur.execute("SELECT EXISTS(SELECT * FROM data WHERE username = '?')",("@" + message.from_user.username)) == 1:
        cur.execute("DELETE FROM data WHERE username = '?')",("@" + message.from_user.username))  #remove from table
        conn.commit()
        bot.reply_to(message, "Ухади отсюда, мужик!")
    else:
        bot.reply_to(message, "Котом Шрёдингера запахло")
    cur.cancel()

@bot.message_handler(commands=['print_all'])
def printing(message):
    if message.from_user.username in verified_users:
        print(list(cur.execute("SELECT username FROM data")[0][0]))
        bot.send_message(message.chat.id, "Больше нит КСеров")
    else:
        bot.send_message(message.chat.id, "Yo r not mah masta")
    cur.cancel()

# @bot.message_handler(commands=['print_teams'])
# def printteams(message):
#     team_a, team_b = divideteams(players)

#     bot.send_message(message.chat.id, "TEAM A: " + str(len(team_a)) + " players")
#     for ta in team_a:
#         bot.send_message(message.chat.id, ta)

#     bot.send_message(message.chat.id, "TEAM B: " + str(len(team_b)) + " players")
#     for tb in team_b:
#         bot.send_message(message.chat.id, tb)

@bot.message_handler(commands=['add_dummies'])  # adds dummy players
def add_dummies(message):
    for ch in ascii_uppercase:
        cur.execute("INSERT INTO data (username) VALUES '?'",("@" + ch * 8))
        conn.commit()
        cur.cancel()

@bot.message_handler(commands=['delete_dummies'])  # delete dummy players
def delete_dummies(message):
    for ch in ascii_uppercase:
        cur.execute("DELETE FROM data WHERE username = '?'",("@" + ch * 8))
        conn.commit()
        cur.cancel()

#conn.close()

bot.polling()
