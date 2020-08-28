from django import forms
from content.models import Resource, SignUpInstructions


class ResourceForm(forms.ModelForm):
    description = forms.CharField(required=True, widget=forms.Textarea)
    attachments = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'attachment_tag'}))

    class Meta:
        model = Resource
        fields = ('title', 'description', 'image')


class SignUpInstructionsForm(forms.ModelForm):

    class Meta:
        model = SignUpInstructions
        fields = ('__all__')
        widgets = {
            'content': forms.Textarea(
                attrs={'id': 'news_textarea'}
            ),
        }


class ContactUsForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)
