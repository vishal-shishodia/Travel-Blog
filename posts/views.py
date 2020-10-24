from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count,Q
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate

from .models import *
from .forms import *

def get_category_count():
	queryset=Post.objects.values('category__title').annotate(Count('category__title'))
	return queryset

def search(request):
	querset=Post.objects.all()
	query=request.GET.get('q')
	if query:
		queryset=querset.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)
			).distinct()
	context={'queryset':queryset}
	return render(request,'search_results.html',context)

def SignUp(request,*args):
	if request.POST:
		email=request.POST['email']
		new_signup=Signup()
		new_signup.email=email
		new_signup.save()

def Register(request):
	if request.POST:
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			username=form.cleaned_data.get('username')
			password=form.cleaned_data.get('password1')
			form.save()
			user=authenticate(username=username,password=password)
			if user:
				login(request,user)
				return redirect('index')
	else:
		form=UserCreationForm()
	context={'form':form}
	return render(request,'register.html',context)


def index(request):
	context={}
	category_count=get_category_count()
	posts=Post.objects.filter(featured=True)
	list_post=Post.objects.filter(listing=True)
	
	SignUp(request)
	context['posts']=posts
	context['list_post']=list_post
	context['category_count']=category_count
	return render(request,'index.html',context)

def DetailView(request,pk):
	most_recent=Post.objects.order_by('-timestamp')[:3]
	post=get_object_or_404(Post,pk=pk)
	comments=Comment.objects.filter(post=post)
	context={'post':post,
	'most_recent':most_recent,
	'comments':comments,
	
	}
	return render(request,'post.html',context)
	
def postComment(request):
	if request.method == "POST":
		comment = request.POST.get("comment")
		user = request.user
		postID = request.POST.get("postID")
		post = Post.objects.get(id=postID)
		parentID = request.POST.get("parentID")

		if parentID == "":
			comment = Comment(
			comment=comment,
			user=user,
			post=post
			)
		else:
			parent = Comment.objects.get(id=parentID)
			comment = Comment(
			comment=comment,
			user=user,
			post=post,
			parent=parent
			)

	comment.save()

	return redirect(f'/detail/{postID}/')
		
		
def get_author(user):
	qs = Author.objects.filter(user=user)
	if qs.exists():
		return qs[0]
	return None
		
def ListView(request):
	posts=Post.objects.all()
	most_recent=Post.objects.order_by('-timestamp')[:3]
	post_cat=get_category_count()
	paginator = Paginator(posts,2)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)
	
	context={'queryset':paginated_queryset,
	'most_recent':most_recent,
	'page_request_var': page_request_var,
	'post_cat':post_cat,
	}
	SignUp(request)
	return render(request,'listing.html',context)



def PostCreate(request):
	title='Create'
	form=PostForm(request.POST or None, request.FILES or None)
	author=get_author(request.user)
	print(author)
	if request.POST:
		if form.is_valid():
			form.instance.author=author
			form.save()
			return redirect(reverse('detail',kwargs={'pk':form.instance.pk}))
	context={'form':form,'title':title}
	return render(request,'post_create.html',context)

def PostDelete(request,pk):
	post=get_object_or_404(Post,pk=pk)
	post.delete()
	return redirect(reverse('index'))

def PostUpdate(request,pk):
	title='Update'
	post=get_object_or_404(Post,pk=pk)
	form=PostForm(request.POST or None, request.FILES or None,instance=post)
	author=Author.objects.get(user=request.user)
	if request.POST:
		if form.is_valid():
			form.instance.author=author
			form.save()
			return redirect(reverse('detail',kwargs={'pk':form.instance.pk}))
	context={'form':form,'title':title}
	return render(request,'post_create.html',context)
