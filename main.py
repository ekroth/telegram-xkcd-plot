import telegram

def main():
    bot = telegram.Bot(token='token')
    print(bot.getMe())

if __name__ == "__main__":
    main()
