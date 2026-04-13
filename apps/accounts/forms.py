import re
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'phone', 'role']
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip().lower()
        names = [name for name in full_name.split() if name]
        if not (2 <= len(names) <= 3):
            raise forms.ValidationError('Full name must contain 2 or 3 names.')
        for name in names:
            if len(name) < 3:
                raise forms.ValidationError(f'Each part of the name ("{name}") must be at least 3 characters long.')
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if not username:
            raise forms.ValidationError('Username is required.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if not re.match(r'^[a-z][a-z0-9]*$', username):
            raise forms.ValidationError('Username must start with a letter and contain only letters or numbers.')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

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
        
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip().lower()
        names = [name for name in full_name.split() if name]
        if not (2 <= len(names) <= 3):
            raise forms.ValidationError('Full name must contain 2 or 3 names.')
        for name in names:
            if len(name) < 3:
                raise forms.ValidationError(f'Each part of the name ("{name}") must be at least 3 characters long.')
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if not username:
            raise forms.ValidationError('Username is required.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if not re.match(r'^[a-z][a-z0-9]*$', username):
            raise forms.ValidationError('Username must start with a letter and contain only letters or numbers.')
        if User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'phone']

    def __init__(self, *args, **kwargs):
        self.user_role = kwargs.pop('user_role', None)
        super().__init__(*args, **kwargs)
        # Non-admin users cannot change full_name
        if self.user_role != 'admin':
            self.fields.pop('full_name')
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip().lower()
        names = [name for name in full_name.split() if name]
        if not (2 <= len(names) <= 3):
            raise forms.ValidationError('Full name must contain 2 or 3 names.')
        for name in names:
            if len(name) < 3:
                raise forms.ValidationError(f'Each part of the name ("{name}") must be at least 3 characters long.')
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if not username:
            raise forms.ValidationError('Username is required.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if not re.match(r'^[a-z][a-z0-9]*$', username):
            raise forms.ValidationError('Username must start with a letter and contain only letters or numbers.')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


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
