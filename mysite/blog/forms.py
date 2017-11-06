# -*- coding:utf-8 -*-
from django import forms
from .models import Comment
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

'''
class CommentForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
 '''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "名字",}),
            'email':forms.TextInput(attrs={'placeholder': "邮件"}),
            'body': forms.Textarea(attrs={'placeholder': '请留下您的评论'})
        }
