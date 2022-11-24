import os
import telebot

# Instanciación del bot de Telegram
bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))

class BotTelegram():

    def botSendMessage(message):
        print(os.environ)
        URL=os.environ.get('URL')
        CHANNEL_ID=os.environ.get('TELEGRAM_CHANNEL_ID')

        bot.send_message(CHANNEL_ID, "Mensaje de prueba")
        bot.send_message(CHANNEL_ID, "Mensaje de prueba 2")
        bot.send_message(CHANNEL_ID, "Probando a ver si manda la URL" + str(URL) )
        bot.send_message(CHANNEL_ID, "Ultimo mensaje ")

# MAIN ################################################################

if __name__ == '__main__':
    print('Iniciando el bot')
    bot.infinity_polling()
    print('Bot iniciado correctamente')
    print('Fin')