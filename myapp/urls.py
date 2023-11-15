from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView,UserPostsView,UserPostDetailView,AccountLoginView,UserPostSearch

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<str:title>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('posts/user/<str:userid>/', UserPostsView.as_view(), name='user-posts'),
    path('posts/<str:userid>/<str:title>/', UserPostDetailView.as_view(), name='user-post-detail'),
    path('account-login/', AccountLoginView.as_view(), name='account_login'),
    path('posts/search/<str:userid>/', UserPostSearch.as_view(), name='userpostsearch'),
]

