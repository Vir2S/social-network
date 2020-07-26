import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.authtoken.models import Token
from .serializers import PostSerializer, LikeSerializer, DislikeSerializer, UserSerializer, UserActivitySerializer
from .models import Post, Like, Dislike, SocialUser


class IndexView(TemplateView):
    template_name = 'index.html'
    permission_classes = [permissions.AllowAny]


class UserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = SocialUser.objects.all()
    serializer_class = UserSerializer

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class PostCreateView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class PostDislikeView(generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer


class AnalyticsView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        likes_analitic = Like.objects.filter(like_published__range=[kwargs['date_from'], kwargs['date_to']])

        if len(likes_analitic) > 0:
            mimetype = 'application/json'
            return HttpResponse(json.dumps({'likes by period': len(likes_analitic)}), mimetype)

        else:
            return self.list(request, *args, [{}])


class ActivityUserView(generics.RetrieveAPIView):
    queryset = SocialUser.objects.all()
    serializer_class = UserActivitySerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'Error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    user = SocialUser.objects.get(username=username, password=password)

    if request.user.is_authenticated:
        print('User is authenticated')

    else:
        print('User is not authenticated')

    if not user:
        return Response({'Error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
