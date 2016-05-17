import telegram

def main():
    token='token'
    with open('.apikey', 'r') as fil:
        token = fil.read().replace('\n', '')
    bot = telegram.Bot(token=token)
    print(bot.getMe())

if __name__ == "__main__":
    main()
