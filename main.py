from telegram.ext import Updater, CommandHandler,\
     StringCommandHandler,\
     MessageHandler, Filters

import logging
import plotting
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi!")

def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Do your own plotting.")

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def text(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="What, I don't care about '" + update.message.text + "'.")

def plot(bot, update, args):
    plot2(bot, update, ["-1.0", "1.0"] + args)

def plot2(bot, update, args):
    try:
        a = float(args[0])
        b = float(args[1])
        text = ' '.join(args[2:])
        bot.sendMessage(chat_id=update.message.chat_id, text="Plotting [" + str(a) + ", " + str(b) + "] '" + text + "'.")
        file_name = plotting.plot(text, a, b)
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
    dp.add_handler(CommandHandler('plot', plot, pass_args=True))
    dp.add_handler(CommandHandler('plot2', plot2, pass_args=True))

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
