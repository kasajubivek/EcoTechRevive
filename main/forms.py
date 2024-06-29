# main/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import UploadedFile, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    security_question_1 = forms.ChoiceField(choices=UserProfile.SECURITY_QUESTIONS, label='Security Question 1')
    security_answer_1 = forms.CharField(label='Security Answer 1')
    security_question_2 = forms.ChoiceField(choices=UserProfile.SECURITY_QUESTIONS, label='Security Question 2')
    security_answer_2 = forms.CharField(label='Security Answer 2')
    security_question_3 = forms.ChoiceField(choices=UserProfile.SECURITY_QUESTIONS, label='Security Question 3')
    security_answer_3 = forms.CharField(label='Security Answer 3')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'security_question_1', 'security_answer_1',
                  'security_question_2', 'security_answer_2', 'security_question_3', 'security_answer_3']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = UserProfile.objects.create(user=user,
                                                 security_question_1=self.cleaned_data['security_question_1'],
                                                 security_answer_1=self.cleaned_data['security_answer_1'],
                                                 security_question_2=self.cleaned_data['security_question_2'],
                                                 security_answer_2=self.cleaned_data['security_answer_2'],
                                                 security_question_3=self.cleaned_data['security_question_3'],
                                                 security_answer_3=self.cleaned_data['security_answer_3'])
            profile.save()
        return user


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


class UserHistoryForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserSessionForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class PasswordResetForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    security_answer_1 = forms.CharField(
        label="Security Question 1",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    security_answer_2 = forms.CharField(
        label="Security Question 2",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    security_answer_3 = forms.CharField(
        label="Security Question 3",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
