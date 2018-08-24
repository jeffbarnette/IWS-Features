from django import forms
from features.models import Feature, Comment

class FeatureForm(forms.ModelForm):

    class Meta():
        model = Feature
        fields = ('author','title','description','client','client_priority','prod_area','target_date')

        widgets = { # Connect to CSS styling
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        widgets = { # Connect to CSS styling
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
