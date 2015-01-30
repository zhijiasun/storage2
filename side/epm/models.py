#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8") 
from django.db import models
from django.utils.dateformat import format
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.storage import default_storage
from epm.utils import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import os
from PIL import Image
from side.settings import MEDIA_ROOT
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.models import User
from adaptor.model import CsvDbModel,CsvModel
from adaptor.fields import *
import datetime
import time
from datetime import date
from django.db.models.signals import post_save, post_delete

telephone_validator = RegexValidator(regex = '^(1(([3-9][0-9])|(47)|[8][01236789]))\d{8}$'
        ,message = u'请输入正确的手机号'
        ,code = 'invalid_telephone')

img_size = [(266,300),(400,300),(800,300)]

def resize(img, box, fit, out):
    '''Downsample the image.
    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
    @param out: file-like-object - save the image into the output stream
    '''
    #preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0]/factor > 2*box[0] and img.size[1]*2/factor > 2*box[1]:
        factor *=2
    if factor > 1:
        img.thumbnail((img.size[0]/factor, img.size[1]/factor), Image.NEAREST)

    #calculate the cropping box and get the cropped part
    if fit:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2/box[0]
        hRatio = 1.0 * y2/box[1]
        if hRatio > wRatio:
            y1 = int(y2/2-box[1]*wRatio/2)
            y2 = int(y2/2+box[1]*wRatio/2)
        else:
            x1 = int(x2/2-box[0]*hRatio/2)
            x2 = int(x2/2+box[0]*hRatio/2)
        img = img.crop((x1,y1,x2,y2))

    #Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)

    #save it into a file-like object
    img.save(out, "JPEG", quality=75)
#resize

def make_thumb(path,size = (640,480)):
    pixbuf = Image.open(path)
    width, height = pixbuf.size

    if width > size:
        delta = width / size
        height = int(height / delta)
        pixbuf.thumbnail((size,height),Image.ANTIALIAS)
        return pixbuf

# Create your models here.

class party(models.Model):
    party_id = models.AutoField(primary_key=True,auto_created=True)
    party_name = models.CharField(u'党组织名称', max_length=100, unique=True)
    party_attribute = models.IntegerField(u'党组织属性',default=1,choices=PARTY_ATTRIBUTE)
    member_number = models.IntegerField(u'党员人数',blank=True)
    secretary_name = models.CharField(u'书记姓名',max_length = 50)
    secretary_phone = models.CharField(u'书记电话',max_length = 15)
    responsible_name = models.CharField(u'党务负责人姓名',max_length=50)
    responsible_phone = models.CharField(u'党务负责人电话',max_length=15)
    qq = models.CharField(u'QQ号',max_length=20,blank=True)
    weixin = models.CharField(u'微信号',max_length=20,blank=True)
    party_email = models.EmailField(u'党组织邮箱',blank=True)

    class Meta:
        verbose_name = u'党支部信息'
        verbose_name_plural = u'党支部信息'


    def __unicode__(self):
        return self.party_name

    def save(self,*args,**kwargs):
        self.member_number = len(self.membersAtParty.all())
        super(party,self).save(*args,**kwargs)

    def related_enter(self):
        # enters = enterprise.objects.filter(party_status=self)
        enters = self.enters.all() # use the realted_name in enterprise
        results = ''
        for enter in enters:
            print type(enter.enter_name)
            print enter.enter_name
            if results:
                results  = results + ';' + enter.enter_name
            else:
                results = results + enter.enter_name
        # enters = [ enter.enter_name for enter in enters ] # !! so strange, can't return chinese correctly

        return results

    related_enter.short_description = u'关联企业'

    def related_members(self):
        members = self.membersAtParty.all()
        return members

class PartyModel(CsvModel):

    def transform_party_attribute(value):
        for attribute in PARTY_ATTRIBUTE:
            if attribute[1] == value:
                return attribute[0]
        return 0

    party_name = CharField()
    party_attribute = IntegerField(prepare=transform_party_attribute)
    secretary_name = CharField()
    secretary_phone = CharField()
    responsible_name = CharField()
    responsible_phone = CharField()
    qq = CharField()
    weixin = CharField()
    party_email = CharField()

    class Meta:
        dbModel = party
        delimiter = ","
        has_header = True


