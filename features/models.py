from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from ordered_model.models import OrderedModelBase

@python_2_unicode_compatible # Make it work with Python 2.7x
class Feature(OrderedModelBase):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=200) # Title of request
    description = models.TextField(max_length=500) # Description of feature
    client = models.ForeignKey('features.client', on_delete = models.CASCADE) # Client name
    client_priority = models.PositiveIntegerField(db_index=True, null=True,
                                                  blank=True) # Client priority
    prod_area = models.ForeignKey('features.prodarea', on_delete = models.CASCADE) # Product area
    create_date = models.DateTimeField(default=timezone.now) # Creation date
    target_date = models.DateTimeField(blank=True,null=True) # Target date
    order_field_name = 'client_priority'
    order_with_respect_to = 'client'

    class Meta:
        ordering = ('client', 'client_priority')

    def publish(self):
        self.target_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("feature_detail", kwargs={'pk':self.pk})

    def __str__(self):
        return self.title # Return Feature title in Admin View

@python_2_unicode_compatible # Make it work with Python 2.7x
class Comment(models.Model):
    post = models.ForeignKey('features.Feature', related_name='comments',
                                                 on_delete = models.CASCADE)
    author = models.CharField(max_length= 200) # Comment author name
    text = models.TextField() # Comment text
    create_date = models.DateTimeField(default=timezone.now) # Creation date
    approved_comment = models.BooleanField(default=False) # Boolean status

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('feature_list') # Return to feature list view

    def __str__(self):
        return self.text # Return Comment text in Admin View

@python_2_unicode_compatible # Make it work with Python 2.7x
class Client(models.Model):
    client_name = models.CharField(max_length=200, unique=True) # Client name

    class Meta:
        ordering = ('client_name',)

    def __str__(self):
        return self.client_name # Return Client name in Admin View

@python_2_unicode_compatible # Make it work with Python 2.7x
class ProdArea(models.Model):
    prod_area = models.CharField(max_length=200) # Product area

    class Meta:
        ordering = ('prod_area',)

    def __str__(self):
        return self.prod_area # Return Product area in Admin View
