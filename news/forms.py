from django import forms
from djrichtextfield.widgets import RichTextWidget
from news.models import News


class NewsForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=RichTextWidget())
    image = forms.ImageField()
