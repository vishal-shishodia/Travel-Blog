from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	about = models.CharField(max_length=100,blank=True,null=True)
	profile_picture = models.ImageField()

	def __str__(self):
		return self.user.username

class Signup(models.Model):
	email = models.EmailField(max_length=50,unique=True)

	def __str__(self):
		return self.email

class Category(models.Model):
	title = models.CharField(max_length=20)

	def __str__(self):
		return self.title


class Country(models.Model):
	name = models.CharField(max_length=20)
	place = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=100,blank=False,null=False)
	content = models.CharField(max_length=300,blank=False,null=False)
	author = models.ForeignKey(Author,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	country = models.ForeignKey(Country,on_delete=models.CASCADE,default=None)
	thumbnail = models.ImageField()
	featured = models.BooleanField()
	listing = models.BooleanField()
	previous_post = models.ForeignKey(
	'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
	next_post = models.ForeignKey(
	'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('detail',kwargs={'pk':self.pk})

	@property
	def comment_count(self):
		return Comment.objects.filter(post=self).count()


class Comment(MPTTModel):
	comment = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,related_name="children",)
	posted_on = models.DateTimeField(auto_now_add=True)

	class MPTTMeta:
		order_insertion_by = ['posted_on']

	def __str__(self):
		return self.comment[:15] + "... by " + str(self.user.username)
	

