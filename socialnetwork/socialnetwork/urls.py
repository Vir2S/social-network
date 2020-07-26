"""starnavi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.views import APIView
from rest_framework.authtoken.views import obtain_auth_token

from social.views import PostCreateView, PostListView, UserCreateView, PostLikeView, PostDislikeView, \
    AnalyticsView, ActivityUserView, login, IndexView

urlpatterns = [
    path('api/', APIView.as_view(), name='main_create'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('posts_list/', PostListView.as_view(), name='posts_list'),
    path('post/<int:post_pk>/<int:user_pk>/like/', PostLikeView.as_view(), name='post_like'),
    path('post/<int:post_pk>/<int:user_pk>/dislike/', PostDislikeView.as_view(), name='post_dislike'),
    path('post/analytics/?date_from=<date_from>&date_to=<date_to>/', AnalyticsView.as_view(), name='post_likes'),

    path('user_activity/<int:pk>', ActivityUserView.as_view(), name='user_activity'),

    path('create_user/', UserCreateView.as_view(), name='create_user'),
    path('login_user/', login, name='login'),

    # path('start_bot/', start_bot, name='startbot'),

    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
