from django import forms
from djrichtextfield.widgets import RichTextWidget
from news.models import News
from django.forms import ModelForm, Textarea, CheckboxInput


class NewsForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    attachments = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = News
        fields = ('title', 'content', 'tags', 'image')
        required = ('title', 'content')

    def save(self, commit=True, author=None):
        news = super(NewsForm, self).save(commit=False)
        news.author = author
        if commit:
            news.save()
        return news


class NewsModelForm(ModelForm):

    class Meta:
        model = News
        fields = ('__all__')
        widgets = {
            'content': Textarea(
                attrs={'id': 'news_textarea'}
            ),
            'share_on_facebook': CheckboxInput(
                attrs={'id': 'news_share_on_fb'}
            )
        }
