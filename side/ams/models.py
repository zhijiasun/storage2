#coding:utf-8
from django.db import models

# Create your models here.


class AppComment(models.Model):
    app_version = models.CharField(u'app版本号',max_length=30)
    phone_info = models.CharField(u'手机信息',max_length=40)
    comment = models.TextField(u'意见')

    class Meta:
        verbose_name = u'意见反馈'
        verbose_name_plural = u'意见反馈'


class VersionManager(models.Model):
    version_id = models.AutoField(primary_key=True, auto_created=True)
    specified_app = models.IntegerField(u'针对',default=0,choices=((0,u'普通用户版本'),(1,u'工作人员版本')))
    version_code = models.CharField(u'版本号',max_length=30)
    version_name = models.CharField(u'版本名称',max_length=30)
    description = models.TextField(u'描述')
    download_url = models.FileField(upload_to='upload/',verbose_name="apk")

    class Meta:
        verbose_name = u'版本管理'
        verbose_name_plural = u'版本管理'
