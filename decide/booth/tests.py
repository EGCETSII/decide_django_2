from django.test import TestCase
from django.urls import reverse
from voting.models import Voting
from voting.serializers import VotingSerializer
# Create your tests here.


def setUp(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    self.driver = webdriver.Chrome(options=options)
    super().setUp()


def tearDown(self):
    super().tearDown()
    self.driver.quit()
        
        
def test_call_view_votings_authenticated(self):
    response = self.client.get('/booth/', follow=True) 
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'booth/booth.html')
        

def test_call_view_voted_authenticated(self):
    response = self.client.get(reverse('hasVotado')) 
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'booth/hasVotado.html')     


def test_get_votings(self, mocker):
    expected_results = [
        Voting(
            voting_id=4,
            name="EGC",
            desc="Aprobar EGC no es fácil",
            question(
                yesorno="¿Vamos a aprobar EGC?",
                options(
                    y="Yes",
                    n="No")),
            start_date="2021-01-08T15:29:52.040435",
            end_date=None,
            url="http://localhost:8000/booth/4",
            pubkey="a1s2d3f4g5h6j7k8l9",
            voted=False
            )]
    qs = MockSet(expected_results[0])
    mocker.patch.object(Voting.objects, 'get_queryset', return_value=qs)

    result = list(Voting.objects.get_id(4))

    assert result == expected_results
    assert str(result[0]) == expected_results[0].code

    
def test_get_votings_fail(self, mocker):
    expected_results = [
        Voting(
            voting_id=4,
            name="PGPI",
            desc="Aprobar PGPI no es fácil",
            question(
                yesorno="¿Vamos a aprobar PGPI?",
                options(
                    y="Yes",
                    n="No")),
            start_date="2021-01-08T15:29:52.040435",
            end_date=None,
            url="http://localhost:8000/booth/4",
            pubkey="a1s2d3f4g5h3j7k8l9",
            voted=False
            )]
    qs = MockSet(expected_results[0])
    mocker.patch.object(Voting.objects, 'get_queryset', return_value=qs)

    result = list(Voting.objects.get_id(4))

    assert result != expected_results
    assert str(result[0]) != expected_results[0].code

    
def test_expected_serialized_json(self):
    expected_results = {
            "voting_id": 4,
            "name": "EGC",
            "desc": "Aprobar EGC no es fácil",
            "question": {
                "yesorno": "¿Vamos a aprobar EGC?",
                "options": {
                    "y": "Yes",
                    "n": "No"}},
            "start_date":"2021-01-08T15:29:52.040435",
            "end_date":None,
            "url":"http://localhost:8000/booth/4",
            "pub-key": "a1s2d3f4g5h6j7k8l9",
            "voted": False
            }
    voting = Voting(**expected_results)
    results = VotingSerializer(voting).data
    
    assert results == expected_results
    

def test_raise_error_when_missing_required_field(self):
        incomplete_data = {
            "voting_id": 4,
            "desc": "Aprobar EGC no es fácil",
            "question": {
                "yesorno": "¿Vamos a aprobar EGC?",
                "options": {
                    "y": "Yes",
                    "n": "No"}},
            "start_date":"2021-01-08T15:29:52.040435",
            "end_date":None,
            "pub-key": "a1s2d3f4g5h6j7k8l9",
            "voted": False
            }

        serializer = VotingSerializer(data=incomplete_data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)    
            
            
