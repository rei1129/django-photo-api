from rest_framework import generics
# 汎用view
from rest_framework import viewsets

from rest_framework.permissions import AllowAny
# 現在はjson web tokenの認証が全てのviewで設定されているのでAllowAnyで上書きするとどのユーザーでもそのviewにアクセスすることができる

from . import serializers

from .models import Profile, Post, Comment

class CreateUserView(generics.CreateAPIView):
    # userを新規で作成するクラス
    serializer_class = serializers.UserSerializer #対象となるシリアライザーを指定

    permission_classes = (AllowAny,)
    # permission_classesをAllowAnyで上書きし、jwtの認証の例外としている

class ProfileViewSet(viewsets.ModelViewSet):
    # CRUD を全て使いたいのでModelViewSet
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)
    # self.request.userでログインしているユーザーのユーザー情報を取得することができる
    # それをuserProfileに格納し、新規でprofileを作る

class MyProfileListView(generics.ListAPIView):
    #　ログインしているユーザーの情報を返す
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)
        # ログインしているユーザーだけを返したいのでfilterを用いる

class PostViewSet(viewsets.ModelViewSet):
    # CRUD を全て使いたいのでModelViewSet
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    # CRUD を全て使いたいのでModelViewSet
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)