class enterprise(models.Model):

    def validate_notnull(obj):
        if not obj:
            raise ValidationError('related party is NULL')

    enter_id = models.AutoField(primary_key=True,auto_created=True)
    enter_name = models.CharField(u'单位名称',max_length=50)
    enter_address = models.CharField(u'单位地址',max_length=300)
    enter_attribute = models.IntegerField(u'单位属性',default=1,choices=NATURE_CHOICES,blank=True)
    industry_type = models.IntegerField(u'行业类别',default=1,choices=INDUSTRY_TYPE)
    industry_nature = models.IntegerField(u'单位类型',default=1,choices=INDUSTRY_NATURE,blank=True)
    enter_scale = models.IntegerField(u'单位规模',default=1,choices=ENTER_SCALE,blank=True)
    total_assets = models.IntegerField(u'资产总额',default=1,choices=TOTAL_ASSETS,blank=True)
    legal_person = models.CharField(u'法人姓名',max_length=50)
    legal_email = models.EmailField(u'法人邮箱')
    enter_email = models.EmailField(u'单位邮箱', blank=True)
    legal_phone = models.CharField(u'负责人手机',max_length=50,validators=[telephone_validator,])
    fixed_phone = models.CharField(u'固定电话',max_length=50,blank=True)
    """
    blank=True, null=True can make ForeignKey is optional.
    1.
    we also can create an default party which means NULL and the id is 1 at DB, and do as follows:

    def get_default_party():
        return party.objects.get(id=1) 
    related_party = models.ForeignKey(party,verbose_name = u'党组织情况',default=get_default_party())

    2. chagne the behaviour when delete the ForeignKey:
       set the on_delete can change the behaviour
    """
    related_party = models.ForeignKey(party,verbose_name = u'党组织情况',blank=True,null=True,on_delete=models.SET_NULL,related_name='enters')

    class Meta:
        verbose_name = u'单位信息'
        verbose_name_plural = u'单位信息'


    def __unicode__(self):
        return self.enter_name

    def related_party_status(self):
        if self.related_party:
            return PARTY_ATTRIBUTE[self.related_party.party_attribute - 1][1]

    related_party_status.short_description = u'党组织属性'


# class EnterpriseModel(CsvDbModel):
#     class Meta:
#         dbModel = enterprise
#         delimiter = ","
#         exclude = ['enter_id',]
#         has_header = True


class EnterModel(CsvModel):

    def transform_enter_attribute(value):
        for attribute in NATURE_CHOICES:
            if attribute[1] == value:
                return attribute[0]
        return 0

    def transform_industry_type(value):
        for attribute in INDUSTRY_TYPE:
            if attribute[1] == value:
                return attribute[0]
        return 0

    def transform_industry_nature(value):
        for attribute in INDUSTRY_NATURE:
            if attribute[1] == value:
                return attribute[0]
        return 0

    def transform_enter_scale(value):
        for attribute in ENTER_SCALE:
            if attribute[1] == value:
                return attribute[0]
        return 0

    def transform_total_assets(value):
        for attribute in TOTAL_ASSETS:
            if attribute[1] == value:
                return attribute[0]
        return 0

    enter_name = CharField()
    enter_address = CharField()
    enter_attribute = IntegerField(prepare=transform_enter_attribute)
    industry_type = IntegerField(prepare=transform_industry_type)
    industry_nature = IntegerField(prepare=transform_industry_nature)
    enter_scale = IntegerField(prepare=transform_enter_scale)
    total_assets = IntegerField(prepare=transform_total_assets)
    legal_person = CharField()
    legal_email = CharField()
    enter_email = CharField()
    legal_phone = CharField()
    fixed_phone = CharField()
    related_party = DjangoModelField(party,pk='party_name')### here we can add default parameter


    class Meta:
        dbModel = enterprise
        delimiter = ","
        has_header = True


def validate_idcard(value):
    message = u'请输入正确长度的身份证号'
    message2 = u'身份证号内的出生年月不对'
    if len(value) != 18 and len(value) != 15:
        raise ValidationError(message)
    try:
        date(int(value[6:10]),int(value[10:12]),int(value[12:14]))
    except Exception, e:
        print str(e)
        raise ValidationError(message2)


