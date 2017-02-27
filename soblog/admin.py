from django.contrib import admin
from soblog.models import *
from pagedown.widgets import AdminPagedownWidget
from django import forms

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Blog
        fields = '__all__'

class BlogAdmin(admin.ModelAdmin):
    form = BlogForm

admin.site.register(Blog,BlogAdmin)
admin.site.register(Catagory)
admin.site.register(Comment)