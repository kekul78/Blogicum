from django.urls import path

from pages import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutBlogicum.as_view(), name='about'),
    path('rules/', views.RulesBlogicum.as_view(), name='rules'),
]
