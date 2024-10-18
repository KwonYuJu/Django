from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Comment
from .forms import MovieForm, CommentForm

from django.views.decorators.http import (
    require_http_methods, # GET & POST요청 # create, update
    require_safe, # GET요청 # index, detail
    require_POST, # POST요청 # delete
)

# 전체 영화 데이터 조회
@require_safe
def index(request):
  movies = Movie.objects.all()
  context = {
    "movies" : movies,
  }
  return render(request, 'movies/index.html', context)

# 단일 영화 데이터 조회
@require_safe
def detail(request, pk):
  movie = Movie.objects.get(pk=pk)
  comment_form = CommentForm()
  comments = movie.comment_set.all()
  context = {
    'movie' : movie,
    'comment_form' : comment_form,
    'comments' : comments,
  }
  return render(request, 'movies/detail.html', context)

# 영화 등록
@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
  if request.method == 'POST':
    form = MovieForm(request.POST, request.FILES)
    if form.is_valid():
      movie = form.save(commit=False)
      movie.user = request.user
      movie.save()
      return redirect('movies:detail', movie.pk)
  else:
    form = MovieForm()
  context = {
    'form' : form,
  }
  return render(request, 'movies/create.html', context)

# 영화 수정
@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
  movie = Movie.objects.get(pk=pk)
  if request.user == movie.user:
    if request.method == 'POST':
      form = MovieForm(request.POST, request.FILES, instance=movie)
      if form.is_valid():
        movie = form.save()
        return redirect('movies:detail', movie.pk)
    else:
      form = MovieForm(instance=movie)
  else:
    return redirect('movies:index')
  context = {
    'movie': movie,
    'form' : form, 
  }
  return render(request, 'movies/update.html', context)

# 영화 삭제
@login_required
@require_POST
def delete(request, pk):
  movie = Movie.objects.get(pk=pk)
  if request.user == movie.user:
    movie.delete()
    return redirect('movies:index')
  return redirect('movies:detail', movie.pk)

# 댓글 생성
@login_required
@require_POST
def comments_create(request, pk):
  movie = Movie.objects.get(pk=pk)
  comment_form = CommentForm(request.POST)
  if comment_form.is_valid():
    comment = comment_form.save(commit=False)
    comment.movie = movie 
    comment.user = request.user 
    comment.save()  
    return redirect('movies:detail', movie.pk)
  context = {
    'movie' : movie,
    'comment_form' : comment_form,
  }
  return render(request, 'movies/detail.html', context)

# 댓글 삭제
@login_required
@require_POST
def comments_delete(request, movie_pk, comment_pk):
  comment = Comment.objects.get(pk=comment_pk)
  if request.user == comment.user:
    comment.delete()
  return redirect('movies:detail', movie_pk)

# 좋아요
@login_required
@require_POST
def likes(request, movie_pk):
  movie = Movie.objects.get(pk=movie_pk)
  if request.user in movie.like_users.all():
    movie.like_users.remove(request.user)
  else:
    movie.like_users.add(request.user)
  return redirect('movies:index')