class member(models.Model):
    member_name = models.CharField(verbose_name=u'党员姓名',max_length=80)
    member_gender = models.IntegerField(u'性别',default=0,choices=GENDER)
    member_nation = models.IntegerField(u'民族',default=1,choices=NATION)
    member_education = models.IntegerField(u'学历',default=0,choices=EDUCATION)
    member_birth = models.DateField(u'出生日期',blank=True,null=True)
    member_worktime = models.DateField(u'参加工作时间')
    join_party_time = models.DateField(u'入党时间')
    formal_member_time = models.DateField(u'转正时间',blank=True,null=True)
    now_party_time = models.DateField(u'转入现组织时间',blank=True,null=True)
    birth_address = models.CharField(u'出生地',max_length=100,blank=True,null=True)
    home_address = models.CharField(u'家庭住址',max_length=100,blank=True,null=True)
    living_address = models.CharField(u'现居住地址',max_length=100,blank=True,null=True)
    member_phone = models.CharField(u'手机号',max_length=11,validators=[telephone_validator,])
    member_email = models.EmailField(u'电子邮箱',max_length=50)
    qq = models.CharField(u'QQ号',max_length=15,blank=True,null=True)
    weixin = models.CharField(u'微信号',max_length=20,blank=True,null=True)
    school = models.CharField(u'毕业院校',max_length=80,blank=True,null=True)
    id_card = models.CharField(u'身份证号',unique=True, max_length=30, validators=[validate_idcard,])
    member_party = models.ForeignKey(party,verbose_name=u'隶属党组织',blank=True,null=True,on_delete=models.SET_NULL,related_name='membersAtParty')
    member_enter = models.ForeignKey(enterprise,verbose_name=u'隶属企业',blank=True,null=True,on_delete=models.SET_NULL,related_name='membersAtEnter')

    class Meta:
        verbose_name = u'党员信息'
        verbose_name_plural = u'党员信息'

    def __unicode__(self):
        return self.member_name

    def member_enter_name(self):
        return self.member_enter.enter_name

    member_enter_name.short_description = u'隶属企业'

    def member_party_name(self):
        return self.member_party.party_name
    member_party_name.short_description = u'隶属党组织'

    def save(self, *args, **kwargs):
        if self.id_card and not self.member_birth:
            self.member_birth = date(int(self.id_card[6:10]),int(self.id_card[10:12]),int(self.id_card[12:14]))
        super(member,self).save(*args, **kwargs)


def update_member_number(sender,**kwargs):
    obj = kwargs['instance']
    if obj and obj.member_party:
        obj.member_party.save()

post_save.connect(update_member_number, sender=member)


class MemberModel(CsvModel):
    def transform_member_gender(value):
        for attribute in GENDER:
            if attribute[1] == value:
                return attribute[0]
        return 0

    def transform_member_nation(value):
        for attribute in NATION:
            if attribute[1] == value:
                return attribute[0]
        return 0

    def transform_member_education(value):
        for attribute in EDUCATION:
            if attribute[1] == value:
                return attribute[0]
        return 0

    member_name = CharField()
    member_gender = IntegerField(prepare=transform_member_gender)
    member_nation = IntegerField(prepare=transform_member_nation)
    member_education = IntegerField(prepare=transform_member_education)
    member_birth = DateField(format="%Y/%m/%d")
    member_worktime = DateField(format="%Y/%m/%d")
    join_party_time = DateField(format="%Y/%m/%d")
    formal_member_time = DateField(format="%Y/%m/%d")
    now_party_time = DateField(format="%Y/%m/%d")
    birth_address = CharField(null=True,default='')
    home_address = CharField(null=True,default='')
    living_address = CharField(null=True,default='')
    member_phone = CharField(null=True,default='')
    member_email = CharField(null=True,default='')
    qq = CharField(null=True,default='')
    weixin = CharField(null=True,default='')
    school = CharField(null=True,default='')
    id_card = CharField(null=True,default='')
    member_party = DjangoModelField(party, pk='party_name')### here we can add default parameter
    member_enter = DjangoModelField(enterprise, pk='enter_name')### here we can add default parameter
    # member_party = models.ForeignKey(party,verbose_name=u'隶属党组织',blank=True,null=True,on_delete=models.SET_NULL,related_name='membersAtParty')
    # member_enter = models.ForeignKey(enterprise,verbose_name=u'隶属企业',blank=True,null=True,on_delete=models.SET_NULL,related_name='membersAtEnter')
    class Meta:
        dbModel = member
        delimiter = ","
        # exclude = 'party_id','member_number'
        has_header = True
        update = {'keys':["id_card"]}


