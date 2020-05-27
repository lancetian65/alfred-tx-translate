#!/usr/bin/env python
# coding: utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
import urllib
import urllib2
import json
import time
import argparse
from urlparse import urlparse
import subprocess
import re
import socket
from distutils.version import LooseVersion

from alfred.feedback import Feedback


TOKEN_FILE = os.path.abspath('token')


SEARCH_API = 'https://fanyi.qq.com/api/translate/'

def _get_current_version():
    with open('./VERSION', 'r') as version_file:
        return version_file.read().strip()


CURRENT_VERSION = _get_current_version()


def _request(path, params=None, method='GET', data=None, headers=None):
    params = params or {}
    headers = headers or {}
    if method == 'GET':
        if params:
            url = path + '?' + urllib.urlencode(params)
        else:
            url = path
    if method == 'POST':
        data = urllib.urlencode(params)
        url = path
    request = urllib2.Request(url, data, headers)
    request.get_method = lambda: method
    response = urllib2.urlopen(request)
    return response.read()


def _api(path, params=None, method='GET', data=None, headers=None):
    response = _request(path=path, params=params, method=method, data=data,
                        headers=headers)
    result = json.loads(response)
    if result['translate']['errCode']:
        return None
    return result['translate']


def search(word):
    feedback = Feedback()
    data = _api(SEARCH_API,headers={'Host':'fanyi.qq.com','Origin':'https://fanyi.qq.com','Referer':'https://fanyi.qq.com/','Content-Type':'application/x-www-form-urlencoded'}, method='POST', params={'source': 'en','target':'zh','sourceText':word,'qtv':'3b438e4b45934643','qtk':'OvgyVz9mMm6gHObjMobt1nJPiE1QG6SS0WmCmWOHEARqyQw9LaVoTi3iCKmanY4EwP9XF82HWskv4l8pe8P3E/TVw/T+1MtbrzBSuvpJFc9zTXG4Jck1CUlLXVlAfbHthdDqzCluWPUEGnjTAOJyyQ==','sessionUuid':'translate_uuid1590576428257'})
    if data is None:
        return
    for chinese in data['records']:
        title = "%s [%s]" % (chinese['sourceText'], chinese['targetText'])
        feedback.addItem(title=title)

    feedback.output()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', nargs='?', type=str)
    args = parser.parse_args()
    if args.search:
        search(args.search)

if __name__ == '__main__':
    main()
