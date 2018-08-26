from django.utils import timezone
import factory
from factory import DjangoModelFactory
from features.models import Client, ProdArea, Feature
from django.contrib.auth import get_user_model
User = get_user_model()


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
        django_get_or_create = ('client_name',)

    client_name = 'Test Client'


class ProductAreaFactory(DjangoModelFactory):
    class Meta:
        model = ProdArea
        django_get_or_create = ('prod_area',)

    prod_area = 'Reports'

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email', 'password')

    username = 'admin'
    email = 'admin@mycompanysite.com'
    password = 'django1234'

    is_superuser = True
    is_staff = True
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class FeatureRequestFactory(DjangoModelFactory):
    class Meta:
        model = Feature

    author = factory.SubFactory(UserFactory)
    title = 'Feature Request'
    description = 'This new features needs to be added right away!'
    client = factory.SubFactory(ClientFactory)
    client_priority = 1
    prod_area = factory.SubFactory(ProductAreaFactory)
    create_date = timezone.now().date()
    target_date = timezone.now().date()
