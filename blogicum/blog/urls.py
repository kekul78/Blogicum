from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [

    path('', views.IndexListView.as_view(), name='index'),
    path('posts/create/', views.PostCreateViews.as_view(), name='create_post'),
    path('category/<slug:slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'),
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/<int:post_id>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<post_id>/edit_comment/<comment_id>/',
         views.edit_comment,
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment,
         name='delete_comment'),
    path('profile/<slug:username>/',
         views.ProfileListView.as_view(),
         name='profile'),
    path('profile_edit/',
         views.ProfiletUpdateView.as_view(),
         name='edit_profile'),
]
