from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# model view setで作成したview
app_name = 'user'
router = DefaultRouter()
# model view setを敬称したviewのみrouter が記述できる
router.register('profile',views.ProfileViewSet)
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)


# 汎用viewで作成したviewはurlpatternで記述する

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('', include(router.urls))
]