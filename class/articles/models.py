from django.db import models

# Create your models here.
class Article(models.Model):
  title = models.CharField(max_length=20)
  content = models.TextField()
  image = models.ImageField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

# ORM
# : python 코드를 SQL 쿼리로 변환해주는 도구

# 왜 ORM을 쓰냐?
# 우리가 사용하는 Django는 python, DB는 SQL

# QuerySet API 
# : 이 구문을 사용하면 데이터베이스에 접근하고 조작할 수 있다


# Create
'''
# 첫 번째 방법

article = Article()
article.title = ‘first’
article.content = ‘hello’
article.save()

Article.objects.all()

# 두 번째 방법

article = Article(title = ‘second’, content = ‘hello’)
article.save()

Ariticle.objects.all()

# 세 번째 방법

Article.objects.create(title = ‘third’, content = ‘byebye’)

Ariticle.objects.all()
'''
# 1번, 2번 <-> 3번 : save 호출을 따로 하는지 안하는지
# 3번 방법은 사용하지 않는게 좋다
# save() 호출 전에 미리 '데이터를 검증'하고 그 다음에 save 해야한다
# -> 검증단계 (유효성 검사.. 등)
# best는 1번 가장 안정적

# Read
'''
# 전체 데이터 조회
Aritcle.objects.all()


# 특정 조건 데이터 조회(filter)
Article.objects.filter(title = ‘first’)
Article.objects.filter(content__contains=’hel’)
Article.objects.filter(title__startswith=’f’)

# 단일 데이터 조회(get)
Article.objects.get(pk = 1)
Article.objects.get(content = ‘hello word’)

# 찾는 객체가 없으면 예외발생
# 찾는 객체가 두개 이상 있으면 예외 발생

# —> 고유성을 보장하는 조회
'''

# Update
'''
article = Article.objects.get(pk = 1)
article.title = ‘first1’
article.save()
'''

# delete
'''
article = Article.objects.get(pk = 1)
article.delete()
Article.objects.get(pk = 1)
# —> 예외 발생
'''

# 추가 QuerySet API 는 구글에 Django QuerySet API 검색 ---> 공식문서