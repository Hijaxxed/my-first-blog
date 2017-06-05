from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

def post_list(request):
    
    
    

#search bar - not filtering
    posts = Post.objects.all()#.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    query = request.GET.get("q")
    
    if query:
        posts = posts.filter(       
				Q(title__icontains=query)|
				Q(text__icontains=query)
				#Q(user__first_name__icontains=query) |
				#Q(user__last_name__icontains=query)
				).distinct()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


        

    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')        
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

def home_page(request):
    feed = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:3]
    
    
    return render(request, 'blog/home.html',{'feed':feed})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
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
            #post.published_date = timezone.now()
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


