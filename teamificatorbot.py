# -*- coding: utf-8 -*-

import telebot
from random import shuffle
import sqlite3 as sq
from string import ascii_uppercase

from logcreds import *

bot = telebot.TeleBot(TOKEN)


def divideteams(players):
    shuffle(players)
    mid = len(players) // 2
    return players[:mid], players[mid:]


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
    conn = sq.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (message.from_user.username,))
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO users VALUES (?)", (message.from_user.username,))
        bot.reply_to(message, "Теперь ты официальный КСер XD")
    else:
        bot.send_message(message.chat.id, "Я фсио видэль. Тебя точно видэль")
    conn.commit()
    conn.close()


@bot.message_handler(commands=['add'])  # adds dummy players
def add_dummies(message):
    conn = sq.connect('database.db')
    cur = conn.cursor()

    for ch in ascii_uppercase:
        cur.execute("SELECT * FROM users WHERE username=?", (ch * 8,))
        if len(cur.fetchall()) == 0:
            cur.execute("INSERT INTO users VALUES (?)", (ch * 8,))

    conn.commit()
    conn.close()


@bot.message_handler(commands=['immaout'])
def remove_player(message):
    if message.from_user.username in players:
        bot.reply_to(message, "Ухади отсюда, мужик!")
        players.remove(message.from_user.username)
    else:
        bot.reply_to(message, "Котом Шрёдингера запахло")


@bot.message_handler(commands=['print_all'])
def printing(message):
    # if message.from_user.username in verified_users:

    conn = sq.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    list = cur.fetchall()

    for player in list:
        bot.send_message(message.chat.id, "@" + player[0])
    bot.send_message(message.chat.id, "Больше нит КСеров")
    conn.commit()
    conn.close()


# @bot.message_handler(commands=['create_db'])
# def create_db(message):
#     conn = sq.connect('database.db')
#     cur = conn.cursor()
#     cur.execute("""CREATE TABLE users (
#             username text
#             )""")
#     conn.commit()
#     conn.close()


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
