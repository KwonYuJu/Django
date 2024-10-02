from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import (
  AuthenticationForm, # 로그인을 위한 폼(id, password 입력)
  UserCreationForm, # 계정 생성을 위한 폼(id, password, password 확인)  
  PasswordChangeForm # 비밀번호 변경 폼(현재 password, 새 password)
)
# 로그인, 로그아웃 기능 사용
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash

from .models import User

# login_required 데코레이터
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomUserChangeForm

def index(request):
  persons = User.objects.all()
  context = {
    'persons' : persons
  }
  return render(request, 'accounts/index.html', context)

def login(request):
  if request.method == 'POST': # 로그인 버튼 눌렀을 때
    # AuthenticationForm : 첫 번째 인자 ---> request
    # request : HTTP 요청 전체 정보 
    # request.POST : 사용자가 입력한 ID, Password
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      # 유효성 검사 통과하면 사용자 로그인 처리
      # get_user() : 인증된 사용자의 객체 반환
      # 이미 존재하는 사용자를 인증(signup과의 차이)
      auth_login(request, form.get_user())
      return redirect('articles:index')# 메인 페이지로 리다이렉트
  else: # 로그인 버튼 누르기 전
    form = AuthenticationForm() # 빈 폼
  # 유효성 검사 실패
  context = {
    'form' : form
  }
  return render(request, 'accounts/login.html', context)

# 로그인을 하지 않은 상태에서 로그아웃 URL 접근하는 것을 방지
# 보안성 : 로그인한 사용자만 로그아웃 할 수 있도록
@login_required
def logout(request):
  auth_logout(request)  # 사용자 로그아웃
  return redirect('articles:index') # 메인 페이지로 리다이렉트

def signup(request):
  # is_authenticated 속성 : 이미 인증된 사용자라면
  if request.user.is_authenticated:
    return redirect('articles:index')
  
  if request.method == "POST":  # 제출 버튼을 눌렀을 때
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():         # 1. 유효성 검사
      user = form.save()        # 2. DB에 저장
      auth_login(request, user) # 3. 로그인
      return redirect('articles:index')
  else: # 제출 버튼을 누르기 전 -> 빈 폼
    form = CustomUserCreationForm()
  # 유효성 검사 실패
  context = {
    'form' : form,
  }
  return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
  # request.user : 현재 로그인 되어있는 user
  request.user.delete()
  # auth_logout(request)
  return redirect('articles:index')

@login_required
def update(request):
  if request.method == "POST":
    form = CustomUserChangeForm(request.POST, instance=request.user)
    if form.is_valid():        
      form.save()       
      return redirect('articles:index')
  else: # 회원 정보 변경 버튼을 누르기 전
    form = CustomUserChangeForm(instance=request.user)
  context = {
    'form' : form,
  }
  return render(request, 'accounts/update.html', context)

@login_required
def change_password(request, user_pk):
  if request.method == "POST":
    # 첫번째 인자는 user, 두번째 인자는 데이터
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():        
      user = form.save()       
      # 세션 무효화 방지(자동 로그아웃 방지)
      # hash 함수로 현재 사용자의 인증 세션 갱신
      update_session_auth_hash(request, user)
      return redirect('articles:index')
  else:
    form = PasswordChangeForm(request.user)
  context = {
    'form' : form,
  }
  return render(request, 'accounts/change_password.html', context)