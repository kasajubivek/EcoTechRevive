# main/forms.py
# sample

from django import forms
from django.contrib.auth.models import User
from .models import UploadedFile, UserProfile, Product, EnquiryModel


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    security_question_1 = forms.ChoiceField(
        choices=[('', 'Select an appropriate question')] + UserProfile.SECURITY_QUESTIONS,
        label='Security Question 1',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    security_answer_1 = forms.CharField(label='Security Answer 1',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    security_question_2 = forms.ChoiceField(
        choices=[('', 'Select an appropriate question')] + UserProfile.SECURITY_QUESTIONS,
        label='Security Question 2',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    security_answer_2 = forms.CharField(label='Security Answer 2',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    security_question_3 = forms.ChoiceField(
        choices=[('', 'Select an appropriate question')] + UserProfile.SECURITY_QUESTIONS,
        label='Security Question 3',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    security_answer_3 = forms.CharField(label='Security Answer 3',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'security_question_1', 'security_answer_1',
                  'security_question_2', 'security_answer_2', 'security_question_3', 'security_answer_3']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose another one.")
        return username

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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'product_image']
        exclude = ['uploaded_by']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = EnquiryModel
        fields = ['company_name', 'first_name', 'last_name', 'phone_number', 'email', 'service', 'heard_about']

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        # Combine the label for first and last name fields
        self.fields['first_name'].label = "Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
        self.fields['last_name'].label = ""  # Hide the individual label for last name
        # Ensure service field is a ChoiceField
        self.fields['service'] = forms.ChoiceField(
            choices=EnquiryModel.SERVICE_CHOICES,
            required=True,
            widget=forms.Select
        )
