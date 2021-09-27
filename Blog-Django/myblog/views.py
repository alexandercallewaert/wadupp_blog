from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm, add_post_form
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from myblog.models import User
from django.contrib import messages


@csrf_exempt
def get_country(request):
	all_Category = Category.objects.all().order_by('name')
	get_cat_seri = serializers.serialize('json', all_Category)
	return JsonResponse(get_cat_seri, safe=False)



@csrf_exempt
def get_bloggers(request):

	all_usr = User.objects.all()

	bloggers = []
	for i in all_usr:
		if Post.objects.filter(author=i):
			bloggers.append(i)

	print(bloggers)

	get_cat_seri = serializers.serialize('json', bloggers)
	return JsonResponse(get_cat_seri, safe=False)



def author_all_posts(request, pk):
	print(pk)
	get_user = User.objects.get(id=pk)

	all_post_of_this_usr = Post.objects.filter(author=get_user)
	context = {'all_post_of_this_usr':all_post_of_this_usr, 'get_user':get_user}
	return render(request, 'author_all_posts.html', context)

def LikeView(request, pk):
	post = get_object_or_404(Post, id = request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id = request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else: 
		post.likes.add(request.user)
		liked = True

	return HttpResponseRedirect(reverse('article-detail', args = [str(pk)]))



def index(request):
	print('all_post')
	all_post = Post.objects.all()
	print(all_post)
	context={'all_post':all_post}
	return render(request, 'home.html', context)


class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	ordering = ['-post_date']
	#ordering = ['-id']

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(HomeView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context


def CategoryView(request, cats):
	print(cats)
	get_cat = Category.objects.get(id=cats)
	category_posts = Post.objects.filter(category = cats)
	return render(request, 'categories.html', {'cats': cats.title(), 'category_posts': category_posts, 'get_cat':get_cat})


#def CategoryView2(request, bloggers):
	#category2_posts = Post.objects.filter(author = bloggers)
	#return render(request, 'bloggers.html', {'bloggers': bloggers, 'category2_posts': category2_posts})


class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args, **kwargs):
		print('ck')
		cat_menu = Category.objects.all()
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
		
		stuff = get_object_or_404(Post, id = self.kwargs['pk'])
		total_likes = stuff.total_likes()
		
		liked = False
		if stuff.likes.filter(id = self.request.user.id).exists():
			liked = True

		context["cat_menu"] = cat_menu
		context["total_likes"] = total_likes
		context["liked"] = liked
		return context


class AddPostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'add_post.html'
	#fields = '__all__'


def add_post(request):
	if request.method == 'POST':
		form = add_post_form(request.POST, request.FILES)
		if form.is_valid():
			other_value = form.save(commit=False)
			other_value.author=request.user
			other_value.save()
			messages.success(request, 'Successfully Added !!')
			return redirect('add_post')
		else:
			messages.success(request, 'Fail to Add !!')
			return redirect('add_post')
	else:
		form = add_post_form()
		print(form)
		context = {'form':form}
		return render(request, 'add_post.html', context)


def add_comments(request, pk):
	get_post = Post.objects.get(id=pk)
	print(get_post)
	context = {'get_post':get_post}
	return render(request, 'add_comment.html', context)


def save_comment(request):
	post_id = request.POST.get('post_id')
	name = request.POST.get('name')
	comment = request.POST.get('comment')

	print(post_id, name, comment)

	get_post = Post.objects.get(id=post_id)

	save_comnt = Comment(post=get_post, your_name=name, body=comment)
	save_comnt.save()


	return redirect('article-detail', post_id)



class AddCommentView(CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'add_comment.html'
	#fields = '__all__'

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)
	success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
	model = Category
	#form_class = PostForm
	template_name = 'add_category.html'
	fields = '__all__'


class UpdatePostView(UpdateView):
	model = Post
	form_class = EditForm
	template_name = 'edit_post.html'
	#fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')