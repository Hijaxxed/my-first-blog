from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

# Create your views here.

def post_list(request):
   
    posts = Post.objects.all()
    
    query = request.GET.get("q")    
    if query:
        posts = posts.filter(Q(title__icontains=query)|Q(text__icontains=query)).distinct()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
          
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('post_detail', slug=slug)

def post_remove(request, slug):
    post = get_object_or_404(Post,slug=slug)
    post.delete()
    return redirect('post_list')

def about_page(request):
    return render(request, 'blog/about.html')

def contact_page(request):
    return render(request, 'blog/contact.html')

def home_page(request):
    feed = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:3]
        
    return render(request, 'blog/home.html',{'feed':feed})


def category_list(request):
    categories = Category.objects.all()

    return render (request, 'blog/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
     
    posts = Post.objects.all().filter(categories=category)

    return render(request, 'blog/category_detail.html',{'category': category , 'posts': posts})

def gamedev_home(request):
    return render(request, 'blog/gamedev_home.html')



@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            #form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.categories = post.categories.category
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})



@login_required
def comment_remove(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    post_slug = comment.post.slug
    comment.delete()
    return redirect('post_detail',slug=post.slug)