def delete_user(sender,**kwargs):
    obj = kwargs['instance']
    if obj and obj.user:
        obj.user.delete()


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='app_user', verbose_name=u'用户名')
    # member_info = models.OneToOneField(member,blank=True,null=True)
    # need to consider what is content of the table ?
    # real_name and real_idcard is the field that user should commit
    # and through member_info to find the registerd info to verify
    real_name = models.CharField(u'认证姓名', max_length=40, blank=True, null=True)
    real_idcard = models.CharField(u'认证身份证号', max_length=20, blank=True, null=True)
    real_organization = models.CharField(u'认证党组织',max_length=120,blank=True, null=True)
    is_verified = models.BooleanField(u'是否已认证', default=False)
    is_manager = models.IntegerField(u'是否是党组织管理员', default=0,choices=VERIFY_PROCESS)

    class Meta:
        verbose_name = u'终端用户认证'
        verbose_name_plural = u'终端用户认证'


post_delete.connect(delete_user, sender=UserProfile)


class WorkUserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='worker', verbose_name = u'用户名')
    has_published = models.IntegerField(u'是否具有发布权限', default=0, choices=((0,u'不具有'),(1,u'具有')))

    class Meta:
        verbose_name = u'工作人员用户'
        verbose_name_plural = u'工作人员用户'


post_delete.connect(delete_user, sender=WorkUserProfile)


class Pioneer(models.Model):
    pioneer_id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(u'标题',max_length=30)
    date = models.DateTimeField(u'创建日期',auto_now_add=True)
    author = models.CharField(u'作者',max_length=30)
    content = models.TextField(u'内容')
    int_date = models.IntegerField(blank=True, null=True)
    # pioneer_pic = models.ImageField(upload_to='upload/',blank=True,verbose_name=u"图片")

    class Meta:
        verbose_name = u'党务先锋'
        verbose_name_plural = u'党务先锋'

    def __unicode__(self):
        return self.title

    def content_thumb(self):
        if self.content:
            return self.content[0:20]
    content_thumb.short_description = u'内容缩略'

    def save(self,*args,**kwargs):
        self.int_date = int(time.time())
        super(Pioneer,self).save(*args,**kwargs)


class PioneerImage(models.Model):
    content = models.ForeignKey(Pioneer,related_name='img_list', verbose_name=u"附图")
    pic = models.ImageField(upload_to='upload/%Y_%m_%d/',blank=True,verbose_name=u"图片")

    class Meta:
        verbose_name = u'党务先锋附图'
        verbose_name_plural = u'党务先锋附图'

    def __unicode__(self):
        base, ext = os.path.splitext(os.path.basename(self.pic.url))
        base_url = os.path.dirname(self.pic.url)
        # return os.path.join(base_url + '/' + base + '_thumb' + ext)
        return self.pic.url

    def save(self):
        super(PioneerImage, self).save()
        base, ext = os.path.splitext(os.path.basename(self.pic.path))
        directory = os.path.dirname(self.pic.path)
        picture = Image.open(self.pic.path)
        actual_size = picture.size
        for size in img_size:
            if size < actual_size:
                # thumb = picture.thumbnail(size,Image.ANTIALIAS)
                thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                resize(picture,size,True,thumb_path)
                # thumb.save(thumb_path)
        super(PioneerImage, self).save()

