from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm


# Home page view with pagination and bloggers
def home(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    bloggers = User.objects.all()
    return render(request, 'home.html', {'posts': posts, 'bloggers': bloggers})


# List all blog posts
def blog_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog_list.html', {'posts': posts})


# Blog post detail with comments, likes, and dislikes
def blog_detail(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    comments = post.comments.order_by('created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Your comment has been added!")
                return redirect('blog_detail', blog_id=post.id)
        else:
            messages.error(request, "You need to log in to comment.")
            return redirect('login')
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'likes_count': post.total_likes(),
        'dislikes_count': post.total_dislikes(),
        'liked': request.user in post.likes.all(),
        'disliked': request.user in post.dislikes.all(),
    }

    return render(request, 'blog_detail.html', context)


# Create a new blog post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, "Your blog post has been created successfully!")
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


# Update an existing blog post
@login_required
def update_post(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)

    if request.user != post.author:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('blog_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your blog post has been updated!")
            return redirect('blog_detail', blog_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'update_post.html', {'form': form, 'post': post})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post


@login_required
def delete_post_confirm(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')  # Redirect after successful deletion

    # Render the correct confirmation page
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# User registration with signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created successfully.")
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# Separate register view (redirects to login after registration)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# Author detail page with their posts
def author_detail(request, author_id):
    author = get_object_or_404(User, pk=author_id)
    posts = Post.objects.filter(author=author).order_by('-created_at')
    return render(request, 'author_detail.html', {'author': author, 'posts': posts})


# List all bloggers
def blogger_list(request):
    bloggers = User.objects.all()
    return render(request, 'blogger_list.html', {'bloggers': bloggers})


# Like a post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
        liked = True

    return JsonResponse({'likes': post.total_likes(), 'dislikes': post.total_dislikes(), 'liked': liked})


# Dislike a post
@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
        disliked = True

    return JsonResponse({'likes': post.total_likes(), 'dislikes': post.total_dislikes(), 'disliked': disliked})

from django.shortcuts import render
from django.db.models import Q
from .models import Post


def search_results(request):
    query = request.GET.get('q')
    results = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
    )

    return render(request, 'search_results.html', {'query': query, 'results': results})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

def blog_detail(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    return render(request, 'blog_detail.html', {'post': post})

@login_required
def add_comment(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
    return redirect('blog_detail', blog_id=post.id)
