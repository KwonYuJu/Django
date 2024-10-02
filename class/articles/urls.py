from django.urls import path

from . import views

app_name = 'articles'

urlpatterns = [
    # 전체 게시글 조회
    path('', views.index, name='index'),

    # 단일 게시글 조회(detail 페이지)
    # variable routing -> 단순히 조회 목적
    # 1. views.py 함수에서 pk를 매개변수로 받고
    # 2. url naming pattern에서 article.pk 받고
    path('<int:pk>/', views.detail, name='detail'),

    # 게시글 생성
    # 페이지 렌더링 + 리다이렉트
    path('create/', views.create, name='create'),

    # 게시글 삭제
    # variable routing -> 조회 후 삭제, 조회 후 수정
    path('<int:pk>/delete/', views.delete, name='delete'),

    # 게시글 수정
    # 페이지를 렌더링 + 리다이렉트
    path('<int:pk>/update/', views.update, name='update'),
]

