import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i + 1), number=i + 1)
            opt.save()
        v = Voting(name='test voting', question=q, desc='test voting')
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                # a, b = self.encrypt_msg(opt.number, v)
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                token = self.token
                data = {
                    'voting_id': v.id,
                    'voter_id': voter.voter_id,
                    'opt_number': opt.number,
                    'token': token
                }
                clear[opt.number] += 1

                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)  ## 100 voters are created

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        votes = v.tally_votes(self.token)

        tally = v.tally
        tally.sort()

        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):

        user = self.get_or_create_user(1)
        # Make the user an admin
        user.is_staff = True
        user.save()

        # Log in as the user
        self.login(user=user.username)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': {"cat": 1, "dog": 2, "horse": 3},
            'token': self.token
        }

        # Check that the api returns the correct status code
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

        # Check that the voting has been created
        voting = Voting.objects.get(name='Example')
        self.assertEqual(voting.name, 'Example')
        return voting

    def test_start_voting_from_api(self):

        # Create a voting
        voting = self.test_create_voting_from_api()

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action, 'token': self.token}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

    def test_stop_voting_from_api(self):
        voting = self.test_create_voting_from_api()

        # Start the voting
        data = {'action': 'start', 'token': self.token}
        self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        # Stop the voting
        data = {'action': 'stop', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

    def test_tally_voting_from_api(self):
        voting = self.test_create_voting_from_api()

        # Start the voting
        data = {'action': 'start', 'token': self.token}
        self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        # Stop the voting
        data = {'action': 'stop', 'token': self.token}
        self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        # Tally the voting
        data = {'action': 'tally', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop', 'token': self.token}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')