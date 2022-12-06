import os
import telebot
from dotenv import load_dotenv
from django.core.management.base import BaseCommand,CommandError
from ...bot import BotTelegram

load_dotenv("voting/.env")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

class Command(BaseCommand):

    def handle(self,*args,**options):
        self.stdout.write("Iniciando bot")
        BotTelegram().main()
        self.stdout.write("Bot finalizado")
