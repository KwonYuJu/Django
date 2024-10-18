from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),      # 로그인
    path('logout/', views.logout, name='logout'),   # 로그아웃
    path('signup/', views.signup, name='signup'),   # 회원가입
    path('delete/', views.delete, name='delete'),   # 회원탈퇴
    path('update/', views.update, name='update'),   # 업데이트
    path('profile/<username>/', views.profile, name='profile'), # 개인 프로필
    path('follow/<int:user_pk>/', views.follow, name='follow'), # 팔로잉
] 