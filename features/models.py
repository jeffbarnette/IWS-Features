from django.db import models
from django.utils import timezone
from django.urls import reverse

class Feature(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=200) # Title of request
    description = models.TextField(max_length=500) # Description of feature
    client = models.ForeignKey('features.client', on_delete = models.CASCADE) # Client name
    client_priority = models.IntegerField() # Client priority
    prod_area = models.ForeignKey('features.prodarea', on_delete = models.CASCADE) # Product area
    create_date = models.DateTimeField(default=timezone.now) # Creation date
    target_date = models.DateTimeField(blank=True,null=True) # Target date

    def publish(self):
        self.target_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("feature_detail", kwargs={'pk':self.pk})

    def __str__(self):
        return self.title # Return Feature title in Admin View

class Comment(models.Model):
    post = models.ForeignKey('features.Feature', related_name='comments', on_delete = models.CASCADE)
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

class Client(models.Model):
    client_name = models.CharField(max_length=200) # Client name
    def __str__(self):
        return self.client_name # Return Client name in Admin View

class ProdArea(models.Model):
    prod_area = models.CharField(max_length=200) # Product area
    def __str__(self):
        return self.prod_area # Return Product area in Admin View