class LifeTips(models.Model):
    lifetips_id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(u'标题',max_length=30)
    date = models.DateTimeField(u'创建日期',auto_now_add=True)
    author = models.CharField(u'作者',max_length=30)
    content = models.TextField(u'内容')
    int_date = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = u'生活小贴士'
        verbose_name_plural = u'生活小贴士'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.int_date = int(time.time())
        super(LifeTips,self).save(*args,**kwargs)


class LifeTipsImage(models.Model):
    content = models.ForeignKey(LifeTips,related_name='img_list', verbose_name=u"附图")
    pic = models.ImageField(upload_to='upload/%Y_%m_%d/',blank=True,verbose_name=u"图片")

    class Meta:
        verbose_name = u'生活小贴士附图'
        verbose_name_plural = u'生活小贴士附图'

    def __unicode__(self):
        base, ext = os.path.splitext(os.path.basename(self.pic.url))
        base_url = os.path.dirname(self.pic.url)
        # return os.path.join(base_url + '/' + base + '_thumb' + ext)
        return self.pic.url

    def save(self):
        super(LifeTipsImage, self).save()
        base, ext = os.path.splitext(os.path.basename(self.pic.path))
        directory = os.path.dirname(self.pic.path)
        picture = Image.open(self.pic.path)
        actual_size = picture.size
        for size in img_size:
            if size < actual_size:
                thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                resize(picture,size,True,thumb_path)
                # thumb = picture.resize(size,Image.ANTIALIAS)
                # thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                # thumb.save(thumb_path)
        super(LifeTipsImage, self).save()


class PartyWork(models.Model):
    partywork_id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(u'标题',max_length=30)
    specified = models.IntegerField(u'针对',default=0,choices=((0,u'请选择'),(1,u'所有党员'),(2,u'所有党组织管理员')))
    specified_person = models.ManyToManyField(member,verbose_name=u'针对特定党员', blank=True,null=True)
    # specified_party = models.BooleanField(verbose_name=u'针对所有党组织管理员', default=False)
    # is_all = models.BooleanField(verbose_name=u'针对所有人',blank=True,default=False)
    date = models.DateTimeField(u'创建日期',auto_now_add=True)
    author = models.CharField(u'作者',max_length=30)
    content = models.TextField(u'内容',)
    int_date = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = u'党务提醒信息'
        verbose_name_plural = u'党务提醒信息'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.int_date = int(time.time())
        super(PartyWork,self).save(*args,**kwargs)


class PartyWorkImage(models.Model):
    content = models.ForeignKey(PartyWork,related_name='img_list', verbose_name=u"附图")
    pic = models.ImageField(upload_to='upload/%Y_%m_%d/',blank=True,verbose_name=u"图片")

    class Meta:
        verbose_name = u'党务提醒附图'
        verbose_name_plural = u'党务提醒附图'

    def __unicode__(self):
        base, ext = os.path.splitext(os.path.basename(self.pic.url))
        base_url = os.path.dirname(self.pic.url)
        # return os.path.join(base_url + '/' + base + '_thumb' + ext)
        return self.pic.url

    def save(self):
        super(PartyWorkImage, self).save()
        base, ext = os.path.splitext(os.path.basename(self.pic.path))
        directory = os.path.dirname(self.pic.path)
        picture = Image.open(self.pic.path)
        actual_size = picture.size
        for size in img_size:
            if size < actual_size:
                thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                resize(picture,size,True,thumb_path)
                # thumb = picture.resize(size,Image.ANTIALIAS)
                # thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                # thumb.save(thumb_path)
        super(PartyWorkImage, self).save()


class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(u'标题',max_length=30)
    date = models.DateTimeField(u'创建日期',auto_now_add=True)
    author = models.CharField(u'作者',max_length=30)
    content = models.TextField(u'内容')
    int_date = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = u'公告活动信息'
        verbose_name_plural = u'公告活动信息'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.int_date = int(time.time())
        super(Notice,self).save(*args,**kwargs)


