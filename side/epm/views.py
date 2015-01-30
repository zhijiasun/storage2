#coding:utf-8
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view,link,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from epm.serializers import *
from models import *
from django.views.decorators.csrf import csrf_exempt
from xadmin.views.edit import ModelFormAdminView,CreateAdminView
from django import forms
from django.utils.encoding import force_unicode
from import_export.admin import ImportMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import time,datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from registration.views import RegistrationView as BaseRegistrationView
from registration import signals
from rest_framework.serializers import _resolve_model
from django.contrib.auth import authenticate,login
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from epm.tools import *
from epm.error import errMsg
import csv
import time
import logging
import os,random,base64
logger = logging.getLogger(__name__)

# Create your views here.


class RegistrationView(BaseRegistrationView):
    def register(self,request,**cleaned_data):
        username,email,password = cleaned_data['username'],cleaned_data['email'],cleaned_data['password1']
        u = User.objects.create_user(username, email, password)
        # u.is_staff = True
        # u.save()
        # new_user = authenticate(username=username, password=password)
        # login(request, new_user)

        signals.user_registered.send(sender=self.__class__, user=u, request=request)
        
        # user_profile_model = _resolve_model
        # new_user.is_staff=True
        UserProfile.objects.create(user=u)
        return u


class IsVerified(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print 'obj is:',type(obj)
        print obj.app_user
        print request.user

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = member.objects.all()
    serializer_class = MemberSerializer


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = enterprise.objects.all()
    serializer_class = EnterpriseSerializer


class PartyViewSet(viewsets.ModelViewSet):
    queryset = party.objects.all()
    serializer_class = PartySerializer


# class TestViewSet(viewsets.ModelViewSet):
#     queryset = Test.objects.all()
#     serializer_class = TestSerializer

#     @link()
#     def get_bynumber(self,request,pk=None):
#         print pk
#         tests = Test.objects.filter(member_number=pk)
#         tserializer = TestSerializer(tests,many=True)
#         return Response(tserializer.data)


@api_view(['POST'])
def email_change(request, username):
    if request.method == 'POST':
        result = {'errCode':10000,'errDesc':errMsg[10000]}
        old_email = request.DATA.get('old_email','')
        new_email = request.DATA.get('new_email','')
        users = User.objects.filter(username=username,email=old_email)
        if users:
            logger.debug('input new email is:%s',new_email)
            users[0].email=new_email
            users[0].save()
            return Response(result,status = status.HTTP_200_OK)
        else:
            result['errCode']=10008
            result['errDesc']=errMsg[10008]
            logger.debug('input invalid username or email:%s,%s',username,old_email)
            return Response(result,status = status.HTTP_200_OK)


@api_view(['POST'])
def party_verify(request, username):
    if request.method == 'POST':
        result = {}
        result['errCode']=10006
        result['errDesc']=errMsg[10006]
        users = User.objects.filter(username=username)
        if users:
            name = request.DATA.get('real_name','')
            idcard = request.DATA.get('real_idcard','')
            organization = request.DATA.get('party_name','')
            logger.debug('name:%s,idcard:%d,organization:%s', name, idcard, organization)

            if name and idcard and organization:
                u = UserProfile.objects.get(user=users[0])
                u.real_name = name
                u.real_idcard = idcard
                u.real_organization = organization
                u.is_manager = 1#always set the value to 1 when receive the post request
                u.save()
                result['errCode']=10000
                result['errDesc']=errMsg[10000]
                return Response(result,status = status.HTTP_200_OK)
        else:
            logger.debug('user is not exist,username is: %s', username)

        return Response(result, status = status.HTTP_200_OK)

@api_view(['POST'])
def member_verify(request, username):
    if request.method == 'POST':
        result = {}
        users = User.objects.filter(username=username)
        if users:
            name = request.DATA.get('real_name','')
            idcard = request.DATA.get('real_idcard','')
            if name and idcard:
                m = member.objects.filter(id_card=idcard,member_name=name)
                if len(m) is 1:
                    u = UserProfile.objects.filter(user=users[0])
                    if u:
                        u[0].is_verified = True
                        u[0].real_name = name
                        u[0].real_idcard = idcard
                        u[0].save()
                        result['errCode']=10000
                        result['errDesc'] = errMsg[10000]
                        return Response(result,status = status.HTTP_200_OK)

            logger.debug('name and idcard is:%s,%s', name, idcard)
            result['errCode'] = 10005
            result['errDesc'] = errMsg[10005]

        else:
            logger.debug('user is not exist,username is: %s', username)
            result['errCode']=10006
            result['errDesc']=errMsg[10006]
        return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
def user_info(request, username):
    if request.method == 'GET':
        result = {}
        result['errCode'] = 10006
        result['errDesc'] = errMsg[10006]
        users = User.objects.filter(username=username)
        if users:
            ups = users[0].app_user.all()
            if len(ups) is 1:
                result['errCode'] = 10000
                result['errDesc'] = errMsg[10000]
                result['data'] = {'is_verified':ups[0].is_verified, 'is_manager': ups[0].is_manager,'real_name':ups[0].real_name,
                        'real_idcard':ups[0].real_idcard,'real_organization':ups[0].real_organization}
                return Response(result,status = status.HTTP_200_OK)
        return Response(result,status=status.HTTP_200_OK)



def party_list(request):
    pass


def enter_list(request):
    pass


@api_view(['POST'])
def submit_question(request,username):
    if request.method == 'POST':
        users = User.objects.filter(username=username)
        result = {'errCode':10004,'errDesc':errMsg[10004]}
        if users:
            question_type = request.DATA.get('question_type',0)
            question_content = request.DATA.get('question_content','')
            if question_content:
                q = Question.objects.create(question_type=question_type,question_content=question_content,question_author=username)
                q.save()
                result['errCode']=10000
                result['errDesc']=errMsg[10000]
                return Response(result,status = status.HTTP_200_OK)
            else:
                result['errCode']=10007
                result['errDesc']=errMsg[10007]

        else:
            result['errCode']=10006
            result['errDesc']=errMsg[10006]
        return Response(result,status = status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def member_info(request, username):
    if request.method == 'GET':
        users = User.objects.filter(username=username)
        if users:
            appuser = users[0].app_user.all()
            if appuser[0].is_verified:
                m = member.objects.filter(id_card = appuser[0].real_idcard, member_name = appuser[0].real_name)
                if m:
                    ms = MemberSerializer(m[0])
                    result = {"errCode":10000, "errDesc":errMsg[10000],"data":ms.data}
                    return Response(result,status = status.HTTP_200_OK)
                else:
                    result = {"errCode":10012, "errDesc":errMsg[10012]}
        else:
            result = {"errCode":10006, "errDesc":errMsg[10006]}
        return Response(result,status = status.HTTP_200_OK)

@api_view(['GET','POST'])
def party_info(request,username):
    if request.method == 'GET':
        users = User.objects.filter(username=username)
        result = {}
        if users:
            up = users[0].app_user.all()
            if up:
                party_name = up[0].real_organization
                parties = party.objects.filter(party_name=party_name)
                if parties:
                    m = parties[0].membersAtParty.all()
                    ms = MemberSerializer(m,many=True)
                    result = {"errCode":10000, "errDesc":errMsg[10000],"data":ms.data}
                    return Response(result,status = status.HTTP_200_OK)
                else:
                    result['errCode']=10013
                    result['errDesc']=errMsg[10013]

            else:
                result['errCode']=10006
                result['errDesc']=errMsg[10006]
        else:
            result['errCode']=10006
            result['errDesc']=errMsg[10006]

        return Response(result,status = status.HTTP_200_OK)


def get_upload():
    return 'upload/'+time.strftime("%Y_%m_%d")+"/"


def get_image_name():
    p = os.path.join(settings.MEDIA_ROOT,get_upload())
    if not os.path.isdir(p):
        os.makedirs(p)
    return time.strftime("%Y%m%d%H%M%S")+'_'+str(random.randint(0,10000))+".jpg"

def post_result(model, modelImage, request):
    title = request.DATA.get('title', '')
    author = request.DATA.get('author', '')
    content = request.DATA.get('content', '')
    imgfile = request.DATA.get('imgfile', '')
    result = {'errCode':10000, 'errDesc':errMsg[10000]}

    if not title or not author:
        result['errCode']=10007
        result['errDesc']=errMsg[10007]
        return result

    if imgfile and model is LifeTips:
        logger.debug('can not post image to lifetips from app')
        result['errCode']=10019
        result['errDesc']=errMsg[10019]
        return result

    if imgfile and content and model is not LifeTips:
        try:
            url = get_upload() + get_image_name()
            tmp_file = settings.MEDIA_ROOT + url
            writefile = open(tmp_file,"w")
            writefile.write(base64.decodestring(imgfile))
            writefile.close()
            obj = model(title=title, author=author, content=content)
            obj.save()
            if model is PartyWork:
                specific_person = request.DATA.get('specific_person',[])
                all = request.DATA.get('all',False)
                all_manager = request.DATA.get('all_manager',False)
                print specific_person,all,all_manager
                if all: 
                    obj.specified = 1
                elif all_manager: 
                    obj.specified = 2
                elif specific_person:
                    for p in specific_person:
                        m = member.objects.filter(member_name=p)
                        if m:
                            obj.specified_person.add(m[0])
                obj.save()
            objpic = modelImage(content=obj)
            objpic.pic = url
            objpic.save()
        except Exception,e:
            print str(e)
            result['errCode']=10020
            result['errDesc']=errMsg[10020]
            return result
    if content and not imgfile:
        try:
            obj = model(title=title, author=author, content=content)
            obj.save()
            if model is PartyWork:
                specific_person = request.DATA.get('specific_person',[])
                if type(specific_person) is unicode:
                    specific_person = specific_person.split(',')
                all_person = request.DATA.get('all',False)
                all_manager = request.DATA.get('all_manager',False)
                if type(all_person) is unicode:
                    if str(all_person) is '1':
                        all_person = True
                    elif str(all_person) is '0':
                        all_person = False

                if type(all_manager) is unicode:
                    if str(all_manager) is '1':
                        all_manager = True
                    elif str(all_manager) is '0':
                        all_manager = False

                if all_person: 
                    obj.specified = 1
                elif all_manager: 
                    obj.specified = 2
                elif specific_person:
                    for p in specific_person:
                        m = member.objects.filter(member_name=p)
                        if m:
                            obj.specified_person.add(m[0])
                obj.save()

        except Exception,e:
            print str(e)
            result = {'errCode':10004, 'errDesc':errMsg[10004]}

    return result


def get_result(model, modelSerializer,kwargs):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    # startTime = time.localtime(float(kwargs.get('startTime',0)))
    # startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))

    # if 'endTime' in kwargs.keys():
    #     endTime = time.localtime(float(kwargs.get('endTime')))
    #     endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
    # else:
    #     endTime = datetime.datetime.now()

    startTime = kwargs.get('startTime', 0)

    if 'endTime' in kwargs.keys():
        endTime = kwargs.get('endTime')
    else:
        endTime = int(time.time())


    obj = model.objects.filter(int_date__gt=startTime).filter(int_date__lt=endTime).order_by('-int_date')
    maxCount = int(kwargs.get('maxCount',0))
    offset = int(kwargs.get('offset',0))

    if maxCount:
        obj = obj[offset:offset+maxCount]
    else:
        obj = obj[offset:]
    objs = modelSerializer(obj,many=True)
    result = {"errCode":10000,"errDesc":errMsg[10000],"data":objs.data}
    # if objs.is_valid():
    #     result = {"result":"0000","message":"Successfully get content","data":objs.data}
    #     print result
    # else:
    #     result = {"result":"0001","message":"Get content error!","data":objs.errors}
    #     print result
    return result




@api_view(['GET','POST'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def pioneer_list(request):
    if request.method == 'GET':
        result = get_result(Pioneer, PioneerSerializer,request.GET)
        return Response(result, status = status.HTTP_200_OK)


@api_view(['GET','POST'])
def lifetips_list(request):
    if request.method == 'GET':
        result = get_result(LifeTips,LifeTipsSerializer,request.GET)
        return Response(result,status = status.HTTP_200_OK)
    elif request.method == 'POST':
        result = post_result(LifeTips, LifeTipsImage, request)
        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def notice_list(request):
    if request.method == 'GET':
        result = get_result(Notice, NoticeSerializer,request.GET)
        return Response(result,status = status.HTTP_200_OK)
    elif request.method == 'POST':
        result = post_result(Notice, NoticeImage, request)
        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def spirit_list(request):
    if request.method == 'GET':
        result = get_result(Spirit, SpiritSerializer, request.GET)
        return Response(result, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        result = post_result(Spirit, SpiritImage, request)
        return Response(result, status=status.HTTP_200_OK)



@api_view(['GET','POST'])
def policy_list(request):
    if request.method == 'GET':
        result = get_result(Policy, PolicySerializer, request.GET)
        return Response(result, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        result = post_result(Policy, PolicyImage, request)
        return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def submit_partywork(request):
    if request.method == 'POST':
        result = post_result(PartyWork, PartyWorkImage, request)
        return Response(result, status=status.HTTP_200_OK)



@api_view(['GET'])
def partywork_list(request,username):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    if not specified_person and not specified_party:
        return all()
    elif user.is_manager:
        return objects.filter(specified_party=True)
    else:
        return objects.filter
    """
    if request.method == 'GET':
        result = {"errCode":10000,"errDesc":errMsg[10000],"data":[]}
        users = User.objects.filter(username=username)
        objs = QuerySet()
        if users:
            ups = users[0].app_user.all()
            if ups and ups[0].is_verified:
                members = member.objects.filter(id_card=ups[0].real_idcard)
                if members:
                    print ups[0].is_manager
                    if ups[0].is_manager is 2:
                        objs = PartyWork.objects.filter((Q(specified=1)) | (Q(specified=2)) | (Q(specified_person=members[0])))
                    else:
                        objs = PartyWork.objects.filter((Q(specified=1)) | (Q(specified_person=members[0])))
                else:
                    result['errCode']=10012
                    result['errDesc']=errMsg[10012]
                    return Response(result,status = status.HTTP_200_OK)
            else:
                result['errCode']=10014
                result['errDesc']=errMsg[10014]
                return Response(result,status = status.HTTP_200_OK)
        else:
            result['errCode']=10006
            result['errDesc']=errMsg[10006]
            return Response(result,status = status.HTTP_200_OK)


        if objs.exists():
            startTime = request.GET.get('startTime', 0)

            if 'endTime' in request.GET.keys():
                endTime = request.GET.get('endTime')
            else:
                endTime = int(time.time())
            # startTime = time.localtime(float(request.GET.get('startTime',0)))
            # startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
            # if 'endTime' in request.GET.keys():
            #     endTime = time.localtime(float(request.GET.get('endTime')))
            #     endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
            # else:
            #     endTime = datetime.datetime.now()
            p = objs.filter(int_date__gt=startTime).filter(int_date__lt=endTime).order_by('-int_date')

            maxCount = int(request.GET.get('maxCount',0))
            offset = int(request.GET.get('offset',0))
            if maxCount:
                p = p[offset:offset+maxCount]
            else:
                p = p[offset:]
            pa = PartyWorkSerializer(p,many=True)
            result = {"errCode":10000,"errDesc":errMsg[10000],"data":pa.data}
    return Response(result,status = status.HTTP_200_OK)



@api_view(['GET'])
def process_list(request):
    if request.method == 'GET':
        process_type = request.GET.get('type','')
        result = {"errCode":10000,"errDesc":errMsg[10000],'data':{}}
        if process_type:
            if process_type not in ['join', 'setup', 'record']:
                result['errCode']=10015
                result['errDesc']=errMsg[10015]
                return Response(result,status = status.HTTP_200_OK)
            p = BusinessProcess.objects.filter(process_type=process_type)
            if p:
                ps = ProcessSerializer(p[0])
                result['data']=ps.data
                return Response(result,status = status.HTTP_200_OK)
            else:
                result['errCode']=10010
                result['errDesc']=errMsg[10010]
                logger.debug('specify type not existed:%s',process_type)
                return Response(result,status = status.HTTP_200_OK)
        else:
            result['errCode']=10011
            result['errDesc']=errMsg[10011]
            logger.debug('type is null, please specify a type')
    return Response(result,status = status.HTTP_200_OK)



@api_view(['GET'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def question_list(request,username):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        users = User.objects.filter(username=username)
        result = {"errCode":10000,"errDesc":errMsg[10000],"data":[]}
        if users:
            startTime = request.GET.get('startTime',0)
            # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
            if 'endTime' in request.GET.keys():
                endTime = request.GET.get('endTime')
            else:
                endTime = int(time.time())
            p = Question.objects.filter(question_author=username).filter(reply_int__gt=startTime).filter(reply_int__lte=endTime).order_by('-reply_int')

            maxCount = int(request.GET.get('maxCount',10))
            offset = int(request.GET.get('offset',0))

            p = p[offset:offset+maxCount]
            pa = QuestionSerializer(p,many=True)
            temp_data = []
            for temp in pa.data:
                if not temp['is_published']:
                    temp['question_answer'] = ''

                temp_data.append(temp)
            result['data']=temp_data
    elif request.method == 'POST':
        print 'Method is POST'
    return Response(result,status = status.HTTP_200_OK)


@api_view(['GET','POST'])
def worker_question_list(request):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        result = {"errCode":10000,"errDesc":errMsg[10000],"data":[]}
        # startTime = time.localtime(float(request.GET.get('startTime',0)))
        startTime = request.GET.get('startTime',0)
        action = request.GET.get('action', 0)
        # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
        if 'endTime' in request.GET.keys():
            endTime = request.GET.get('endTime')
        else:
            endTime = int(time.time())

        maxCount = int(request.GET.get('maxCount',10))
        offset = int(request.GET.get('offset',0))
        published = request.GET.get('is_published','false')
        if published == 'false':
            is_published = False
        else:
            is_published = True

        if action == '2':
            p = Question.objects.filter(reply_int__gt=startTime).filter(reply_int__lte=endTime).filter(is_published=is_published).order_by('reply_int')
        else:
            p = Question.objects.filter(reply_int__gt=startTime).filter(reply_int__lte=endTime).filter(is_published=is_published).order_by('-reply_int')

        p = p[offset:offset+maxCount]
        pa = QuestionSerializer(p,many=True)
        # temp_data = []
        # for temp in pa.data:
        #     if not temp['is_published']:
        #         temp['question_answer'] = u'未回复'

        #     temp_data.append(temp)
        result['data']=pa.data
    elif request.method == 'POST':
        result = {"errCode":10000,"errDesc":errMsg[10000]}
        question_id = request.DATA.get('question_id',0)
        answer = request.DATA.get('answer','')
        published = request.DATA.get('is_published', False)

        if not published:
            is_published = False
        else:
            is_published = True

        if question_id:
            try:
                q = Question.objects.get(question_id=question_id)
            except:
                result['errCode'] = 10017
                result['errDesc'] = errMsg[10017]
                return Response(result, status=status.HTTP_200_OK)
            q.question_answer = answer
            q.is_published = is_published
            q.save()
            return Response(result, status=status.HTTP_200_OK)
        else:
            result['errCode']=10017
            result ['errDesc']=errMsg[10017]
    return Response(result,status = status.HTTP_200_OK)


@api_view(['GET'])
def enter_list(request):
    result = {'errCode':10000,'errDesc':errMsg[10000]}
    if request.method == 'GET':
        enters = enterprise.objects.all()
        serializers = OutlineEnterSerializer(enters, many=True)
        result['data']=serializers.data
        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def enter_detail(request,pk):
    result = {'errCode':10000,'errDesc':errMsg[10000]}
    if request.method == 'GET':
        try:
            enter = enterprise.objects.get(enter_id=pk)
        except Exception, e:
            result['errCode']=10021
            result['errDesc']=errMsg[10021]
            return Response(result, status=status.HTTP_200_OK)

        es = EnterpriseSerializer(enter)
        result['data']=es.data
        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def member_detail(request,pk):
    result = {'errCode':10000,'errDesc':errMsg[10000]}
    if request.method == 'GET':
        try:
            enter = enterprise.objects.get(enter_id=pk)
        except Exception, e:
            result['errCode']=10021
            result['errDesc']=errMsg[10021]
            return Response(result, status=status.HTTP_200_OK)

        members = member.objects.filter(member_enter=enter)
        ms = OutlineMemberSerializer(members, many=True)
        result['data']=ms.data                                                                                                   
        return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def create_user(request):
    serialized = MyUserSerializer(data=request.DATA)
    if serialized.is_valid():
        print dir(serialized)
        print serialized.data

        username = serialized.init_data['username'],
        email = serialized.init_data['email'],
        password = serialized.init_data['password']

        u = User.objects.create_user(username,email,password)
        print u._meta.get_all_field_names()
        u.save()
        # u.set_password(serialized.init_data['password'])
        # try:
        #     u = User.objects.create(username=serialized.init_data['username'],password=serialized.init_data['password'],email=serialized.init_data['email'])
        # except Exception,e:
        #     print e
        # print type(u)
        print 'fadsfd'
        return Response(serialized.data,status = status.HTTP_201_CREATED)
        print serialized.data
    else:
        print 'else'
        print serialized.data
        return Response(serialized._errors,status = status.HTTP_400_BAD_REQUEST)


from xadmin.sites import site
from xadmin.views import BaseAdminView,CommAdminView
from django.template.response import TemplateResponse

class MyAdminView(BaseAdminView):
    def get(self,request,*args,**kwargs):
        return TemplateResponse(request,'test.html')

# class MyCommView(CommAdminView):
#     site_title = 'me_comm'


site.register_view(r'^me_test/$',MyAdminView,name='my_test')
# site.register_view(r'^me_comm/$',MyCommView,name='my_comm')


class ImportForm(forms.Form):
    import_file = forms.FileField(label=u'选择输入的文件')

    def __init__(self, *args, **kwargs):
        super(ImportForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit','Submit'))
    

class ImportAdminView(ImportMixin,CreateAdminView):
    add_form_template = 'model_form.html'
    import_template_name = 'model_form.html'
    new_context = {'msg':''}


    def get_context(self):
        '''
        re-implement import_action()
        '''
        resource = self.get_import_resource_class()()
        context = {}
        fileform = ImportForm
        fileform.helper = self.get_form_helper()
        if fileform.helper:
            fileform.helper.add_input(Submit('submit', 'Submit'))
        self.new_context.update( {'import_title':('从文件导入 %s') % force_unicode(self.opts.verbose_name),'fileform':fileform})
        context = super(CreateAdminView, self).get_context()
        context.update(self.new_context)
        self.new_context['msg'] = ''
        return context

    def post(self,request,*args,**kwargs):
        """
        here we can process the imported file,we can easily get the related model
        """
        if self.module_name == 'enterprise':
            CsvModel = EnterModel
        elif self.module_name == 'party':
            CsvModel = PartyModel
        elif self.module_name == 'member':
            CsvModel = MemberModel

        print self.model_admin_url('import')

        tmp_file = os.path.join(settings.MEDIA_ROOT, 'temp.csv')
	print 'sssssssssssssssss'
	print tmp_file
        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        try:
            data = request.FILES['import_file']
            default_storage.save(tmp_file, ContentFile(data.read()))
            convertFile(tmp_file)
        except Exception, e:
            print 'sssssssssssssssss'
            logger.debug(str(e))
	    print e
            self.new_context['msg']=u'请选择导入正确的文件'

        if os.path.isfile(outputDir) and os.path.getsize(outputDir) > 0:
            try:
                ft = open(outputDir,'r')
                ft.seek(3)
                ft.tell()
                mycsv = CsvModel.import_data(ft)
                os.remove(outputDir)
            except Exception, e:
                self.new_context['msg']=str(e)

        default_storage.delete(tmp_file)

        # ft = open(tmp_file,'r')
        # ft.seek(3)
        # ft.tell()
        # mycsv = PartyModel.import_data(ft)
        # print 'mycsv:',mycsv
        # datareader = csv.reader(ft)
        # print 'datareader',datareader
        # # line = f.readline()
        # # print line
        # for row in datareader:
        #     print row
        if self.new_context['msg']:
            return self.get(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/xadmin/')


site.register_modelview(r'^import/$',ImportAdminView,name='%s_%s_import')

def process_import(request):
    print request.FILES
    if request.POST:
        f = request.FILES['file']
        datareader = csv.reader(f)
        print datareader
        line = f.readline()
        print line
        for row in datareader:
            print row
    return HttpResponseRedirect('/xadmin/')
