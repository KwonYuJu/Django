from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),    # 전체 영화 데이터 조회
    path('detail/<int:pk>/', views.detail, name='detail'),  # 단일 영화 데이터 조회
    path('create/', views.create, name='create'),   # 영화 등록
    path('update/<int:pk>/', views.update, name='update'),    # 영화 수정
    path('delete/<int:pk>/', views.delete, name='delete'),    # 영화 삭제
    path('comments/<int:pk>/', views.comments_create, name='comments_create'),  # 댓글 생성
    path('comments/<int:movie_pk>/delete/<int:comment_pk>/',  # 댓글 삭제
         views.comments_delete, name='comments_delete'),
    path('likes/<int:movie_pk>/', views.likes, name='likes'), # 좋아요
] 