from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from datetime import datetime
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Images, SaveData
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import modelformset_factory

# def home(request):
#     return HttpResponse("my first program")
#
#
# def current_datetime(request):
#     html="<html><body>It is now <b>%s</b>.</body></html>" % datetime.now()
#     return HttpResponse(html)

# for showin list page by default...


def post_list(request):
    global start_index, start_index
    post_list = Post.published.all()
    query = request.GET.get('q')
    if query:
       # posts = Post.published.filter(title__icontains=query) for simple query....
       post_list = Post.published.filter(
            Q(title__icontains=query)|
            Q(author__username=query)|
            Q(body__icontains=query)
        ) # for multiple search.....
        #for pagination
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 7
    else:
        (stat_index, end_index) = proper_pagination(posts, index=4)

    page_range = list(paginator.page_range)[start_index:end_index]
    #[1,2,3,4,5,6,7,8,9,10][0:7]

    context = {
        'posts': posts,
        'page_range': page_range,
    }
    return render(request, 'blog/post_list.html', context)


def proper_pagination(posts, index):
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number - index
        end_index =start_index + end_index
    return (start_index, end_index)

# for show detail page...
def post_detail(request, id, slug):
    post = Post.objects.get(id=id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)



def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if  form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return HttpResponseRedirect(reverse('post_list'))
    else:
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_create.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse("user is not active")
            else:
                return HttpResponse("user is None")
    else:
        form = UserLoginForm()
        context ={
            'form':form,
        }
        return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('post_list')


def register(request):
    if request.method =='POST':
        form =UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('post_list')

    else:
         form = UserRegistrationForm()
    context = {
        'form':form,
        }
    return render(request,'registration/register.html',context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form=ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse("blog:edit_profile"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)

    context ={
            'user_form': user_form,
            'profile_form':profile_form
    }
    return render(request,'blog/edit_profile.html',context)


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())

    else:
        form = PostEditForm(instance=post)
    context = {
        'form':form,
        'post':post,
    }
    return render(request, 'blog/post_edit.html', context)


def post_delete(request, id):
    posts = Post.published.all()
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    context={
        'posts':posts,
    }
    return render(request, 'blog/post_list.html',context)


def save_data(request):
    show = SaveData.objects.all()
    context = {
        'show': show,
    }
    if request.method == 'POST':
        query = request.POST['cost']
        if query:
            store=SaveData(cost = query)
            store.save()
            return render(request, 'blog/save_data.html', context)
    else:
        return render(request, 'blog/save_data.html', context)


def edit_save_data(request, id):
    post = get_object_or_404(SaveData, id=id)
    if request.method == 'POST':
        cost = request.POST['cost']
        date = request.POST['date']
        SaveData.objects.filter(id=id).update(cost=cost,date=date)
        return HttpResponseRedirect(reverse('blog:save_data'))
    else:
        show = SaveData.objects.get(id = id)
        context ={
         'show':show
        }
        return render(request, 'blog/edit_save_data.html',context)



def delete_save_data(request, id):
    show = SaveData.objects.all()
    context = {
        'show': show,
    }
    post = get_object_or_404(SaveData, id=id)
    post.delete()
    return render(request, 'blog/save_data.html',context)