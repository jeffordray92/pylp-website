from django import forms
from content.models import SignUpInstructions


class ResourceForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    image = forms.ImageField()
    attachments = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'attachment_tag'}))


class SignUpInstructionsForm(forms.ModelForm):

    class Meta:
        model = SignUpInstructions
        fields = ('__all__')
        widgets = {
            'content': forms.Textarea(
                attrs={'id': 'news_textarea'}
            ),
        }
