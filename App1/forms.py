from django import forms
from .models import Complains
from django.contrib.auth.forms import AuthenticationForm
class CompalinForm(forms.ModelForm):

    class Meta:
        model = Complains
        fields = ['complaint_catagory', 'description', 'file', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.studentprofile.is_hosteler == False:
                self.fields['complaint_catagory'].choices = [
                    choice
                    for choice in self.fields['complaint_catagory'].choices
                    if choice[0] not in ['Hostel', 'Transport']
                ]
class OverviewForm(forms.ModelForm):
    class Meta:
        model=Complains
        fields=['satisfaction']
class Login_form(AuthenticationForm):
    username=forms.EmailField(
        label="Collage Email:-",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your college email"
        })
    )
    password=forms.CharField(
        label="Password:-",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"

        })
    )