class NoticeImage(models.Model):
    content = models.ForeignKey(Notice,related_name='img_list', verbose_name=u"附图")
    pic = models.ImageField(upload_to='upload/%Y_%m_%d/',blank=True,verbose_name=u"图片")

    class Meta:
        verbose_name = u'公告活动附图'
        verbose_name_plural = u'公告活动附图'

    def __unicode__(self):
        base, ext = os.path.splitext(os.path.basename(self.pic.url))
        base_url = os.path.dirname(self.pic.url)
        # return os.path.join(base_url + '/' + base + '_thumb' + ext)
        return self.pic.url

    def save(self):
        super(NoticeImage, self).save()
        base, ext = os.path.splitext(os.path.basename(self.pic.path))
        directory = os.path.dirname(self.pic.path)
        picture = Image.open(self.pic.path)
        actual_size = picture.size
        for size in img_size:
            if size < actual_size:
                thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                resize(picture,size,True,thumb_path)
                # thumb = picture.resize(size,Image.ANTIALIAS)
                # thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                # thumb.save(thumb_path)
        super(NoticeImage, self).save()


class Spirit(models.Model):
    spirit_id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(u'标题',max_length=30)
    date = models.DateTimeField(u'创建日期',auto_now_add=True)
    author = models.CharField(u'作者',max_length=30)
    content = models.TextField(u'内容')
    int_date = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = u'上级精神'
        verbose_name_plural = u'上级精神'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.int_date = int(time.time())
        super(Spirit,self).save(*args,**kwargs)


class SpiritImage(models.Model):
    content = models.ForeignKey(Spirit,related_name='img_list', verbose_name=u"附图")
    pic = models.ImageField(upload_to='upload/%Y_%m_%d/',blank=True,verbose_name=u"图片")

    class Meta:
        verbose_name = u'上级精神附图'
        verbose_name_plural = u'上级精神附图'

    def __unicode__(self):
        base, ext = os.path.splitext(os.path.basename(self.pic.url))
        base_url = os.path.dirname(self.pic.url)
        # return os.path.join(base_url + '/' + base + '_thumb' + ext)
        return self.pic.url

    def save(self):
        super(SpiritImage, self).save()
        base, ext = os.path.splitext(os.path.basename(self.pic.path))
        directory = os.path.dirname(self.pic.path)
        picture = Image.open(self.pic.path)
        actual_size = picture.size
        for size in img_size:
            if size < actual_size:
                thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                resize(picture,size,True,thumb_path)
                # thumb = picture.resize(size,Image.ANTIALIAS)
                # thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                # thumb.save(thumb_path)
        super(SpiritImage, self).save()


class Policy(models.Model):
    policy_id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(u'标题',max_length=30)
    date = models.DateTimeField(u'创建日期',auto_now_add=True)
    author = models.CharField(u'作者',max_length=30)
    content = models.TextField(u'内容')
    int_date = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = u'惠企政策'
        verbose_name_plural = u'惠企政策'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.int_date = int(time.time())
        super(Policy,self).save(*args,**kwargs)


class PolicyImage(models.Model):
    content = models.ForeignKey(Policy,related_name='img_list', verbose_name=u"附图")
    pic = models.ImageField(upload_to='upload/%Y_%m_%d/',blank=True,verbose_name=u"图片")

    class Meta:
        verbose_name = u'惠企政策附图'
        verbose_name_plural = u'惠企政策附图'

    def __unicode__(self):
        base, ext = os.path.splitext(os.path.basename(self.pic.url))
        base_url = os.path.dirname(self.pic.url)
        # return os.path.join(base_url + '/' + base + '_thumb' + ext)
        return self.pic.url

    def save(self):
        super(PolicyImage, self).save()
        base, ext = os.path.splitext(os.path.basename(self.pic.path))
        directory = os.path.dirname(self.pic.path)
        picture = Image.open(self.pic.path)
        actual_size = picture.size
        for size in img_size:
            if size < actual_size:
                thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                resize(picture,size,True,thumb_path)
                # thumb = picture.resize(size,Image.ANTIALIAS)
                # thumb_path = os.path.join(directory + '/' + base + '_thumb_' +str(size[0])+'_'+str(size[1])+ ext)
                # thumb.save(thumb_path)
        super(PolicyImage, self).save()


