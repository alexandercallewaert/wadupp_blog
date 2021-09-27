from django import forms
from .models import Post, Category, Comment

from django.forms import ModelForm


#categories = [('Hong Kong', 'Hong Kong'), ('Thailand, Phuket', 'Thailand, Phuket')]
categories = Category.objects.all().values_list('name', 'name')

categories_list = []


for item in categories:
	categories_list.append(item)

class add_post_form(ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'title_tag', 'category', 'body', 'snippet', 'header_image', 'image2', 'image3']


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'title_tag', 'author', 'category', 'body', 'snippet', 'header_image', 'image2', 'image3')

		widgets = {
			'title': forms.TextInput(attrs = {'class': 'form-control'}),
			'title_tag': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': "Tab Name"}),
			'author': forms.TextInput(attrs = {'class': 'form-control', 'value': "", 'id': 'x', 'type': 'hidden'}),
			#'author': forms.Select(attrs = {'class': 'form-control'}),
			'category': forms.Select(choices = categories_list, attrs = {'class': 'form-control'}),
			'body': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': "Text"}),
			'snippet': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': "Here comes the summary of your blog post which will appear on the home page"}),
		}


class EditForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'title_tag', 'category', 'body', 'snippet')

		widgets = {
			'title': forms.TextInput(attrs = {'class': 'form-control'}),
			'title_tag': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': "Tab Name"}),
			#'author': forms.Select(attrs = {'class': 'form-control'}),
			'category': forms.Select(choices = categories_list, attrs = {'class': 'form-control'}),
			'body': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': "Text"}),
			'snippet': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': "Here comes the summary of your blog post which will appear on the home page"}),

		}



class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']

		widgets = {
			'your_name': forms.TextInput(attrs = {'class': 'form-control'}),
			'body': forms.Textarea(attrs = {'class': 'form-control'}),

		}


