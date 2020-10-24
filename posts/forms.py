from django import forms
from .models import *


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'country', 'content', 'thumbnail', 
		'category', 'featured', 'previous_post', 'next_post','listing',)


