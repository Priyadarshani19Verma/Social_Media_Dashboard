from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db import models
from .models import Profile, Post, Comment, Like
from .forms import PostForm, CommentForm

# API Fetch Functions (Optional)
from .utils.twitter_api import get_tweets
from .utils.facebook_api import get_facebook_posts


# Register New Users
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'dashboard/register.html', {'form': form})


#  Login Users
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/login.html', {'form': form})


# Logout User
def logout_view(request):
    logout(request)
    return redirect('login')


# Main Dashboard View
@login_required
def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    twitter_username = profile.twitter_username

    posts = Post.objects.all().order_by('-created_at')
    tweets = get_tweets(twitter_username)
    fb_posts = get_facebook_posts() 

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('dashboard')
    else:
        post_form = PostForm()

    #  Basic Analytics
    total_posts = Post.objects.filter(user=request.user).count()
    total_likes = Like.objects.filter(post__user=request.user).count()
    total_comments = Comment.objects.filter(post__user=request.user).count()

    top_post = Post.objects.filter(user=request.user).annotate(
        like_count=models.Count('likes') 
    ).order_by('-like_count').first()


    return render(request, 'dashboard/dashboard.html', {
        'tweets': tweets,
        'fb_posts': fb_posts, 
        'posts': posts,
        'post_form': post_form,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'top_post': top_post,
    })


#  Like Post
@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.get_or_create(user=request.user, post=post)
    return redirect('dashboard')


#  Comment on Post
@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('dashboard')


#  Edit Comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return HttpResponseForbidden("You can't edit this comment.")

    if request.method == 'POST':
        new_text = request.POST.get('text')
        comment.text = new_text
        comment.save()
        return redirect('dashboard')

    return render(request, 'dashboard/edit_comment.html', {'comment': comment})


#  Delete Comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return HttpResponseForbidden("You can't delete this comment.")

    if request.method == 'POST':
        comment.delete()
        return redirect('dashboard')

    return render(request, 'dashboard/delete_comment.html', {'comment': comment})
