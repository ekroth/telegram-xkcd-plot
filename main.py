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
                    "/quiet - Don't be verbose.\n"
                    "/examples - What can I do?\n"
                    "/plot <func>\n"
                    "      ex: sin(x) + x^2, cos(x)\n"
                    "/plot2 <start> <end>, <func>\n"
                    "      ex: -3.14, 3.14, cos(x)\n"
                    "/plot3 <title>, <x-label>, <y-label>, <func>\n"
                    "      ex: Gainz Plot, Gainz, Injuries, x^2\n"
                    "/plot4 <title>, <x-label>, <y-label>, <start> <end>, <func>\n"
                    "      ex: Gainz Plot, Gainz, Injuries, 0 100, x^2\n"
                    "Happy plotting!"
                    )

def quiet(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="No, I will continue being verbose.")

def examples(bot, update):
    xs = [
        ("I can do simple plots, such as sin(x).", "/plot", "sin(x)", lambda x: plot1(bot, update, [x])),
        ("That looks odd, let's change the range!", "/plot2", "-3.14 3.14, sin(x)", lambda x: plot2(bot, update, [x])),
        ("Damn, how does cos(x) look compared to sin(x)?", "/plot2", "-3.14 3.14, sin(x), cos(x)", lambda x: plot2(bot, update, [x])),
        ("Let's do some titles.", "/plot3", "PlottyBot, Time, Awesome, x^2", lambda x: plot3(bot, update, [x])),
        ("Let's do everything!.", "/plot4", "PlottyBot, Time, Swoopin, -6.28 5, cos(x) - 2^x, sin(x) + 2*x", lambda x: plot4(bot, update, [x]))
    ]

    bot.sendMessage(chat_id=update.message.chat_id, text="I'm awesome in so many ways!")

    for (msg, cmd, args, exe) in xs:
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)
        bot.sendMessage(chat_id=update.message.chat_id, text="{0} {1}".format(cmd, args))
        exe(args)

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def text(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="What, I don't care about '" + update.message.text + "'.")

def plot1(bot, update, args):
    plot(bot, update, ' '.join(["Plot,x,y,-1.0 1.0,"] + args))

def plot2(bot, update, args):
    plot(bot, update, ' '.join(["Plot,x,y,"] + args))

def plot3(bot, update, args):
    text = ' '.join(args)
    ts = text.split(',')
    plot(bot, update, ', '.join(ts[0:3]) + ",-1.0 1.0," + ', '.join(ts[3:]))

def plot4(bot, update, args):
    plot(bot, update, ' '.join(args))

def plot(bot, update, text):
    # Patterns
    title_t = '[ ]*([^,]+)'
    range_t = '[ ]*([0-9\.\-]+)[ ]+([0-9\.\-]+)[ ]*'
    funcs_t = '(.+)'
    sep_t   = '[ ]*,[ ]*'

    p = sep_t.join([title_t, title_t, title_t, range_t, funcs_t])
    m = re.search(p, text)

    try:
        if not m:
            raise Exception("Invalid pattern.")

        # Read inputs
        title = str(m.group(1))
        x_legend = str(m.group(2))
        y_legend = str(m.group(3))
        low = float(m.group(4))
        high = float(m.group(5))
        fs = [f.strip() for f in str(m.group(6)).split(',')]

        bot.sendMessage(chat_id=update.message.chat_id, text='Get ready for some serious plotting.')
        file_name = plotting.plot(title, x_legend, y_legend, low, high, fs)
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open(file_name, 'rb'))
        bot.sendMessage(chat_id=update.message.chat_id, text=plot_response() + "!")
    except Exception, e:
        bot.sendMessage(chat_id=update.message.chat_id, text="I'm out. " + e.message + "")

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
    dp.add_handler(CommandHandler('quiet', quiet))
    dp.add_handler(CommandHandler('examples', examples))

    # Plotting
    dp.add_handler(CommandHandler('plot',  plot1, pass_args=True))
    dp.add_handler(CommandHandler('plot2', plot2, pass_args=True))
    dp.add_handler(CommandHandler('plot3', plot3, pass_args=True))
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
