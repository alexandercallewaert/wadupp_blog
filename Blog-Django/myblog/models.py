from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.urls import reverse
from datetime import datetime, date #python date stuff we can import
from ckeditor.fields import RichTextField




class User(AbstractUser):
   Allow_to_post = models.BooleanField(default=False)





#
# class allow_user_to_post(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	allow_to_post = models.BooleanField(default=False)
#
# 	def __str__(self):
# 		return self.user.username



class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home')
		#return reverse('article-detail', args = (str(self.id)))


class Profile(models.Model):
	user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
	bio = models.TextField()
	profile_pic = models.ImageField(null = True, blank = True, upload_to = "images/profile")
	polarsteps_url = models.CharField(max_length=255, null = True, blank = True)
	instagram_url = models.CharField(max_length=255, null = True, blank = True)
	facebook_url = models.CharField(max_length=255, null = True, blank = True)
	linkedin_url = models.CharField(max_length=255, null = True, blank = True)


	def __str__(self):
		return str(self.user)

	def get_absolute_url(self):
		return reverse('home')


class Post(models.Model):
	title = models.CharField(max_length=255)
	header_image = models.ImageField(null = True, blank = True, upload_to = "images/")
	image2 = models.ImageField(null = True, blank = True, upload_to = "images/")
	image3 = models.ImageField(null = True, blank = True, upload_to = "images/")
	title_tag = models.CharField(max_length=255)
	author = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
	body = RichTextField(blank = True, null = True)
	#body = models.TextField()
	post_date = models.DateField(auto_now_add=True)
	# category = models.CharField(max_length=255, default = "Hong Kong")
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	snippet = models.CharField(max_length=255)
	likes = models.ManyToManyField(User, related_name = 'blog_posts', blank=True)


	def total_likes(self):
		return self.likes.count()


	def __str__(self):
		return self.title + ' | ' + str(self.author)

	def get_absolute_url(self):
		#return reverse('article-detail', args = (str(self.id)))
		return reverse('home')


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name = "comments", on_delete=models.CASCADE)
	your_name = models.CharField(max_length = 255)
	body = models.TextField()
	date_added = models.DateTimeField(auto_now_add = True)


	def __str__(self):
		return '%s - %s' % (self.post.title, self.your_name)


