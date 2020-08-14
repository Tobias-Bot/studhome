from django.urls import path
from . import views
from . views import SearchProfilesList, PostsByInterestsListView, PostViewsUpdate, PostByMarksListView, addPostToBookMarksView, deletePostFromBookMarksView, unSubscribeUserView, SubscribeUserView, PopularPostListView, SubsPostsListView, BookMarksPostsListView, ImageDestroyView, PostUpdateView, SearchByTypePostList, PostDetailView, CommentUpdateView, SearchPostList, ImageCreateView, CommentDestroyView, PostCreateView, PostListView, PostDestroyView, CommentListView, UserPostsListView, CommentCreateView

urlpatterns = [
    path('post_create/<str:username>/', PostCreateView.as_view()),
    path('post_update/<str:id>/', PostUpdateView.as_view()),
    path('post_views_update/<int:post_id>/', PostViewsUpdate.as_view()),
    path('post/<int:post_id>/', PostDetailView.as_view()),
    path('post/all/', PostListView.as_view()),
    path('post/list/<str:username>/', UserPostsListView.as_view()),
    path('post_delete/<int:post_id>/<slug:username>/', PostDestroyView.as_view()),
    path('post/<int:pk>/image/', ImageCreateView.as_view()),
    path('post/image_delete/<int:id>/', ImageDestroyView.as_view()),
    path('post/<int:post_id>/comment/list/', CommentListView.as_view()),
    path('post/<int:pk>/comment/', CommentCreateView.as_view()),
    path('post/by_interests/<str:tags>/', PostsByInterestsListView.as_view()),
    path('post/<int:post_id>/comment/<int:com_id>/', CommentDestroyView.as_view()),
    path('comment_update/<int:id>/', CommentUpdateView.as_view()),
    path('search/', SearchPostList.as_view()),
    path('search_people/', SearchProfilesList.as_view()),
    path('post/type/', SearchByTypePostList.as_view()),
    path('post/marks/', PostByMarksListView.as_view()),
    path('post/bookmarks/', BookMarksPostsListView.as_view()),
    path('post/bookmarks_add/', addPostToBookMarksView.as_view()),
    path('post/bookmarks_delete/', deletePostFromBookMarksView.as_view()),
    path('post/mysubs/all/', SubsPostsListView.as_view()),
    path('post/popular/', PopularPostListView.as_view()),
    path('subscribe/', SubscribeUserView.as_view()),
    path('unsubscribe/', unSubscribeUserView.as_view()),
]