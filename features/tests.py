import datetime
from django.urls import reverse
from django.test import TestCase

from features.factories import FeatureRequestFactory, \
    ClientFactory, ProductAreaFactory
from features.forms import FeatureForm
from features.models import Feature

# This is used to test the CRUD capability of the Feature Request Web App

class FeatureRequestTests(TestCase):

    def test_list(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['feature_requests']),
                         [feature_request])

    def test_detail(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_detail', args=[feature_request.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['feature_request'], feature_request)

    def test_create_get(self):
        url = reverse('feature_form')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], FeatureRequestForm)

    def test_create_post_creates_new_feature_request(self):
        client = ClientFactory()
        prod_area = ProductAreaFactory()
        url = reverse('feature_form')

        response = self.client.post(url, data={
            'title': 'New Test Request',
            'description': 'Add this new feature',
            'client': client.pk,
            'client_priority': 1,
            'product_area': prod_area.pk,
            'create_date': '01/01/2019',
            'target_date': '01/01/2019',
        })

        feature_request = Feature.objects.get()
        self.assertEqual(feature_request.title, 'New Test Request')
        self.assertEqual(feature_request.description, 'Add this new feature')
        self.assertEqual(feature_request.client, client)
        self.assertEqual(feature_request.client_priority, 1)
        self.assertEqual(feature_request.prod_area, prod_area)
        self.assertEqual(feature_request.create_date, datetime.date(2019, 1, 1))
        self.assertEqual(feature_request.target_date, datetime.date(2019, 1, 1))

    def test_create_post_changes_the_client_priority_number(self):
        client = ClientFactory()
        prod_area = ProductAreaFactory()
        feature_request = FeatureRequestFactory(client=client,
                                                client_priority=1)
        url = reverse('feature_form')

        response = self.client.post(url, data={
            'title': 'New Sample Request',
            'description': 'Do something else now',
            'client': client.pk,
            'client_priority': 1,
            'product_area': prod_area.pk,
            'create_date': '02/01/2019',
        })

        # New request sets client priority to 1
        new_request = Feature.objects.exclude(pk=feature_request.pk).get()
        self.assertEqual(new_request.client, client)
        self.assertEqual(new_request.client_priority, 1)

        # Old request gets its priority changed to 2
        old_request = Feature.objects.get(pk=feature_request.pk)
        self.assertEqual(old_request.client, client)
        self.assertEqual(old_request.client_priority, 2)

    def test_create_post_does_not_change_the_client_priority_if_different_clients(self):
        client1 = ClientFactory(name='Client D')
        client2 = ClientFactory(name='Client E')
        prod_area = ProductAreaFactory()
        feature_request = FeatureRequestFactory(client=client1, client_priority=1)
        url = reverse('feature_form')

        response = self.client.post(url, data={
            'title': 'A New Special Request',
            'description': 'Do something with this information',
            'client': client2.pk,
            'client_priority': 1,
            'prod_area': prod_area.pk,
            'create_date': '03/01/2019',
        })

        # New request now sets client priority  to 1
        new_request = Feature.objects.exclude(pk=feature_request.pk).get()
        self.assertEqual(new_request.client, client2)
        self.assertEqual(new_request.client_priority, 1)

        # Old request stays on priority 1 since it is a different client
        old_request = Feature.objects.get(pk=feature_request.pk)
        self.assertEqual(old_request.client, client1)
        self.assertEqual(old_request.client_priority, 1)

    def test_create_post_does_not_change_the_client_priority_if_different_priority(self):
        client = ClientFactory()
        prod_area = ProductAreaFactory()
        feature_request = FeatureRequestFactory(client_priority=1)
        url = reverse('feature_form')

        response = self.client.post(url, data={
            'title': 'Special Request',
            'description': 'Do with it what you will',
            'client': client.pk,
            'client_priority': 2,
            'prod_area': prod_area.pk,
            'create_date': '03/01/2019',
        })

        # New request is set to priority 2
        new_request = Feature.objects.exclude(pk=feature_request.pk).get()
        self.assertEqual(new_request.client, client)
        self.assertEqual(new_request.client_priority, 2)

        # Old request stays on priority 1 since it is a different priority
        old_request = Feature.objects.get(pk=feature_request.pk)
        self.assertEqual(old_request.client, client)
        self.assertEqual(old_request.client_priority, 1)

    def test_create_post_redirects_to_list(self):
        client = ClientFactory()
        prod_area = ProductAreaFactory()
        url = reverse('feature_form')

        response = self.client.post(url, data={
            'title': 'New Request',
            'description': 'Do something',
            'client': client.pk,
            'client_priority': 1,
            'prod_area': prod_area.pk,
            'create_date': '09/01/2018',
            'target_date': '01/01/2019',
        })

        expected_url = reverse('feature_list')
        self.assertRedirects(response, expected_url)

    def test_update_get(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_form', args=[feature_request.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], FeatureForm)
        self.assertEqual(response.context['feature_form'], feature_request)

    def test_update_post_updates_new_feature_request(self):
        client = ClientFactory()
        prod_area = ProductAreaFactory()
        feature_request = FeatureRequestFactory()
        url = reverse('feature_form', args=[feature_request.pk])

        response = self.client.post(url, data={
            'title': 'Updated Request',
            'description': 'Do something different now',
            'client': client.pk,
            'client_priority': 2,
            'product_area': prod_area.pk,
            'target_date': '05/01/2019',
        })

        feature_request = Feature.objects.get()
        self.assertEqual(feature_request.title, 'Updated Request')
        self.assertEqual(feature_request.description, 'Do something else')
        self.assertEqual(feature_request.client, client)
        self.assertEqual(feature_request.client_priority, 2)
        self.assertEqual(feature_request.product_area, product_area)
        self.assertEqual(feature_request.target_date, datetime.date(2016, 2, 1))

    def test_update_post_redirects_to_list(self):
        client = ClientFactory()
        prod_area = ProductAreaFactory()
        feature_request = FeatureRequestFactory()
        url = reverse('feature_form', args=[feature_request.pk])

        response = self.client.post(url, data={
            'title': 'Updated Request',
            'description': 'We can change what it says now',
            'client': client.pk,
            'client_priority': 2,
            'prod_area': product_area.pk,
            'target_date': '07/01/2019',
        })

        expected_url = reverse('feature_list')
        self.assertRedirects(response, expected_url)

    def test_delete_get(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_confirm', args=[feature_request.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['feature_confirm'], feature_request)

    def test_delete_post_deletes_feature_request(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_confirm', args=[feature_request.pk])

        response = self.client.post(url)

        self.assertEqual(Feature.objects.count(), 0)

    def test_delete_post_deletes_redirects_to_list(self):
        feature_request = FeatureRequestFactory()
        url = reverse('feature_confirm', args=[feature_request.pk])

        response = self.client.post(url)

        expected_url = reverse('feature_list')
        self.assertRedirects(response, expected_url)


class FeatureRequestModelTests(TestCase):

    def test_feature_request_str_returns_title(self):
        feature_request = FeatureRequestFactory(title='New Request')

        self.assertEqual(str(feature_request), 'New Request')
