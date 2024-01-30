from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer
from .forms import CommentForm
from rest_framework.decorators import api_view
from rest_framework.throttling import UserRateThrottle


class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, pk=kwargs['pk'])
        comment_form = CommentForm()
        return render(request, self.template_name, {'post': post, 'comment_form': comment_form})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, pk=kwargs['pk'])
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
        return render(request, self.template_name, {'post': post, 'comment_form': comment_form})


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['POST'])
def add_comment(request, post_id):
    """
    Функция для добавления комментария к конкретному посту.
    """
    if request.method == 'POST':
        data = {'post': post_id, 'author': request.user.id, 'text': request.data.get('text')}
        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)