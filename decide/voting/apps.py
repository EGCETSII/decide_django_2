from django.apps import AppConfig
from django.core.management import call_command


class VotingConfig(AppConfig):
    name = 'voting'

    def ready(self):
        pass
        