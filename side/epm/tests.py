from django.test import TestCase
from django.test.client import Client
from epm.models import Pioneer, member, UserProfile, WorkUserProfile,Question, enterprise
from datetime import datetime
from django.contrib.auth.models import User
from django_dynamic_fixture import G
import json

# Create your tests here.

class QuestionTestCase(TestCase):
    def setUp(self):
        # pass
        u = G(User, username='test',password='123456')
        up = G(UserProfile,user=u)
        q = G(Question, question_title='test question', question_author='test',question_type=0,question_content='test content')
        q1 = G(Question, question_title='test question1', question_author='test',question_type=1,question_content='test content 1')

    def test_get_questions(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/test/questions')
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)

    def test_get_questions_with_param(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/test/questions?maxCount=1')
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)
        self.assertEquals(len(result['data']),1)

    def test_post_question(self):
        data = {"question_type":1,"question_content":"test question content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/test/question/',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)

        response1 = c.get('/dangjian/laoshanparty/v1/test/questions')
        result1 = json.loads(response1.content)
        self.assertEquals(result1['errCode'],10000)
        self.assertEquals(len(result1['data']),3)

    def test_post_question_with_invalid_param(self):
        data = {"question_type":1,"question_content":"test question content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/invalid_username/question/',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10006)

        response1 = c.get('/dangjian/laoshanparty/v1/test/questions')
        result1 = json.loads(response1.content)
        self.assertEquals(result1['errCode'],10000)
        self.assertEquals(len(result1['data']),2)


class WorkerQuestionTestCase(TestCase):
    def setUp(self):
        u = G(User, username='test',password='123456')
        up = G(UserProfile,user=u)
        q1 = G(Question, question_title='test question1', question_author='test',question_type=1,question_content='test content1')
        q2 = G(Question, question_title='test question2', question_author='test',question_type=2,question_content='test content2')
        q3 = G(Question, question_title='test question3', question_author='test',question_type=3,question_content='test content3')

    def test_get_all_published_questions(self):
        q4 = G(Question, question_title='test question4', question_author='test',question_type=4,question_content='test content4')
        q4.is_published = True
        q4.save()
        c = Client()
        response = c.get('/dangjian/lspmanager/v1/questions?is_published=true')
        result = json.loads(response.content)
        self.assertEquals(result['errCode'], 10000)
        self.assertEquals(len(result['data']), 1)

    def test_get_all_unpublished_questions(self):
        c = Client()
        response = c.get('/dangjian/lspmanager/v1/questions?is_published=false')
        result = json.loads(response.content)
        self.assertEquals(result['errCode'], 10000)
        self.assertEquals(len(result['data']), 3)

    def test_update_specified_question(self):
        data = {"question_id":1,"answer":"answer for test question", "published": "false"}
        c = Client()
        response = c.post('/dangjian/lspmanager/v1/questions', data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'], 10000)

        response1 = c.get('/dangjian/lspmanager/v1/questions?is_published=false')
        result1 = json.loads(response1.content)
        self.assertEquals(result1['errCode'], 10000)
        self.assertEquals(len(result1['data']), 3)

    def test_publish_specified_question(self):
        data = {"question_id":1,"answer":"answer for test question", "is_published": "true"}
        c = Client()
        response = c.post('/dangjian/lspmanager/v1/questions', data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'], 10000)

        response1 = c.get('/dangjian/lspmanager/v1/questions?is_published=true')
        result1 = json.loads(response1.content)
        self.assertEquals(result1['errCode'], 10000)
        self.assertEquals(len(result1['data']), 1)

        response2 = c.get('/dangjian/lspmanager/v1/questions?is_published=false')
        result2 = json.loads(response2.content)
        self.assertEquals(result2['errCode'], 10000)
        self.assertEquals(len(result2['data']), 2)


class PioneerTestCase(TestCase):
    
    def test_pioneer_create(self):
        p = Pioneer.objects.create(title='first pioneer title',date=datetime.now(),author='first author',content='content')
        self.assertEquals(p.title, 'first pioneer title')


class PioneerListTestCase(TestCase):

    def test_get_pioneer(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/pioneer')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)


class LifeTipsListTestCase(TestCase):

    def test_get_lifetips(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/lifetips')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)

    def test_post_lifetips(self):
        data = {"title":"first title","author":"test","content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/lifetips',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)

    def test_post_lifetips_with_invliad(self):
        data = {"title":"first title", "content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/lifetips',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10007)


class NoticeListTestCase(TestCase):

    def test_get_notice(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/notice')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)

    def test_post_notice(self):
        data = {"title":"first title","author":"test","content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/notice',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)
        
    def test_post_notice_with_invliad(self):
        data = {"title":"first title", "content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/notice',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10007)


class SpiritListTestCase(TestCase):

    def test_get_spirit(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/spirit')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)

    def test_post_spirit(self):
        data = {"title":"first title","author":"test","content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/spirit',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)

    def test_post_spirit_with_invliad(self):
        data = {"title":"first title", "content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/spirit',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10007)


class PolicyListTestCase(TestCase):

    def test_get_plicy(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/policy')
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)

    def test_post_policy(self):
        data = {"title":"first title","author":"test","content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/policy',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)

    def test_post_policy_with_invliad(self):
        data = {"title":"first title", "content":"first content"}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/policy',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10007)

class PorcessListTestCase(TestCase):

    def test_get_null_process(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/process')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10011)

    def test_get_join_process_without_data(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/process?type=join')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10010)

    def test_get_invalid_type_process(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/process?type=invliad')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10015)


class WorkUserRegisterTestCase(TestCase):
    def setUp(self):
        pass
        # user = G(User,username='testUser', password='123456')
        # up = G(UserProfile, user=user)
        # user2 = G(User, username='testWorker', password='123456')
        # worker = G(WorkUserProfile, user=user2)
        # print 'set up ********************'

    def test_worker_register_ok(self):
        pass
        # user = G(User,username='testUser', password='123456')
        # up = G(UserProfile, user=user)
        # user2 = G(User, username='worker', password='123456')
        # worker = G(WorkUserProfile, user=user2)

        # c = Client()
        # data = {'username':'worker','password':'123456'}
        # response = c.post('/dangjian/lspmanager/v1/login/',data)
        # print response.content
        # result = json.loads(response.content)
        # self.assertEquals(result['errCode'],10000)



class UserRegisterTestCase(TestCase):

    def test_user_register_successfully(self):
        c= Client()
        data = {'username':'test', 'email':'test@test.com','password':'123456'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)

    def test_user_register_without_username(self):
        c = Client()
        data = {'email':'test@test.com','password':'123456'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10016)

    def test_user_register_without_email(self):
        c = Client()
        data = {'username':'test','password':'123456'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'], 10000)

    def test_user_register_without_password(self):
        c = Client()
        data = {'usename':'test','email':'test@test.com'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10016)

    def create_existed_user(self):
        u = User.objects.create_user('username=test','password=123456')
        u.save()
        
    def test_user_register_with_existed_username(self):
        pass


class UserLoginTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username="jason",password="111111",email="fad@testc.om")
        up = G(UserProfile, user=u1)

    def test_user_login(self):
        data = {'username': 'jason', 'password': '111111'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/login/', data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10000)

    def test_user_with_invliad_login(self):
        data = {'username': 'jason1', 'password': '111111'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/login/', data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10003)

    def test_user_change_password(self):
        data = {'old_password': '111111', 'new_password1': '222222', 'new_password2':'222222'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/jason/password/change/', data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'], 10000)

    def test_user_change_password_with_invalid_old_password(self):
        data = {'old_password': 'invalid', 'new_password1': '222222', 'new_password2':'222222'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/jason/password/change/', data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'], 10003)

    def test_user_change_password_with_invalid_param(self):
        data = {'old_password': '111111', 'password1': '222222', 'new_password2':'222222'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/jason/password/change/', data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'], 10018)



class GetUserInfoTestCase(TestCase):

    fixtures = ['admin.json','epm.json']

    def test_get_valid_user_info(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/test/info/')
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)
        self.assertTrue('is_verified' in result['data'].keys())
        self.assertTrue('real_organization' in result['data'].keys())
        self.assertTrue('real_idcard' in result['data'].keys())
        self.assertTrue('is_manager' in result['data'].keys())
        self.assertTrue('real_name' in result['data'].keys())

    def test_get_invalid_user_info(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/invalid/info/')
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10006)
        self.assertTrue('data' not in result.keys())


class MemberVerifyTestCase(TestCase):

    def test_member_verify_with_valid_info(self):
        #initialize the needed data
        m = G(member,member_name='test_name',id_card='123456789012345678')
        user = G(User,username='testMember',password='123456')
        up = G(UserProfile, user=user)

        data = {'real_name':'test_name','real_idcard':'123456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/testMember/member/verify/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)

    def test_member_verify_with_invliad_info(self):
        m = G(member,member_name='test_name',id_card='123456789012345678')
        user = G(User,username='testMember',password='123456')
        up = G(UserProfile, user=user)

        #with invliad real_name
        data = {'real_name':'test_invliad_name','real_idcard':'123456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/testMember/member/verify/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10005)

        #with invliad real_idcard
        data1 = {'real_name':'test_name','real_idcard':'223456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/testMember/member/verify/', data1)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10005)


        #with invliad username in api
        data2 = {'real_name':'test_name','real_idcard':'123456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/invalid_name/member/verify/', data2)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10006)

class EnterTestCase(TestCase):
    def setUp(self):
        self.clinet = Client()
        enter1 = G(enterprise,enter_id=1,enter_name="enter1")
        enter2 = G(enterprise,enter_id=2,enter_name="enter2")
        enter3 = G(enterprise,enter_id=3,enter_name="enter3")
        

    def test_get_all_enters(self):
        response = self.client.get('/dangjian/laoshanparty/v1/enters/')
        result = json.loads(response.content)
        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)
        self.assertEquals(len(result['data']),3)


    def test_get_concrete_enter(self):
        response = self.client.get('/dangjian/laoshanparty/v1/enters/1/')
        result = json.loads(response.content)
        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)
        self.assertEquals(result['data']['enter_id'],1)
        self.assertEquals(result['data']['enter_name'],'enter1')

        response = self.client.get('/dangjian/laoshanparty/v1/enters/2/')
        result = json.loads(response.content)
        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)
        self.assertEquals(result['data']['enter_id'],2)
        self.assertEquals(result['data']['enter_name'],'enter2')

        response = self.client.get('/dangjian/laoshanparty/v1/enters/4/')
        result = json.loads(response.content)
        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10021)
