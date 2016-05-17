import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

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
    print([u.message.text for u in updates])

    for u in updates:
        update_id = u.update_id + 1

        chat_id = u.message.chat_id

        bot.sendMessage(chat_id=chat_id, text="Andy is king you know")

        ax = test_fig()
        plt.savefig('temp.png')

        bot.sendPhoto(chat_id=chat_id, photo=open('temp.png', 'rb'))
        plt.clf()

    return update_id

def test_fig():
    ax = plt.axes()

    x = np.linspace(-10, 10, 100)
    ax.plot(x, -x, 'b')

    ax.set_title('APPLE IS KING')
    ax.set_xlabel('IPHONES')
    ax.set_ylabel('BROKEN')

    ax.legend(loc='lower right')

    XKCDify(ax,
            xaxis_loc=0.0,
            yaxis_loc=0.0,
            xaxis_arrow='+-',
            yaxis_arrow='+-',
            expand_axes=True)

    return ax


if __name__ == "__main__":
    main()
