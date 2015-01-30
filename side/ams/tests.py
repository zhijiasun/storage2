from django.test import TestCase
from django.test.client import Client
from ams.models import VersionManager, AppComment
from django_dynamic_fixture import G
import json

# Create your tests here.


class AppCommentTestCase(TestCase):
    def test_post_comment_with_valid_content(self):
        c = Client()
        data = {"app_version":"2.x.x.x","phone_info":"android phone","comment":"xxxxx"}
        response = c.post('/dangjian/laoshanparty/v1/comment/',data)
        result = json.loads(response.content)

        self.assertEquals(result['errCode'],10000)

    def test_post_comment_with_invalid_content(self):
        c = Client()
        data = {"app_version":"2.x.x.x", "comment":"xxxxx"}
        response = c.post('/dangjian/laoshanparty/v1/comment/',data)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10007)

        data1 = {"phone_info":"android phone","comment":"xxxxx"}
        response = c.post('/dangjian/laoshanparty/v1/comment/',data1)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10007)

        data2 = {"app_version":"2.x.x.x","phone_info":"android phone"}
        response = c.post('/dangjian/laoshanparty/v1/comment/',data2)
        result = json.loads(response.content)
        self.assertEquals(result['errCode'],10007)


class VersionManagerTestCase(TestCase):
    pass
