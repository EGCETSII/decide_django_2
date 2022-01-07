from datetime import date, datetime
from voting.models import Voting
from apscheduler.schedulers.background import BackgroundScheduler


def autoclose_votings():
    for voting in Voting.objects.filter(deadline__lte=date.today(), end_date=None):
        voting.end_date = datetime.now()
        voting.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(autoclose_votings, 'cron', hour=0, minute=0)
    scheduler.start()
