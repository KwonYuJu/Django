from rest_framework import serializers
from .models import Article

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # 직렬화 하고자 하는 필드를 지정 -> json으로 직렬화
        fields = ('id', 'title', 'content',)

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # __all__ 모든 필드 직렬화
        fields = '__all__'