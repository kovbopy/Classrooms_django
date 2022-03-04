from django.forms import ModelForm
from base.models import Users, Classroom
from django import forms


class UserRegisterForm(ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Users.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        exclude = ['slug', 'updated', 'created']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Classroom name'}),
                   'description': forms.Textarea(attrs={'rows': 3})}

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        r = Classroom.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Classroom name already exists")
        return name


class UpdateUserForm(ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['username', 'password', 'picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widgets.attrs.update({'class': 'form-control', 'placeholder': 'Your name'})
        self.fields['username'].label = 'Update Username'
        self.fields['password'].widgets.attrs.update({'class': 'form-control', 'placeholder': 'Your password'})
        self.fields['password'].label = 'Update Password'

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Users.objects.filter(username=username)
        if r.exists():
            raise forms.ValidationError("Username already exists")
        return username