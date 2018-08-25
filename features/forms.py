from django import forms
from features.models import Feature, Comment

class FeatureForm(forms.ModelForm):
    title = forms.CharField(max_length=200)

    class Meta():
        model = Feature
        fields = ('author','title','description','client','client_priority','prod_area','target_date')

        widgets = {
            'title':forms.TextInput(),
            'description':forms.Textarea(),
            'client_priority':forms.NumberInput(),
            'target_date':forms.SelectDateWidget()

        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        widgets = {
            'author':forms.TextInput(),
            'text':forms.Textarea()
        }
