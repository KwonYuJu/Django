from django import forms
from .models import Article

# form 태그, django ModelForm의 차이?
# 사용자로부터 입력 받은 데이터를 DB에 저장하는지 안하는지?
# form 태그 사용해서도 DB 저장 가능, 단 수동으로 구현해야 함
# ModelForm을 왜 쓸까? -> 편하고 효율성이 좋음 + 유효성 검사에 용이

class ArticleForm(forms.ModelForm):
  # ModelForm의 설계 구조
  # class Meta : 폼의 기본 구조를 자동으로 생성 -> 세부 조정 가능(어떤 필드, 위젯)
  class Meta:
    model = Article
    # fields = ('title', 'content', 'created_at', 'updated_at', 'image',)
    fields = '__all__'

    