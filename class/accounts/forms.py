# django auth form에서 유저생성 폼, 유저변경 폼
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# 직접 참조
# from .models import User

# 간접 참조
# get_user_model -> 커스텀 User모델을 자동으로 변환해주는 함수
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # model = User              # 직접 참조
        model = get_user_model()    # 간접 참조

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        # 회원 정보 변경할 필드를 설정
        fields = ('first_name', 'last_name', 'email',)