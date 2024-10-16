from django.urls import path
from articles import views

# app_name은 이제 안쓴다 -> templates 없기 때문에

urlpatterns = [
    # 전체 게시글 조회
    path('articles/', views.article_list),
    # 단일 게시글 조회
    path('articles/<int:article_pk>/', views.article_detail),
]
