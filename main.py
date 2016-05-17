import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from parse import string2func
from xkcd_plot import XKCDify

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from time import sleep
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I won't help you.")

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():

    # Token
    token='token'
    with open('.apikey', 'r') as fil:
        token = fil.read().replace('\n', '')

    # Setup bot
    updater = Updater(token=token)
    dp = updater.dispatcher

    # Setup handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler([Filters.command], unknown))

    # Log all errors
    dp.add_error_handler(error)

    # Start
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    main()
