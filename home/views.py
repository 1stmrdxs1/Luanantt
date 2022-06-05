from email import message
from imaplib import _Authenticator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from matplotlib.style import context
from django.db.models import Q
from .models import Comment, Post, Topic, User
from .forms import PostForm, UserForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

# Create your views here.

#Dang nhap
def loginPage(request):
    page = 'login'


    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context ={'page':page}
    return render(request, 'base/login_register.html', context)


#Dang xuat
def logoutUser(request):
    logout(request)
    return redirect('home')
#Dang ki
def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html',{'form':form})


#Trang chu
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    post_count = posts.count()
    post_comments = Comment.objects.filter(Q(post__topic__name__icontains=q))

    context = {'posts': posts, 'topics': topics, 'post_count': post_count,'post_comments': post_comments}
    return render(request, 'base/home.html',context )

#Post
def post(request,pk):
    post = Post.objects.get(id = pk)
    post_comments = post.comment_set.all()
    participants = post.participants.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            post = post,
            body = request.POST.get('body')
        )
        post.participants.add(request.user)
        return redirect('post',pk=post.id)

    context = {'post': post,'post_comments':post_comments,'participants': participants}

    return render(request, 'base/post.html', context)

#like
def like(request,pk):
    post = Post.objects.get(id = pk)
    if post.liked.filter(id=request.user.id).exists():
        post.liked.remove(request.user)
    else:
        post.liked.add(request.user)
    return HttpResponseRedirect(reverse('post', args=[str(pk)]))

#Trang ca nhan
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    post_comments = user.comment_set.all()
    topics = Topic.objects.all()
    context ={'user': user, 'posts':posts,'post_comments': post_comments,'topics': topics}
    return render(request, 'base/profile.html', context)

#Post bai
@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Post.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form':form,'topics':topics}
    return render(request, 'base/post_form.html', context)

#Update Post
@login_required(login_url='login')
def updatePost(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    topics = Topic.objects.all()
    if request.user != post.host:
        return HttpResponse('You cannot do that')



    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = PostForm(request.POST, instance=post)
        post.name = request.POST.get('name')
        post.topic = topic
        post.description = request.POST.get('description')
        post.save()
        return redirect('home')

    context ={'form':form,'topics':topics,'post':post}
    return render(request, 'base/post_form.html', context)

#delete Post
@login_required(login_url='login')
def deletePost(request,pk):
    post = Post.objects.get(id=pk)



    if request.user != post.host:
        return HttpResponse('You cannot do that')

        
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':post})

#Delete cmt
@login_required(login_url='login')
def deleteComment(request,pk):
    comment = Comment.objects.get(id=pk)



    if request.user != comment.user:
        return HttpResponse('You cannot do that')

        
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':comment})

#update tai khoan ca nhan
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)



    if request.method == 'POST':
        form =UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)

    context = {'form':form}
    return render(request,'base/update-user.html',context)


#trang topic
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})


#trang doi password
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user-profile',pk=user.id)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base/change-password.html', {'form': form})