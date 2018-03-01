#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from urlparse import urlparse
from time import gmtime, strftime
import logging
import urllib, json
import random
import urllib

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

currency = ''
prevUserMessage = ''
prevData = ''

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):

    keyboard = [[InlineKeyboardButton("USD", callback_data='USD'), InlineKeyboardButton("JPY", callback_data='JPY'), InlineKeyboardButton("CNY", callback_data='CNY'),
                InlineKeyboardButton("SGD", callback_data='SGD')], 
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hello, Friend!\n\nWelcome to the BitCoin Converter.', reply_markup=reply_markup)

def help(bot, update):
    update.message.reply_text('Helpful links here:\n\n🚪 /start - restart the Bot\n\n📱 /about - all about the Bot and creator\n\n📘 /help - helpful links\n\n⚙️ /settings - in developing')

def about(bot, update):
    update.message.reply_text('About us! ----> 🏞🌄🏙 \nWe\'re the largest database of free pictures from all over the world ' 
        'provided by Unsplash.com and Pixabay.com.\n\n📘 /help - helpful links\n\nDo not hesitate to contact with creator @stanrud of this Bot in any questions or propositions.😉\n\nLeft your review here: https://storebot.me/bot/freeimagebot')


def button(bot, update):
    query = update.callback_query

    global currency
    currency = query.data
    bot.edit_message_text(text="Selected currency: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def echo(bot, update):
    
    global prevUserMessage
    global prevData

    ### LOGS ###
    currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(currentTime + " - Request: '" + update.message.text + "' by " + update.message.chat.first_name)
    bot.sendMessage(343438904, currentTime + " - Request: '" + update.message.text + "' by " + update.message.chat.first_name)
    ### END LOGS ###

    userMessage = update.message.text.encode('utf-8')
    url = "https://blockchain.info/tobtc?currency=" + currency + "&value=" + userMessage
    
    print("-------------------------------------")
    
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    keyboard = [[InlineKeyboardButton("USD", callback_data='USD'), InlineKeyboardButton("JPY", callback_data='JPY'), InlineKeyboardButton("CNY", callback_data='CNY'),
                InlineKeyboardButton("SGD", callback_data='SGD')], 
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(data, reply_markup=reply_markup)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("BOT_TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("about", about))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()