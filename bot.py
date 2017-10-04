#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import config
import core
import telebot

bot = telebot.TeleBot(config.token)

'''
@bot.message_handler(commands=["get"])
def repeat_all_messages_stickers(message):
    msg = bot.send_message(message.chat.id, "Enter some keyword in ENGLISH (for example: piano)")
    bot.register_next_step_handler(bot.send_message(msg, output))

    def output(message):
        #try:
            res = core.get_pic(message.text)
            bot.send_photo(message.from_user.id, res[0])
            bot.send_message(message.from_user.id, 'Fullsize download here:\n' + res[1])
    #except:
        #bot.send_sticker(message.chat.id, config.sorry)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    #try:
        res = core.get_mus(message.text)
        #bot.send_photo(message.from_user.id, res[0])
        #bot.send_message(message.from_user.id, 'Fullsize download here:\n' + res[1])
        bot.send_audio(message.from_user.id, res)
    #except:
        #bot.send_message(message.chat.id, config.sorry)
    #msg = "Hello, " + message.chat.first_name + "!\nEnter command '/get'"
    #bot.send_message(message.chat.id, msg)
    #photo = open('img/check.png', 'rb')
    #bot.send_photo(message.chat.id, photo)
    #message.chat.first_name
    #bot.send_message(message.chat.id, msg)
    #bot.send_photo(message.chat.id, '/check.png')
    #bot.register_next_step_handler(sent, hello)
'''
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.from_user.id, config.start)

@bot.message_handler(commands=['music'])
def photo_message(message):
    msg = bot.send_message(message.from_user.id, config.music)
    bot.register_next_step_handler(msg, getMusic)

def getMusic(message):
    if message.text == '0':
        bot.send_message(message.from_user.id, 'meh...')
    else:
        try:
            res = core.get_mus(message.text)
            bot.send_audio(message.from_user.id, res)
        except:
            bot.send_message(message.chat.id, config.sorry)
        finally:
            msg = bot.send_message(message.from_user.id, config.again)
            bot.register_next_step_handler(msg, getMusic)

@bot.message_handler(commands=['photo'])
def photo_message(message):
    msg = bot.send_message(message.from_user.id, config.photo)
    bot.register_next_step_handler(msg, getPhoto)

def getPhoto(message):
    if message.text == '0':
        bot.send_message(message.from_user.id, 'meh..')
    else:
        try:
            res = core.get_pic(message.text)
            bot.send_photo(message.from_user.id, res[0])
            bot.send_message(message.from_user.id, 'Fullsize download here:\n' + res[1])
        except:
            bot.send_message(message.chat.id, config.sorry)
        finally:
            msg = bot.send_message(message.from_user.id, config.again)
            bot.register_next_step_handler(msg, getPhoto)

@bot.message_handler(content_types=["sticker"])
def repeat_all_messages_stickers(message): 
    bot.send_sticker(message.chat.id, message.sticker.file_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)

