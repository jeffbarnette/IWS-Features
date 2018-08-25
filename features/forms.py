from django import forms
from features.models import Feature, Comment

class FeatureForm(forms.ModelForm):
    title = forms.CharField(max_length=200)

    class Meta():
        model = Feature
        fields = ('author','title','description','client','client_priority',
                  'prod_area','target_date')

        widgets = {
            'title':forms.TextInput(),
            'description':forms.Textarea(),
            'client_priority':forms.NumberInput(),
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

        widgets = {
            'author':forms.TextInput(),
            'text':forms.Textarea()
        }
