from django import forms
from djrichtextfield.widgets import RichTextWidget
from news.models import News
from django.forms import ModelForm, Textarea


class NewsForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField()
    image = forms.ImageField()
    tags = forms.CharField()
    attachments = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'multiple': True}))


class NewsModelForm(ModelForm):

    class Meta:
        model = News
        fields = ('__all__')
        widgets = {
            'content': Textarea(
                attrs={'id': 'news_textarea'}
            ),
        }
