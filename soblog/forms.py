#coding:utf-8
from django import forms
from soblog.models import *
from django.contrib.auth.forms import PasswordChangeForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content','created')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar',]

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','author','content','catagory','tags')

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm,self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})