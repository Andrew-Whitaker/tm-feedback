from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from ..views import ClubCreateView
from ..models import Club
from ..forms import ClubModelForm


class ClubCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='john', email='john@doe.com')
        self.user.set_password('12345678')
        self.user.save()
        self.client.login(username='john', password='12345678')

    def test_club_create_view_success_status_code(self):
        url = reverse('clubs:create', kwargs={})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_csrf(self):
        url = reverse('clubs:create', kwargs={})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_club_valid_post_data(self):
        url = reverse('clubs:create', kwargs={})
        data = {
            'name': 'Pushing the Envelope',
            'id': 55,
            'description': 'A safe place to fail, but a great place to succeed!'
        }
        response = self.client.post(url, data)
        # TODO: figure out why response.context is Nonetype in this test
        #  but not in the invalid_data test below
        # form = response.context['form']
        # self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Club.objects.exists(),
                         'The club did not get created')
        club = Club.objects.get(id=55)
        self.assertEquals(club.organizer, self.user)

    def test_new_club_invalid_post_data(self):
        url = reverse('clubs:create', kwargs={})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 200)


class ClubCreateUserRequirements(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='john', email='john@doe.com')
        self.user.set_password('12345678')
        self.user.save()
        self.url = reverse('clubs:create', kwargs={})

    def test_login_required(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

