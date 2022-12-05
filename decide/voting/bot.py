import os
import telebot
from dotenv import load_dotenv

load_dotenv("voting/.env")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

class BotTelegram():

    def botSendMessage(message):
        CHANNEL_ID=os.getenv("TELEGRAM_CHANNEL_ID")
        bot.send_message(CHANNEL_ID, "Hola 👋👋👋, ¿Cómo está ese votante? 🫶")
        bot.send_message(CHANNEL_ID, message)


if __name__ == '__main__':
    print('Iniciando el bot')
    bot.infinity_polling()
    print('Bot iniciado correctamente')
    print('Fin')
    