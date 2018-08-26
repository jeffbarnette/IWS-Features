from django import forms
from features.models import Feature, Comment

class FeatureForm(forms.ModelForm):
    #title = forms.CharField(max_length=200)

    class Meta():
        model = Feature
        fields = ('author','title','description','client','client_priority',
                  'prod_area','target_date')
        labels = {
            "client": "Client Name",
            "client_priority": "Client Priority",
            "prod_area": "Product Area"
        }

        widgets = {
            'author':forms.Select(),
            'title':forms.TextInput(attrs={'required': True, 'size': 50, 'maxlength': 200}),
            'description':forms.Textarea(attrs={'required': True, 'rows':5, 'cols':55, 'maxlength': 500}),
            'client':forms.Select(),
            'client_priority':forms.NumberInput(attrs={'required': True, 'min': 1, 'max': 1000, 'maxlength': 4}),
            'prod_area':forms.Select(),
            'target_date':forms.SelectDateWidget()

        }

    def save(self, commit=True):
        if commit:
            priority = self.cleaned_data['client_priority']
            if Feature.objects.filter(client_priority=priority).exists():
                self.instance.client_priority = None
                self.instance.save()
                # Set this feature's client_priority field and change all of the
                # other client feature request priorities (if needed)
                self.instance.to(priority)
            else:
                self.instance.client_priority = priority
                self.instance.save()

        return self.instance

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        labels = {
            "author": "Your Name",
            "text": "Comment"
        }

        widgets = {
            'author':forms.TextInput(attrs={'required': True, 'maxlength': 100}),
            'text':forms.Textarea(attrs={'required': True, 'rows':5, 'cols':55, 'maxlength': 500})
        }