class BusinessProcess(models.Model):
    process_id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(u'标题',max_length=30)
    date = models.DateTimeField(u'创建日期',auto_now_add=True)
    process_type = models.CharField(u'流程类型',max_length=10,default='join',choices =PROCESS_TYPE)
    author = models.CharField(u'作者',max_length=30)
    content = models.TextField(u'内容')
    # process_file = models.FileField(upload_to='upload/',blank=True,null=True,verbose_name=u'附件')

    class Meta:
        verbose_name = u'业务办理流程'
        verbose_name_plural = u'业务办理流程'

    def __unicode__(self):
        return self.title


class Question(models.Model):

    def create_int_default():
        return int(time.time())

    question_id = models.AutoField(primary_key=True,auto_created=True, verbose_name=u'问题ID')
    question_title = models.CharField(u'标题',max_length=30,default=u'问题咨询')
    create_time = models.DateTimeField(u'创建日期',auto_now_add=True)
    reply_time = models.DateTimeField(u'回复时间', auto_now_add=True)
    create_int = models.IntegerField(blank=True, null=True, default=create_int_default)
    reply_int = models.IntegerField(blank=True, null=True, default=create_int_default)
    # question_author = models.ManyToManyField(User, verbose_name=u'提问者',related_name='user_questions')
    question_author = models.CharField(verbose_name=u'提问者', max_length='40')
    question_type = models.IntegerField(u'问题类型',default=0, choices=QUESTION_TYPE)
    question_content = models.TextField(u'咨询内容')
    question_answer = models.TextField(u'咨询回复',blank=True,null=True)
    is_published = models.BooleanField(u'发布',default=False)
    class Meta:
        verbose_name = u'咨询服务'
        verbose_name_plural = u'咨询服务'
        permissions = (('is_published',u'可发布咨询回复'),)

    def __unicode__(self):
        return self.question_title

    def question_type_str(self):
        return QUESTION_TYPE[self.question_type][1]
    question_type_str.short_description=u'问题类型'

    def save(self,*args,**kwargs):
        """
        reply_time equals to the time that when the is_published set to true.
        Otherwise reply_time equals to create_time
        """
        if self.is_published:
            self.reply_time = datetime.datetime.now()
            self.reply_int = int(format(self.reply_time, u'U'))
        super(Question,self).save(*args,**kwargs)



# class Test(models.Model):
#     party_id = models.AutoField(primary_key=True,auto_created=True)
#     party_name = models.CharField(u'党支部名称',max_length=100)
#     member_number = models.IntegerField(u'党员人数')
#     contact_info = models.CharField(u'联系方式',max_length=300)
#     attachment = models.FileField(upload_to='upload/',blank=True)
#     pic = models.ImageField(upload_to='upload/',blank=True)
#     thumb = models.ImageField(upload_to='thumb/',blank=True)

#     class Meta:
#         verbose_name = u'测试'
#         verbose_name_plural = u'测试'


#     def __unicode__(self):
#         return self.party_name

#     def save(self):
#         super(Test,self).save()
#         base, ext = os.path.splitext(os.path.basename(self.pic.path))
#         thumb_path = os.path.join(MEDIA_ROOT, base + '_thumb' + ext)
#         thumb_path1 = os.path.join(base + '_thumb' + ext)
#         thumb_pixbuf = make_thumb(self.pic.path)
#         thumb_pixbuf.save(thumb_path)
#         self.thumb = ImageFieldFile(self,self.thumb,thumb_path1)
#         super(Test,self).save()


# class Category(models.Model):
#     name = models.CharField(u"名称", max_length=64)
#     parent = models.ForeignKey('self', verbose_name=u'父类别', related_name='children', null=True, blank=True)

#     class Meta:
#         verbose_name=u'类别'
#         verbose_name_plural = verbose_name

#     def __unicode__(self):
#         return self.name

# class Article(models.Model):
#     title = models.CharField(u"标题", max_length=200)
#     date = models.DateField(u"发布时间")
#     content = models.TextField(u"内容", null=True, blank=True)
#     attachment = models.FileField(u'附件',upload_to='/home/jasonsun/svn_repo/',blank=True)
#     categories = models.ManyToManyField('Category', null=True, blank=True)

#     class Meta:
#         verbose_name=u'文章'
#         verbose_name_plural = verbose_name

#     def __unicode__(self):
#         return self.title
