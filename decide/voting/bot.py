import os
import telebot
from dotenv import load_dotenv
from voting.models import Voting

load_dotenv("voting/.env")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

class BotTelegram():

    def botSendMessage(message):
        CHANNEL_ID=os.getenv("TELEGRAM_CHANNEL_ID")
        bot.send_message(CHANNEL_ID, "Hola 👋👋👋, ¿Cómo está ese votante? 🫶")
        bot.send_message(CHANNEL_ID, message)

    @bot.message_handler(commands=['votaciones',])
    def showAllVotings(message):
        # TODO: Mostrar votaciones parseadas
        votings=Voting.objects.all().values_list(flat=True)
        bot.send_message(message.chat.id,"Historial de votaciones: " + str(votings))

    @bot.message_handler(commands=['start',])
    def greetingMessage(message):
        bot.send_message(message.chat.id,"""\
            ¡Hola!👋 soy el bot de Decide 🤖.Estoy aquí para ayudarle 🫡 , escriba /ayuda para ver todos los comandos disponibles. 😊\
                """)
    @bot.message_handler(commands=['canal',])
    def channelMessage(message):
        CHANNEL_LINK=os.getenv("TELEGRAM_NAME_CHANNEL")
        bot.send_message(message.chat.id,"Únete 🫵 a nuestro canal de telegram para mantenerte informado de Decide!! ➡️" + CHANNEL_LINK+ "⬅️")
    @bot.message_handler(commands=['info',])
    def infoMessage(message):
        bot.send_message(message.chat.id,"""\
        Decide es una plataforma de voto electrónica educativa 🗳️, 
el objetivo de este proyecto es implementar una plataforma de voto electrónico seguro 🛟
que cumpla una serie de garantías básicas, como la anonimicidad y el secreto del voto. 🤐

Se trata de un proyecto educativo, pensado para el estudio de sistemas de votación 👨‍🏫,
por lo que prima la simplicidad por encima de la eficiencia cuando sea posible 😬.
Por lo tanto se asumen algunas carencias para permitir que sea entendible y extensible 🤝.
                        \
                """)
    @bot.message_handler(commands=['links',])
    def LinksMessage(message):
        #TODO no muestra los links
        FRONT_LINK=os.getenv("FRONT_URL")
        BACK_LINK=os.getenv("API_URL")
        text="Estos son los Links oficiales de Decide: \n"
        text2="🔘 Front ➡️ "+str(FRONT_LINK)+"✅\n"+ "🔘 Back/API ➡️ " +str(BACK_LINK)+"✅"
        text_final=text + text2
        bot.send_message(message.chat.id,text_final)      
    @bot.message_handler(commands=['ayuda',])
    def helpMessage(message):
        bot.send_message(message.chat.id,"""\
            Los comandos disponibles son los siguientes:
            🔘 /start ➡️ Mensaje de bienvenida 🫶
            🔘 /ayuda ➡️ Ver comandos disponibles 🆘
            🔘 /votaciones ➡️ Ver historial de votaciones 🗳️
            🔘 /canal ➡️ Link del canal oficial de Decide ℹ️
            🔘 /info ➡️ ¿Qué es Decide? 🧐
            🔘 /links ➡️ Links oficiales de Decide ✅

            \
                """)
    def main(self):
        bot.infinity_polling()
    if __name__ == '__main__':
        print('Iniciando el bot')
        main()
        print('Bot iniciado correctamente')
        print('Fin')
