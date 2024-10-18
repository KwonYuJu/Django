from django.shortcuts import render, redirect

from django.contrib.auth.forms import (
    AuthenticationForm, # 로그인 폼
    UserCreationForm,   # 계정생성 폼
    PasswordChangeForm, # 비밀번호 변경 폼
)

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash

from .models import User

from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.views.decorators.http import (
    require_http_methods, # GET & POST요청 # login, signup, update, change_password
    require_POST, # POST요청 # logout, delete
)

# 로그인
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/login.html', context)

# 로그아웃
@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

# 회원가입
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

# 회원 탈퇴
@login_required
@require_POST
def delete(request):
    request.user.delete()
    return redirect('movies:index')

# 회원정보 수정
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/update.html', context)

# 비밀번호 변경
@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request, user_pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/change_password.html', context)


from django.contrib.auth import get_user_model

# 개인 프로필
@login_required
@require_http_methods(['GET', 'POST'])
def profile(request, username):
  User = get_user_model()
  person = User.objects.get(username=username)
  context = {
    'person' : person
  }
  return render(request, 'accounts/profile.html', context)

# 팔로잉
@login_required
@require_POST
def follow(request, user_pk):
  User = get_user_model()
  person = User.objects.get(pk=user_pk)
  if person != request.user:
    if person.followers.filter(pk=request.user.pk).exists():
      person.followers.remove(request.user)
    else:
      person.followers.add(request.user)
  return redirect('accounts:profile', person.username)