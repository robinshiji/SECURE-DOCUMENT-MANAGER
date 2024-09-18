from django import forms
from .models import Document,ImageUpload,User
 # Import both models

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UploadTextFileForm(forms.Form):
    file = forms.FileField(label='Select a text file')