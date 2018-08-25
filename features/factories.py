from django.utils import timezone
import factory
from factory import DjangoModelFactory

from feature_request.request.models import Client, ProdArea, Feature


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
        django_get_or_create = ('client_name',)

    name = 'Test Client'


class ProductAreaFactory(DjangoModelFactory):
    class Meta:
        model = ProdArea
        django_get_or_create = ('prod_area',)

    name = 'Reports'


class FeatureRequestFactory(DjangoModelFactory):
    class Meta:
        model = Feature

    author = 'admin'
    title = 'Feature Request'
    description = 'This new features needs to be added right away!'
    client = factory.SubFactory(ClientFactory)
    client_priority = 1
    prod_area = factory.SubFactory(ProductAreaFactory)
    create_date = timezone.now().date()
    target_date = timezone.now().date()
