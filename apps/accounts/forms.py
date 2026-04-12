from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'phone', 'role']

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username.lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(user.username.upper())
        user.must_change_password = True
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'phone', 'role']

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        qs = User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('This username is already taken.')
        return username.lower()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        pw = self.cleaned_data.get('current_password')
        if not self.user.check_password(pw):
            raise forms.ValidationError('Current password is incorrect.')
        return pw

    def clean(self):
        cleaned = super().clean()
        npw = cleaned.get('new_password')
        cpw = cleaned.get('confirm_password')
        if npw and cpw and npw != cpw:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.must_change_password = False
        self.user.save(update_fields=['password', 'must_change_password'])


class SetNewPasswordForm(forms.Form):
    """Used on first login when must_change_password=True."""
    new_password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        npw = cleaned.get('new_password')
        cpw = cleaned.get('confirm_password')
        if npw and cpw and npw != cpw:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned