from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
# Create your models here.

def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    # extには拡張子が格納されている
    # . で区切り、一番最後の配　例えば　test.aa.jpg の場合　.jpgを取得したいので-1 としている
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])
    # joinでavatorsというフォルダを作成し、その中に　userRei.jpg のような形で作成される

def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # オーバーライト
        if not email:
            raise ValueError('emailは必須です')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        # staff権限はAdmin Dashboardにログインするための権限
        user.is_superuser = True
        # staff権限に加え、DBの変更などの全ての権限
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    # デフォルトのものをEmail_verにオーバーライト
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    # アカウントの利用状況はtrue
    is_staff = models.BooleanField(default=False)
    # adminの権限はfalse
    objects = UserManager()
    # 上記のUserManagerのインスタンスを作成しobjectsに入れる

    USERNAME_FIELD = 'email'
    # defaultのusernameをオーバーライト

    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        # USER MODELとuserProfileを結びつけている
        on_delete=models.CASCADE
        # CASCADEは userが削除された時にProfileを紐付けで削除される
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    # Avatorの画像　画像を登録しなくても良いようにblankとnullをTrueにしている

    def __str__(self):
        return self.nickName

class Post(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)
    equipment = models.CharField(max_length=100, null=True)

    userPost = models.ForeignKey(
        # One to Manyを表現する時にはDjangoではForeignKeyと記述する
        settings.AUTH_USER_MODEL, related_name='userPost',
        # User Modelを紐付けしている
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked',blank=True)
    # User ModelとMany to Many

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        # UserModelとOne to Many
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # POSTとOne to Many

    def __str__(self):
        return self.text