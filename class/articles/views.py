from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# 현재 디렉토리의 models.py로부터 Article, Comment 모델을 가져오겠다.
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

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
  comment_form = CommentForm()

  # comment_set -> 역참조
  # 게시글에 달린 모든 댓글을 가져오기 위해서 (역참조)
  comments = article.comment_set.all()

  context = {
    'article' : article,
    'comment_form' : comment_form,
    'comments' : comments,
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

@login_required
def create(request):
  # 게시글 생성 버튼을 눌렀을 때
  if request.method == 'POST':
    form = ArticleForm(request.POST, request.FILES)
    # 유효성 검사 대표 2가지
    # 1. 모든 필수 필드가 채워져 있는지
    # 2. 입력된 데이터가 필드의 조건(ex. 데이터 형식)을 만족 하는지
    if form.is_valid():
      # 바로 DB에 자동으로 저장됨 -> request.user 정보(수동으로 저장) 
      # -> (commit=False)
      article = form.save(commit=False)
      # request.user -> 로그인한 사용자
      article.user = request.user
      article.save() # 최종적으로 DB에 저장
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
@login_required
def delete(request, pk):
  article = Article.objects.get(pk=pk)
  # request.user : 로그인한 사용자
  # article.user : 게시글 작성자
  # 로그인한 사용자랑 게시글 작성자랑 같을 때만 삭제할 수 있다
  if request.user == article.user: 
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
@login_required
def update(request, pk):
  # 조회 먼저 하고
  article = Article.objects.get(pk=pk)
  # 로그인한 사용자랑 게시글 작성자랑 같을 때만 수정할 수 있다
  if request.user == article.user:
    if request.method == 'POST':
      # 기존 게시글의 데이터를 미리 채운다(instance=article)
      form = ArticleForm(request.POST, request.FILES , instance=article)
      if form.is_valid():
        form.save()
        return redirect('articles:detail', article.pk)
    # 변경 버튼 누르기 전 또는 다른 버튼 눌렀을 때
    else:
      form = ArticleForm(instance=article)
  else:
    return redirect('articles:index')

  context = {
    # article은 기존에 존재했던 데이터
    'article': article,
    'form': form,
  }
  return render(request, 'articles/update.html', context)

# 댓글 생성
@login_required
def comments_create(request, pk):
  # 게시글 조회
  article = Article.objects.get(pk=pk)
  comment_form = CommentForm(request.POST)
  # 댓글 유효성 검사
  if comment_form.is_valid():
    # 댓글을 바로 DB에 저장? -> 2개 수동으로 저장
    comment = comment_form.save(commit=False)
    comment.article = article # 첫 번째 : 게시글의 외래키
    comment.user = request.user # 두 번째 : 로그인한 사용자(request.user)
    comment.save()  # DB에 수동으로 저장
    return redirect('articles:detail', article.pk)
  # 유효성 검사에 실패했으면
  context = {
    'article' : article,
    'comment_form' : comment_form,
  }
  return render(request, 'articles/detail.html', context)

# 댓글 삭제
@login_required
def comments_delete(request, article_pk, comment_pk):
  comment = Comment.objects.get(pk=comment_pk)
  if request.user == comment.user:
    comment.delete()

  return redirect('articles:detail', article_pk)