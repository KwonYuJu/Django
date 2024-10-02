from django.shortcuts import render, redirect
# 현재 디렉토리의 models.py로부터 Article 모델을 가져오겠다.
from .models import Article
from .forms import ArticleForm

def index(request):
  # QuerySet API -> 전체 데이터 조회 : Article.objects.all()
  articles = Article.objects.all()

  context = {
    'articles' : articles,
  }

  return render(request, 'articles/index.html', context)

# 단일 게시글 페이지 랜더링
def detail(request, pk):
  # QuerySet API -> 단일 데이터 조회 : get
  article = Article.objects.get(pk=pk)
  context = {
    'article' : article,
  }
  return render(request, 'articles/detail.html', context)

'''
# 게시글 생성
# 페이지 렌더링
def new(request):
  return render(request, 'articles/new.html')

# render와 redirect 차이
# render : 사용자에게 새로운 페이지를 보여줄 때 사용
# redirect : 데이터 처리 후 다른 페이지로 이동할 때 사용

# 페이지 리다이렉트(데이터를 받아서 DB에 저장 - POST 방식)
def create(request):
  # create 2번 방법 사용, 3번 방법은 절대 사용 x
  # GET 방식은 데이터가 url에 노출 -> 데이터를 조회, 검색
  # POST 방식은 보안성(csrf 토큰) -> 데이터를 생성, 수정, 삭제
  title = request.POST.get('title')
  content = request.POST.get('content')

  # 저장 -> 2번 방법(코드가 간결하면서 안정적)
  article = Article(title=title, content=content)
  # 데이터 관리(저장) 원칙 : 안정성
  # save 하기 전에 유효성 검사
  article.save()

  # 게시글 생성하고(데이터 변경), 생성버튼 누르고 어떤 페이지로 이동할건가?
  # 클라이언트가 GET 요청을 다시 한번 더 보내도록 한다(redirect). 
  # 데이터가 변경 되었을 때 
  return redirect('articles:detail', article.pk)
'''

def create(request):
  # 게시글 생성 버튼을 눌렀을 때
  if request.method == 'POST':
    form = ArticleForm(request.POST, request.FILES)
    # 유효성 검사 대표 2가지
    # 1. 모든 필수 필드가 채워져 있는지
    # 2. 입력된 데이터가 필드의 조건(ex. 데이터 형식)을 만족 하는지
    if form.is_valid():
      article = form.save()
      # create 함수 부분(데이터가 변경됨)
      return redirect('articles:detail', article.pk)

  # 게시글 생성 버튼을 누르기 전 또는 다른 버튼을 눌렀을 때
  # 요청 메서드가 POST 방식이 아닐때(GET, PUT, DELETE 등 다른 메서드)
  else:
    form = ArticleForm()
  # 1. 유효성 검사 통과하지 못한 경우 -> 에러와 함께 폼 다시 표시
  # 2. GET 요청인 경우(빈 폼 표시)
  context = {
    'form' : form,
  }
  return render(request, 'articles/create.html', context)

# 게시글 삭제
# 단일 게시글 조회 후 삭제
# 데이터 변경 -> redirect
def delete(request, pk):
  article = Article.objects.get(pk=pk)
  article.delete()
  # 여기서 request는 POST 방식 -> DB 변경하니까
  return redirect('articles:index')

'''
# 게시글 수정
# 페이지 렌더링(create와 차이 : 기존에 있던 게시글을 조회)
def edit(request, pk):
  article = Article.objects.get(pk=pk)
  context = {
    'article' : article
  }
  return render(request, 'articles/edit.html', context)

# 페이지 리다이렉트(create와 차이 : 기존에 있던 게시글을 변경)
def update(request, pk):
  article = Article.objects.get(pk=pk)

  article.title = request.POST.get('title')
  article.content = request.POST.get('content')

  article.save()

  return redirect('articles:detail', article.pk)
'''

# 단일 게시글 조회하고 변경, 저장
def update(request, pk):
  # 조회 먼저 하고
  article = Article.objects.get(pk=pk)
  if request.method == 'POST':
    # 기존 게시글의 데이터를 미리 채운다(instance=article)
    form = ArticleForm(request.POST, request.FILES , instance=article)
    if form.is_valid():
      form.save()
      return redirect('articles:detail', article.pk)
  # 변경 버튼 누르기 전 또는 다른 버튼 눌렀을 때
  else:
    form = ArticleForm(instance=article)
  context = {
    # article은 기존에 존재했던 데이터
    'article': article,
    'form': form,
  }
  return render(request, 'articles/update.html', context)

