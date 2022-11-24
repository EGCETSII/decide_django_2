import os
import telebot

# Instanciación del bot de Telegram
bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))

class BotTelegram():

    def botSendMessage(message):

        bot.send_message(os.environ.get('TELEGRAM_CANNEL_ID'), "Mensaje de prueba")
        bot.send_message(os.environ.get('TELEGRAM_CANNEL_ID'), "Mensaje de prueba 2")
        bot.send_message(os.environ.get('TELEGRAM_CANNEL_ID'), "Mensaje de prueba 3")
        bot.send_message(os.environ.get('TELEGRAM_CANNEL_ID'), "Si ha llegado hasta aquí ha funcionado todo perfectamente")

# MAIN ################################################################

if __name__ == '__main__':
    print('Iniciando el bot')
    bot.infinity_polling()
    print('Fin')