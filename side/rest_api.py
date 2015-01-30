#!/usr/bin/python
import requests
import json
import sys
import argparse


# parser = argparse.ArgumentParser()
# parser.add_argument('-m',dest='method',help='the method of the http request')
# parser.add_argument('-u',dest='url',help='the url of the http address')
# parser.add_argument('-d',dest='data',type=dict,help='the data of the request')
# parser.add_argument('-e',dest='headers',type=dict,help='the headers of the request')

# result = parser.parse_args()
# print result

# if len(sys.argv) > 1:
#     options, args = parser.parse_args()
#     method = options.get('method','')
#     url = options.get('url','')
#     data = options.get('data',{})
#     headers = options.get('headers',{})
#     print method,url,data,headers
# else:
#     print parser.print_help()
# payload2 = {"username":"","password":"123456"}
# url4 = 'http://115.28.79.151:8081/dangjian/laoshanparty/v1/login/'
# r = requests.post(url4,data=payload2)
# print r.text
# print r.status_code

r = requests.get('http://192.168.1.103:8081/dangjian/laoshanparty/v1/pioneer')
print r.text
print r.encoding
r.encoding =''

print r.json()
