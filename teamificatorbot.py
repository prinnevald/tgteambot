# -*- coding: utf-8 -*-

import telebot
import sqlite3 as sq
from random import shuffle
from string import ascii_uppercase
from logcreds import *

bot = telebot.TeleBot(TOKEN)

def dbup():		#connect db
    conn = sq.connect('database.db')
    cur = conn.cursor()
    return cur, conn


def dbdown(conn):	#disconnect db
    conn.commit()
    conn.close()


def verified(msg):	#if admin then true
	return msg in verified_users


def divideteams():	#extracts players from db and forms teams
    cur, conn = dbup()
    cur.execute("SELECT * FROM users")
    players = cur.fetchall()
    shuffle(players)
    mid = len(players) // 2
    return players[:mid], players[mid:]
    dbdown(conn)

#############################################################################

@bot.message_handler(commands=['start', 'help'])	#introductory msg
def send_welcome(message):
    bot.send_message(message.chat.id, intromsg)


@bot.message_handler(commands=['allo'])	#just a check
def allo(message):
    bot.send_message(message.chat.id, "Moshi, Moshi?")


@bot.message_handler(commands=['reg'])	#adds player into database
def add_player(message):
    cur, conn = dbup()
    cur.execute("SELECT * FROM users WHERE username=?", [message.from_user.username])
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO users VALUES (?)", [message.from_user.username])
        bot.reply_to(message, "Теперь ты официальный КСер XD")
    else:
        bot.send_message(message.chat.id, "Я фсио видэль. Тебя точно видэль")   
    dbdown(conn)


@bot.message_handler(commands=['immaout'])	#deletes the record of the player from db
def remove_player(message):
    cur, conn = dbup()
    cur.execute("SELECT * FROM users WHERE username=?", [message.from_user.username])
    if len(cur.fetchall()) > 0:
        cur.execute("DELETE FROM users WHERE username=?", [message.from_user.username])
        bot.reply_to(message, "Ухади отсюда, мужик!")
    else:
        bot.reply_to(message, "Котом Шрёдингера запахло")
    dbdown(conn)


@bot.message_handler(commands=['print_all'])	#prints every player
def printing(message):
    if verified(message.from_user.username):
        cur, conn = dbup()   
        cur.execute("SELECT * FROM users")
        list = cur.fetchall()

        for player in list:
            bot.send_message(message.chat.id, "@" + player[0])
        bot.send_message(message.chat.id, "Больше нит КСеров")

        dbdown(conn)
    else:
        bot.reply_to(message, "U r not mah masta")


@bot.message_handler(commands=['print_teams'])	#divides and prints out teams
def printteams(message):
    if verified(message.from_user.username):
        team_a, team_b = divideteams()

        bot.send_message(message.chat.id, "TEAM A: " + str(len(team_a)) + " players")
        for ta in team_a:
            bot.send_message(message.chat.id, ta)

        bot.send_message(message.chat.id, "TEAM B: " + str(len(team_b)) + " players")
        for tb in team_b:
            bot.send_message(message.chat.id, tb)
    else:
        bot.reply_to(message, "U r not mah masta")


@bot.message_handler(commands=['add_dummies'])	#adds dummy players for testing
def add_dummies(message):
    if verified(message.from_user.username):
        cur, conn = dbup()
        for ch in ascii_uppercase:
            cur.execute("SELECT * FROM users WHERE username=?", [ch * 8])
            if len(cur.fetchall()) == 0:
                cur.execute("INSERT INTO users VALUES (?)", [ch * 8])

        bot.reply_to(message, "Done")    
        dbdown(conn)
    else:
        bot.reply_to(message, "U r not mah masta")


@bot.message_handler(commands=['delete_dummies'])  #deletes dummy players for testing
def delete_dummies(message):
    if verified(message.from_user.username):
        cur, conn = dbup()
        for ch in ascii_uppercase:
            cur.execute("SELECT * FROM users WHERE username=?", [ch * 8])
            if len(cur.fetchall()) > 0:
                cur.execute("DELETE FROM users WHERE username=?", [ch * 8])

        bot.reply_to(message, "Done")    
        dbdown(conn)
    else:
        bot.reply_to(message, "U r not mah masta")    


@bot.message_handler(commands=['clear_db'])		#clears database if needed to restart
def clear_db(message):
    if verified(message.from_user.username):
        cur, conn = dbup()
        cur.execute("DELETE FROM users")
        bot.reply_to(message, "Done")    
        dbdown(conn)
    else:
        bot.reply_to(message, "U r not mah masta") 


# @bot.message_handler(commands=['create_db'])
# def create_db(message):
#     cur, conn = dbup()
#     cur.execute("""CREATE TABLE users (
#             username text
#             )""")
#     dbdown(conn)


bot.polling()