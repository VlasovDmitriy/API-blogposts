# blog/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import BlogPostListCreateView, BlogPostDetailView, CommentListCreateView, CommentDetailView, add_comment

urlpatterns = [
    path('posts/', BlogPostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:post_id>/comments/', add_comment, name='add-comment'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
