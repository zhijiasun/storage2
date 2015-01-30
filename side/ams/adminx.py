#coding:utf-8
from xadmin.sites import site
from ams.models import AppComment, VersionManager


class AppCommentAdmin(object):
    list_display = ('app_version','phone_info','comment')


class VersionManagerAdmin(object):
    list_display = ('version_code','version_name','description','download_url')
    list_filter = ('version_code','version_name','description')

site.register(AppComment, AppCommentAdmin)
site.register(VersionManager, VersionManagerAdmin)
