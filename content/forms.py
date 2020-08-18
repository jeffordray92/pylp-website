from django import forms


class ResourceForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    image = forms.ImageField()
    attachments = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'attachment_tag'}))
