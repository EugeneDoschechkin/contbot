#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import config
import requests
import random
from bs4 import BeautifulSoup as Parser
from requests_oauthlib import OAuth1
import json
import telebot

### Core class - makes all the dirty work
class BotCore():
        
        ### bools for each command (made for looped work in every function for user's comfort)
        bool_music = False
        bool_photo = False
        bool_gif = False
        bool_ico = False
        bool_vector = False
        bool_art = False
        photo_cash = {}
        art_cash = {}
        vector_cash = {}

        ### user keyboard inits
        start_markup = None
        exit_markup = None
        random_markup = None

        ### create all the user keyboards when initializing a Core object
        def __init__(self):
                self.start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                self.start_markup.row('/photo', '/art', '/vector')
                self.start_markup.row('/icon', '/music', '/gif')
                self.start_markup.row('/help')
                self.exit_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                self.exit_markup.row('/exit')
                self.random_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                self.random_markup.row('more!', '/exit')

        ### reset all bools at start or at /exit command
        def Reset(self):
                self.bool_music = False
                self.bool_photo = False
                self.bool_gif = False
                self.bool_ico = False
                self.bool_vector = False
                self.bool_art = False

        ### music func, works via ccmixter.org API, no key needed
        def Music(self, message, bot):
                try:
                        if (len(message.text.split()) > 1): query = '+'.join(message.text.split())
                        else: query = message.text
                        url = 'http://ccmixter.org/api/query?f=json&score=4&t=links_stream&lic=by&rand=1&limit=20&tags=' + query
                        page = requests.get(url)
                        mus_list = json.loads(page.text)
                        rannum = random.randint(0, len(mus_list)-1)
                        res = mus_list[rannum]['files'][0]['download_url']
                        bot.send_audio(message.from_user.id, res)
                except:
                        bot.send_message(message.chat.id, config.sorry)

        ### gif func, works without API
        def RandGIF(self, message, bot):
                try:
                        page = requests.get('http://www.gifbin.com/random')
                        html = Parser(page.text, "html.parser")
                        res = html.find('source', {'type': 'video/mp4'}).get('src')
                        bot.send_video(message.from_user.id, res)
                except:
                        bot.send_message(message.chat.id, config.sorry)

        ### icon func, works via thenounproject.com API, keys required
        def ICO(self, message, bot):
                try:
                        auth = OAuth1(config.ico_key, config.ico_sec)
                        endpoint = "http://api.thenounproject.com/icons/" + message.text +"?limit_to_public_domain=1"
                        response = requests.get(endpoint, auth=auth)
                        ico_list = json.loads(response.text)
                        rannum = random.randint(0, len(ico_list['icons'])-1)
                        res = ico_list['icons'][rannum]['preview_url_84']
                        bot.send_message(message.from_user.id, 'Image from thenounproject.com\n' + res)
                except:
                        bot.send_message(message.chat.id, config.sorry)

        ### PixaBay func that sends photo, vector or art depending on bools, works via pixabay.com API, key required

        def PixaBay(self, message, bot):
                try:
                        if 'а'<=message.text[0]<='я' or 'А'<=message.text[0]<='Я': lang = 'ru'
                        else: lang = 'en'
                        if (len(message.text.split()) > 1): query = '+'.join(message.text.split())
                        else: query = message.text

                        img_type = ''
                        cash = {}
                        if self.bool_photo:
                                img_type = 'photo'
                                cash = self.photo_cash
                        elif self.bool_vector:
                                img_type = 'vector'
                                cash = self.vector_cash
                        elif self.bool_art:
                                img_type = 'illustration'
                                cash = self.art_cash

                        if query not in cash.keys():
                                url = 'https://pixabay.com/api/?key=' + config.pix_key + '&q=' + query + '&image_type=' + img_type + '&lang=' + lang + '&per_page=50&response_group=high_resolution'
                                response = requests.get(url)
                                pix_list = json.loads(response.text)
                                arr = []
                                dic = {}
                                for i in range(0, len(pix_list['hits'])):
                                    arr.append(pix_list['hits'][i]['imageURL'])
                                dic = {query: arr}
                                cash.update(dic)
                                print('cashed ' + img_type)

                        res = cash.get(query)
                        rannum = random.randint(0, len(res)-1)
                        bot.send_message(message.from_user.id, 'Image from Pixabay.com\n' + res[rannum])
                except:
                        bot.send_message(message.chat.id, config.sorry)

# initialazing objects
bot = telebot.TeleBot(config.token)
core = BotCore()

# decorators, handle incoming commands
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
        core.Reset()
        bot.send_message(message.from_user.id, config.start, reply_markup = core.start_markup)

@bot.message_handler(commands=['exit'])
def exit_message(message):
        core.Reset()
        bot.send_message(message.from_user.id, config.choice, reply_markup = core.start_markup)

@bot.message_handler(commands=['music'])
def music_message(message):
        core.bool_music = True
        bot.send_message(message.from_user.id, config.key, reply_markup = core.exit_markup)

@bot.message_handler(commands=['photo'])
def photo_message(message):
        core.bool_photo = True
        bot.send_message(message.from_user.id, config.key_pix, reply_markup = core.exit_markup)

@bot.message_handler(commands=['art'])
def art_message(message):
        core.bool_art = True
        bot.send_message(message.from_user.id, config.key_pix, reply_markup = core.exit_markup)

@bot.message_handler(commands=['vector'])
def vector_message(message):
        core.bool_vector = True
        bot.send_message(message.from_user.id, config.key_pix, reply_markup = core.exit_markup)

@bot.message_handler(commands=['icon'])
def ico_message(message):
        core.bool_ico = True
        bot.send_message(message.from_user.id, config.key, reply_markup = core.exit_markup)

@bot.message_handler(commands=['gif'])
def gif_message(message):
        core.bool_gif = True
        core.RandGIF(message, bot)
        bot.send_message(message.from_user.id, config.again, reply_markup = core.random_markup)

@bot.message_handler(content_types=['text'])
def executer(message):
        if core.bool_music:
                core.Music(message, bot)
                bot.send_message(message.from_user.id, config.key, reply_markup = core.exit_markup)
        elif core.bool_photo:
                core.PixaBay(message, bot)
                bot.send_message(message.from_user.id, config.key_pix, reply_markup = core.exit_markup)
        elif core.bool_art:
                core.PixaBay(message, bot)
                bot.send_message(message.from_user.id, config.key_pix, reply_markup = core.exit_markup)
        elif core.bool_vector:
                core.PixaBay(message, bot)
                bot.send_message(message.from_user.id, config.key_pix, reply_markup = core.exit_markup)
        elif core.bool_ico:
                core.ICO(message, bot)
                bot.send_message(message.from_user.id, config.key, reply_markup = core.exit_markup)
        elif core.bool_gif and (message.text == 'more!'):
                core.RandGIF(message, bot)
                bot.send_message(message.from_user.id, config.again, reply_markup = core.random_markup)

@bot.message_handler(content_types=["sticker"])
def repeat_all_messages_stickers(message): 
    bot.send_sticker(message.chat.id, message.sticker.file_id)
                   
if __name__ == '__main__':
    bot.polling(none_stop=True)
