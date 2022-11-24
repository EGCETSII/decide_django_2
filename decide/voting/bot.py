import os
import telebot
import environ

env = environ.Env()
environ.Env.read_env()

# Instanciación del bot de Telegram
bot = telebot.TeleBot(env("TELEGRAM_TOKEN"))

class BotTelegram():

    def botSendMessage(message):
        CHANNEL_ID=env("TELEGRAM_CHANNEL_ID")

        bot.send_message(CHANNEL_ID, "Hola, ¿Cómo está ese votante?")
        bot.send_message(CHANNEL_ID, message)

# MAIN ################################################################

if __name__ == '__main__':
    print('Iniciando el bot')
    bot.infinity_polling()
    print('Bot iniciado correctamente')
    print('Fin')
    