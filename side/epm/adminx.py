#coding:utf-8
from models import *
from xadmin.plugins.actions import BaseActionView
from import_export.admin import ImportExportModelAdmin
from plugin import *
from xadmin.sites import site
from xadmin import views
from xadmin.views import filter_hook
import xadmin
from xadmin.views import ListAdminView,ModelFormAdminView,CreateAdminView
from xadmin.layout import Fieldset, Field
from xadmin.views.base import CommAdminView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django import forms
from django.db import models
from django.forms import Textarea

# class JasonForm(forms.ModelForm):
#     class Meta:
#         model = Jason

# class TestAdmin(CommAdminView):
#     list_display = ('party_name','member_number','contact_info','attachment','pic','thumb')
#     list_filter = ('party_name','member_number','contact_info')

    # def save_models(self):
    #     print 'In Jason Admin'
    #     print self.request.FILES
    #     # f = self.request.FILES['attachment']
    #     # pa = default_storage.save('abc',ContentFile(f.read()))
    #     super(JasonAdmin,self).save_models()
    #     print 'ok'

# xadmin.site.register(Test,TestAdmin)


class MyAction(BaseActionView):
    action_name = "my_action"
    description = 'descripe the action'
    model_perm = 'change'

    def do_action(self,queryset):
        pass
class EnterpriseAdmin(object):
    list_display = ('enter_name','enter_address','enter_attribute',
            'industry_type','industry_nature','enter_scale','total_assets','related_party_status',
            'legal_person','legal_email','enter_email','legal_phone','fixed_phone')
    list_filter = ('enter_name','enter_address')
    resource_class = EnterpriseResource


class PartyAdmin(object):
    list_display = ('party_name','secretary_name','secretary_phone','member_number','responsible_name','related_enter','responsible_phone')
    list_filter = ('party_name','member_number')
    actions = [MyAction,]
    # reversion_enable = True


class MemberAdmin(object):

    list_display = ('member_name','member_gender','member_worktime','member_enter_name','member_party_name')
    list_filter = ('member_name','member_gender','member_worktime')
    # reversion_enable = True

class UserProfileAdmin(object):
    list_display = ('user','is_verified')


class WorkUserProfileAdmin(object):
    list_display = ('user','has_published')


class PioneerImageAdmin(object):
    model = PioneerImage
    extra = 1

class PioneerAdmin(object):
    list_display = ('title','date','author','content_thumb')
    list_filter = ('title','date','author','content')
    inlines = [PioneerImageAdmin]
    # reversion_enable = True
    exclude = ('int_date',)


# class LifeTipsImageAdmin(object):
#     model = LifeTipsImage
#     extra = 1


class LifeTipsAdmin(object):
    list_display = ('title','date','author','content')
    list_filter = ('title','date','author','content')
    # inlines = [LifeTipsImageAdmin]
    exclude = ('int_date',)
    # reversion_enable = True

    formfield_overrides = {models.TextField:{'widget':Textarea(attrs={'rows':4,'cols':40})},}


class PartyWorkImageAdmin(object):
    model = PartyWorkImage
    extra = 1


class PartyWorkAdmin(object):
    list_display = ('title','date','author','content')
    list_filter = ('title','date','author','content')
    inlines = [PartyWorkImageAdmin]
    exclude = ('int_date',)

    # reversion_enable = True


class NoticeImageAdmin(object):
    model = NoticeImage
    extra = 1


class NoticeAdmin(object):
    list_display = ('title','date','author','content')
    list_filter = ('title','date','author','content')
    inlines = [NoticeImageAdmin]
    exclude = ('int_date',)

    # reversion_enable = True


class SpiritImageAdmin(object):
    model = SpiritImage
    extra = 1


class SpiritAdmin(object):
    list_display = ('title','date','author','content')
    list_filter = ('title','date','author','content')
    inlines = [SpiritImageAdmin]
    exclude = ('int_date',)

    # reversion_enable = True


class PolicyImageAdmin(object):
    model = PolicyImage
    extra = 1


class PolicyAdmin(object):
    list_display = ('title','date','author','content')
    list_filter = ('title','date','author','content')
    inlines = [PolicyImageAdmin]
    exclude = ('int_date',)

    # reversion_enable = True
    
class BusinessProcessAdmin(object):
    list_display = ('title','date','author','content','process_type')
    list_filter = ('title','date','author','content','process_type')
    # reversion_enable = True


class QuestionAdmin(object):
    list_display = ('question_id','question_type_str','create_time','reply_time','question_author','question_content')
    list_filter = ('question_id', 'create_time','reply_time','question_author','question_content')
    exclude = ('reply_int','create_int')

    @filter_hook
    def get_model_form(self,**kwargs):
        if not self.user.has_perm('is_published'):
            self.readonly_fields = ('is_published',)

        form = super(QuestionAdmin,self).get_model_form(**kwargs)
        return form


class ListSetting(object):
    object_list_template = 'new.html'

class GolbeSetting(object):
    # globe_search_models = [Article, ]
    # menu_template = 'test.html'
    site_title = (u'崂企党建管理系统')
    site_footer = (u'www.centling.com')
    # globe_models_icon = {
    #     Article: 'file', Category: 'cloud'
    # }
xadmin.site.register(CommAdminView, GolbeSetting)
# xadmin.site.register(ListAdminView,ListSetting)

# class ArticleAdmin(object):
#     list_display = ('title', 'categories', 'date')
#     list_display_links = ('title',)

#     search_fields = ('title', 'content')
#     list_editable = ('date',)
#     list_filter = ('categories', 'date')

#     form_layout = (
#         Fieldset(u'基本信息',
#             'title', 'date'
#         ),
#         Fieldset(u'文章内容',
#             Field('content', template="xcms/content_field.html")
#         ),
#     )
#     style_fields = {'content': 'wysi_ck', 'categories':'m2m_tree'}

# class CategoryAdmin(object):
#     list_display = ('name', 'parent')
#     list_display_links = ('id', 'name',)

#     search_fields = ('name', )
#     list_editable = ('name', )
#     list_filter = ('parent', )

xadmin.site.register(enterprise,EnterpriseAdmin)
xadmin.site.register(party,PartyAdmin)
xadmin.site.register(member,MemberAdmin)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(WorkUserProfile,WorkUserProfileAdmin)
xadmin.site.register(Pioneer,PioneerAdmin)
xadmin.site.register(LifeTips,LifeTipsAdmin)
xadmin.site.register(PartyWork,PartyWorkAdmin)
xadmin.site.register(Notice,NoticeAdmin)
xadmin.site.register(Spirit,SpiritAdmin)
xadmin.site.register(Policy,PolicyAdmin)
xadmin.site.register(BusinessProcess,BusinessProcessAdmin)
xadmin.site.register(Question,QuestionAdmin)
site.register_plugin(MyPlugin,ListAdminView)
# site.register_plugin(ImportPlugin,ListAdminView)
# xadmin.site.register(Article, ArticleAdmin)
# xadmin.site.register(Category, CategoryAdmin)
