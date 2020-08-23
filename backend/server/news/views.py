from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.response import Response
from . serializers import SimpleCommentSerializer, ImageSerializer, PostListSerializer, UserSerializer, CommentSerializer, PostViewsSerializer
from userprofile.serializers import ProfileSerializer
from . permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.db.models import F
from django.db.models import Q

from . models import Post, Comment, Image
from userprofile.models import Profile

PostsPerPage = 10

class SearchPostList(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        tag = self.request.GET.get('q')
        a = int(self.request.GET.get("a"))
        b = int(self.request.GET.get("b"))

        title = tag[1:-1]
        queryset = Post.objects.filter(Q(tags__icontains=tag) | Q(title__icontains=title))[a:b]
        return queryset

class SearchProfilesList(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        name = self.request.GET.get('q')[1:-1]

        queryset = Profile.objects.filter(username__icontains=name)[:PostsPerPage]
        return queryset

class SearchByTypePostList(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        a = int(self.request.GET.get("a"))
        b = int(self.request.GET.get("b"))

        queryset = Post.objects.filter(type__icontains=query).order_by("-date")[a:b]
        return queryset

class SubscribeUserView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        username = self.request.GET.get('q')
        me = self.request.GET.get('me')
        profile = Profile.objects.get(username=me)
        profile.subs_profiles = profile.subs_profiles + username + "|"
        profile.save() 
        Profile.objects.filter(username=username).update(readers = F("readers") + 1)
        return Response(status=200)

class unSubscribeUserView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        username = self.request.GET.get('q')
        me = self.request.GET.get('me')
        profile = Profile.objects.get(username=me)
        profile.subs_profiles = profile.subs_profiles.replace("|" + username + "|", "|", 1)
        profile.save() 
        Profile.objects.filter(username=username).update(readers = F("readers") - 1)
        return Response(status=200)

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        username = self.kwargs['username']
        profile = Profile.objects.filter(username=username)
        serializer.save(user=self.request.user)
        profile.update(posts_count=Post.objects.filter(username=username).count())

class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    lookup_field = 'id'
    queryset = Post.objects.all()

class ImageCreateView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated, )

class ImageDestroyView(generics.DestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    def delete(self, request, id):
        img_id = self.kwargs['id']
        image = Image.objects.get(id=img_id)
        image.delete()
        return Response(status=204)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    # lookup_field = 'post_id'
    # queryset = Comment.objects.all()

    # def post(self, request, *args, **kwargs):
    #     post_id = self.kwargs['post_id']
    #     post = Post.objects.filter(id=post_id)
    #     comment = self.create(request, *args, **kwargs)
    #     post.update(comments_count=Comment.objects.filter(post=post_id).count())
    #     return Response(status=201)

class CommentDestroyView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated, )

    def delete(self, request, post_id, com_id):
        post_id = self.kwargs['post_id']
        com_id = self.kwargs['com_id']
        post = Post.objects.filter(id=post_id)
        comment = Comment.objects.get(id=com_id)
        comment.delete()
        post.update(comments_count=Comment.objects.filter(post=post_id).count())
        return Response(status=204)

class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        a = int(self.request.GET.get("a"))
        b = int(self.request.GET.get("b"))

        queryset = Post.objects.all().order_by('-date')[a:b]
        return queryset

class PostByMarksListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        query = self.request.GET.get('q')
        a = int(self.request.GET.get("a"))
        b = int(self.request.GET.get("b"))

        if (query):
            marks = query[1:-1].split("|")
            if (len(marks) == 1):
                queryset = Post.objects.filter(marks__icontains=marks[0]).order_by('-date')[a:b]
            if (len(marks) == 2):
                queryset = Post.objects.filter(Q(marks__icontains=marks[0]) | Q(marks__icontains=marks[1])).order_by('-date')[a:b]
            if (len(marks) == 3):
                queryset = Post.objects.filter(Q(marks__icontains=marks[0]) | Q(marks__icontains=marks[1]) | Q(marks__icontains=marks[2])).order_by('-date')[a:b]
        else:
            queryset = Post.objects.all().order_by('-date')[a:b]
            
        return queryset
    
class PopularPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        a = int(self.request.GET.get("a"))
        b = int(self.request.GET.get("b"))

        queryset = Post.objects.order_by('-views', '-comments_count')[a:b]
        return queryset

class UserPostsListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        username = self.kwargs['username']
        a = int(self.request.GET.get("a"))
        b = int(self.request.GET.get("b"))

        queryset = Post.objects.filter(username=username).order_by('-date')[a:b]
        return queryset

class BookMarksPostsListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    def get_queryset(self):
        username = self.request.GET.get("me")
        str = Profile.objects.get(username=username).bookmarks[1:-1]
        if (str):
            ids = str.split("|")
            queryset = Post.objects.filter(id__in=ids)[:PostsPerPage]
            return queryset

class PostsByInterestsListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    def get_queryset(self):
        str = self.kwargs['tags']
        if (str):
            tags = str[1:-1].split("|")
            print(tags)
            queryset = Post.objects.filter(tags__in=tags)[:PostsPerPage]
            return queryset

class addPostToBookMarksView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        index = self.request.GET.get('q')
        me = self.request.GET.get('me')
        profile = Profile.objects.get(username=me)
        profile.bookmarks = profile.bookmarks + index + "|"
        profile.save()
        return Response(status=201)

class deletePostFromBookMarksView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        index = self.request.GET.get('q')
        me = self.request.GET.get('me')
        profile = Profile.objects.get(username=me)
        profile.bookmarks = profile.bookmarks.replace("|" + index + "|", "|", 1)
        profile.save() 
        return Response(status=204)

class SubsPostsListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        username = self.request.GET.get("me")
        date = self.request.GET.get("d")
        a = int(self.request.GET.get("a"))
        b = int(self.request.GET.get("b"))

        str = Profile.objects.get(username=username).subs_profiles[1:-1]
        names = str.split("|")
        queryset = Post.objects.filter(username__in=names, date__gt=date).order_by("-date")[a:b]
        return queryset

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        #Post.objects.filter(id=post_id).update(views = F("views") + 1)
        queryset = Comment.objects.filter(post=post_id).order_by('-date', '-likes')
        return queryset

class PostDestroyView(generics.DestroyAPIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    def delete(self, request, post_id, username):
        post_id = self.kwargs['post_id']
        username = self.kwargs['username']
        post = Post.objects.get(id=post_id)
        post.delete()
        profile = Profile.objects.filter(username=username)
        profile.update(posts_count=Post.objects.filter(username=username).count())
        return Response(status=204)

class PostDetailView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        Post.objects.filter(id=post_id).update(views = F("views") + 1)
        queryset = Post.objects.filter(id=post_id)
        return queryset

class PostViewsUpdate(APIView):
    serializer_class = PostViewsSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, post_id):
        post_id = self.kwargs['post_id']
        Post.objects.filter(id=post_id).update(views = F("views") + 1)
        return Response(status=201)

class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = SimpleCommentSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'
    queryset = Comment.objects.all()