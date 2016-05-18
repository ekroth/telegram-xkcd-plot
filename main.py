from telegram.ext import Updater, CommandHandler,\
     StringCommandHandler,\
     MessageHandler, Filters

import logging
import plotting
import random
import re
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi! Type '/help'.")

def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=
                    "/start - Seems like every bot needs this.\n"
                    "/help - This, obviously.\n"
                    "/plot <func>\n"
                    "      ex: sin(x) + x^2\n"
                    "/plot2 <start> <end>, <func>\n"
                    "      ex: -3.14, 3.14, cos(x)\n"
                    "/plot3 <title>, <x-label>, <y-label>, <func>\n"
                    "      ex: Gainz Plot, Gainz, Injuries, x^2\n"
                    "/plot4 <title>, <x-label>, <y-label>, <start> <end>, <func>\n"
                    "      ex: Gainz Plot, Gainz, Injuries, 0 100, x^2\n"
                    "Happy plotting!"
                    )

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def text(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="What, I don't care about '" + update.message.text + "'.")

def plot4(bot, update, args):
    # Patterns
    title_t = '[ ]*([a-zA-Z0-9 ]+)'
    range_t = '[ ]*([0-9\.\-]+)[ ]+([0-9\.\-]+)[ ]*'
    funcs_t = '(.+)'
    sep_t   = '[ ]*,[ ]*'

    text = ' '.join(args)
    p = sep_t.join([title_t, title_t, title_t, range_t, funcs_t])
    m = re.search(p, text)

    try:
        # Read inputs
        title = str(m.group(1))
        x_legend = str(m.group(2))
        y_legend = str(m.group(3))
        low = float(m.group(4))
        high = float(m.group(5))
        fs = [f.strip() for f in str(m.group(6)).split(',')]

        bot.sendMessage(chat_id=update.message.chat_id, text=
                        "Plotting '{0}' x: '{1}' y: '{2}' [{3}, {4}] of '{5}'".format(
                            title, x_legend, y_legend, low, high, ', '.join(fs)))
        file_name = plotting.plot(title, x_legend, y_legend, low, high, fs)
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open(file_name, 'rb'))
        bot.sendMessage(chat_id=update.message.chat_id, text=plot_response() + "!")
    except Exception, e:
        bot.sendMessage(chat_id=update.message.chat_id, text="Invalid input because '" + e.message + "'.")

def plot_response():
    responses = [
        "Magnificent", "Sumptuous", "Grand", "Impressive",\
        "Imposing", "Superb", "Spectacular", "Resplendent",\
        "Opulent", "Luxurious", "Palatial", "Deluxe", "Rich",\
        "Fine", "Costly", "Expensive", "Lavish", "Ornate", "Gorgeous",\
        "Glorious", "Dazzling", "Elegant", "Handsome", "Beautiful",\
        "Stately", "Majestic", "Kingly", "Princely", "Regal", "Noble"]

    return random.choice(responses)

def main():

    # Token
    token='token'
    with open('.apikey', 'r') as fil:
        token = fil.read().replace('\n', '')

    # Setup bot
    updater = Updater(token=token)
    dp = updater.dispatcher

    # Standard handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    # Plotting
    dp.add_handler(CommandHandler('plot4', plot4, pass_args=True))

    # Text
    dp.add_handler(MessageHandler([Filters.text], text))

    # Fallback
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
