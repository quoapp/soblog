#coding:utf-8
from django import forms
from soblog.models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','content','created')

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Userinfo
#         fields = ('username','password','email')
#         # widgets = {
#         #     'password':forms.PasswordInput()
#         # }

class BlogForm(forms.ModelForm):
      class Meta:
        model = Blog
        fields = ('title','author','content','catagory','tags')

# class CatagoryForm(ModelForm):
#     class Meta:
#         model = Catagory
#         fields = ('name',)
#
# class TagForm(ModelForm):
#     class Meta:
#         model = Tag
#         fields = ('name',)