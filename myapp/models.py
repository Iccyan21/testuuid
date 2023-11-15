from django.db import models
import uuid
from django.db.models import Q

class Account(models.Model):
    userid = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=True) 

    class Meta:
        unique_together = ['account', 'title']
        
    def get_queryset(self):
        # 公開されている投稿と、ログインユーザーの非公開の投稿のみ取得
        return Post.objects.filter(Q(is_public=True) | Q(author=self.request.user))
    
    