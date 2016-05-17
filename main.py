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
        bot.sendMessage(chat_id=u.message.chat_id, text="Andy is king you know")

    return update_id


if __name__ == "__main__":
    main()
