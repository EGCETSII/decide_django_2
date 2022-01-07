from datetime import date, timedelta

from django.utils import timezone

from voting.models import Voting, Question
from base.tests import BaseTestCase
from .updater import autoclose_votings


class EndVotingAutomatically(BaseTestCase):
    def setUp(self):
        super().setUp()

        q1: Question = Question.objects.create(
            desc="Color favorito de entre estos dos: ")

        v1: Voting = Voting.objects.create(
            question=q1, name="¿Qué color te gusta menos?", desc="", deadline=date.today() + timedelta(days=1))
        v1.create_pubkey()
        v1.start_date = timezone.now()
        v1.save()

        v2: Voting = Voting.objects.create(
            question=q1, name="¿Qué color te gusta más?", desc="", deadline=date.today())
        v2.create_pubkey()
        v2.start_date = timezone.now()
        v2.save()

    def tearDown(self):
        super().tearDown()

    def test_group_closing(self):
        self.assertEquals(Voting.objects.filter(end_date=None).count(), 2)
        autoclose_votings()
        self.assertEquals(Voting.objects.filter(end_date=None).count(), 1)
