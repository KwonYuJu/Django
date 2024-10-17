from rest_framework import serializers
from .models import Article, Comment

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # 직렬화 하고자 하는 필드를 지정 -> json으로 직렬화
        fields = ('id', 'title', 'content',)

class ArticleSerializer(serializers.ModelSerializer):
    # 게시글에 해당하는 댓글, 왜 ArticleSerializer 안에 중첩으로 있을까?
    # -> CommentDetailSerializer는 반드시 ArticleSerializer에서만 사용되기 때문이다
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)
    
    # 필드 2개 추가 : 읽기 전용 필드(read_only=True) 설정
    # 아래 3가지 조건 만족하면 읽기 전용 필드로
    # 1. 사용자로부터 입력 받지 않는다 -> 읽기 전용
    # 2. 유효성 검사 과정에서 제외됨
    # 3. 결과 데이터는 포함되어 클라이언트에 제공
    comment_set = CommentDetailSerializer(many=True, read_only=True)
    # comment_set : 역참조, count : 메서드
    comment_count = serializers.IntegerField(
        source = 'comment_set.sount', read_only=True
    )

    class Meta:
        model = Article
        # __all__ 모든 필드 직렬화
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # 댓글을 조회했을 때 게시글의 제목도 같이 나오게
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title',)
    # 댓글을 조회했을 때 같이 나오는 게시글의 제목은 읽기 전용
    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

