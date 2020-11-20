from django.db import models
from django.contrib.auth.models import AbstractUser
from permission.models import Role
import uuid
# Create your models here.


class UserProfile(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name="手机号")
    department = models.CharField(max_length=512, verbose_name="部门")
    uid = models.CharField(default=uuid.uuid4, max_length=128, verbose_name="用户ID", unique=True)
    introduction = models.CharField(max_length=1024, verbose_name="简介", blank=True)
    role = models.ManyToManyField(to=Role, related_name="user_profile",
                                  blank=True, verbose_name="角色")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_profile"
        verbose_name_plural = verbose_name = "用户信息"

