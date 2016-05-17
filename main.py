import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import re
from xkcd_plot import XKCDify
import telegram
from telegram.error import NetworkError, Unauthorized

from time import sleep
import logging

_log = logging.getLogger()
_log.setLevel(logging.INFO)

def main():
    token='token'
    with open('.apikey', 'r') as fil:
        token = fil.read().replace('\n', '')
    bot = telegram.Bot(token=token)
    print(bot.getMe())

    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            update_id = handle(bot, update_id)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

def handle(bot, update_id):

    updates = bot.getUpdates(offset=update_id, timeout=10)


    for u in updates:
        update_id = u.update_id + 1

        chat_id = u.message.chat_id
        text = u.message.text.replace('/plottybot ', '')
        print("received input " + text)
        try:
            func = string2func(text)
            a = -3.14
            b = 3.14
            x = np.linspace(a, b, 250)
            ax = plt.axes()
            ax.plot(x, func(x))
        except ValueError, e:
            bot.sendMessage(chat_id=chat_id, text="Invalid input" + str(e))
            continue
        except SyntaxError, e:
            bot.sendMessage(chat_id=chat_id, text="Invalid input" + str(e))
            continue


        plt.xlim(a, b)

        XKCDify(ax,
                xaxis_loc=0.0,
                yaxis_loc=1.0,
                xaxis_arrow='+-',
                yaxis_arrow='+-',
                expand_axes=True)

        plt.savefig('temp.png')
        bot.sendPhoto(chat_id=chat_id, photo=open('temp.png', 'rb'))
        plt.clf()

    return update_id

# Thank you, MaxNoe.
# http://stackoverflow.com/questions/32726992/how-to-plot-a-math-function-from-string
replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
}

allowed_words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
]

def string2func(string):
    ''' evaluates the string and returns a function of x '''
    # find all words and check if all are allowed:
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            raise ValueError(
                '"{}" is forbidden to use in math expression'.format(word)
            )

    for old, new in replacements.items():
        string = string.replace(old, new)

    def func(x):
        return eval(string)

    return func

if __name__ == "__main__":
    main()
