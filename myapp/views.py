from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PostListCreateView(APIView):
    
    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        # 公開されている投稿と、ログインユーザーの非公開の投稿のみ取得
        return Post.objects.filter(Q(is_public=True) | Q(account=user))

    def get(self, request):
        posts = self.get_queryset()
        serializer = PostSerializer(posts, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Account
from .serializers import AccountLoginSerializer

class AccountLoginView(APIView):

    def post(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        if serializer.is_valid():
            account = Account.objects.get(userid=serializer.validated_data['userid'])
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyView(APIView):
    
    def get_object(self, title):
        try:
            return Post.objects.get(title=title)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, title):
        post = self.get_object(title)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, title):
        post = self.get_object(title)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, title):
        post = self.get_object(title)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Post
from .serializers import PostSerializer

class UserPostsView(APIView):
    
    def get_queryset(self, userid, title=None):  # タイトルのクエリパラメータを引数として追加
        current_user_userid = self.request.user.username

        # 基本のクエリセット
        if current_user_userid == userid:
            queryset = Post.objects.filter(account__userid=userid)
        else:
            queryset = Post.objects.filter(account__userid=userid, is_public=True)
        
        # タイトルでのフィルタリング
        if title:
            queryset = queryset.filter(title__icontains=title)  # タイトルが部分一致するものをフィルタリング

        return queryset

    def get(self, request, userid):
        title = request.query_params.get('title')  # タイトルのクエリパラメータを取得
        posts = self.get_queryset(userid, title)   # get_querysetにtitleを渡します
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






class UserPostDetailView(APIView):

    def get(self, request, userid, title):
        # userid に基づく Account を取得
        account = get_object_or_404(Account, userid=userid)
        # 指定された title を持つ Post を取得
        post = get_object_or_404(Post, account=account, title=title)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserPostSearch(APIView):

    def get_queryset(self, userid, title=None):  # タイトルのクエリパラメータを引数として追加
        current_user_userid = self.request.user.username

        # 基本のクエリセット
        if current_user_userid == userid:
            queryset = Post.objects.filter(account__userid=userid)
        else:
            queryset = Post.objects.filter(account__userid=userid, is_public=True)
        
        # タイトルでのフィルタリング
        if title:
            queryset = queryset.filter(title__icontains=title)  # タイトルが部分一致するものをフィルタリング

        return queryset

    def get(self, request, userid):
        title = request.query_params.get('title')  # タイトルのクエリパラメータを取得
        posts = self.get_queryset(userid, title)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
