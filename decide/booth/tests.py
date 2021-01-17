from django.test import TestCase
from django.urls import reverse
# Create your tests here.
        
def test_call_view_votings_authenticated(self):
    response = self.client.get('/booth/', follow=True) 
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'booth/booth.html')
        

def test_call_view_voted_authenticated(self):
    response = self.client.get(reverse('hasVotado')) 
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'booth/hasVotado.html')     
