import datetime
from django.urls import reverse
from django.test import TestCase

from features.factories import FeatureRequestFactory, \
    ClientFactory, ProductAreaFactory, UserFactory
#from features.forms import FeatureForm, CommentForm
#from features.models import Feature

# These tests are used to check the CRUD capability of the Feature Request App

class TestFeatureRequests(TestCase):

    # Test feature list response
    def test_feature_list(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_list') # As defined in urls.py

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['feature_list']),
                        [feature_request])

    # Test feature detail response
    def test_feature_detail(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_detail', args=[feature_request.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # Test create get redirect response
    def test_create_get(self):
        url = reverse('feature_new')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    # Test creating a new feature request and redirect response
    def test_create_new_feature_request(self):
        author = UserFactory()
        client = ClientFactory()
        prod_area = ProductAreaFactory()
        url = reverse('feature_new')

        response = self.client.post(url, data={
            'author': author.pk,
            'title': 'New Test Request',
            'description': 'Add this new feature',
            'client': client.pk,
            'client_priority': 1,
            'prod_area': prod_area.pk,
            'create_date': '01/01/2019',
            'target_date': '01/01/2019',
        })

        self.assertEqual(response.status_code, 302)

    # Test removing feature and redirect
    def test_delete_get(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_remove', args=[feature_request.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)


# Test to see if the testing model works
class FeatureRequestModelTests(TestCase):

    def test_feature_request_str_returns_title(self):
        feature_request = FeatureRequestFactory(title='New Request')

        self.assertEqual(str(feature_request), 'New Request')
