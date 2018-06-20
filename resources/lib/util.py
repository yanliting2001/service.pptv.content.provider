#!/usr/bin/env python
# coding=utf8


import urllib2
import re
import StringIO
import gzip
import xbmcvfs
import json
from common import *


def GetHttpData(url, data=None, cookie=None, use_qua=True):
    if use_qua:
        if data is None:
            url = url + "&Q-UA=" + qua
        else:
            data = data + "&Q-UA=" + qua
    log("Fetch URL :%s, with data: %s" % (url, data))
    print url
    for i in range(0, 2):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) {0}{1}'.
                           format('AppleWebKit/537.36 (KHTML, like Gecko) ',
                                  'Chrome/28.0.1500.71 Safari/537.36'))
            req.add_header('Accept-encoding', 'gzip')
            if cookie is not None:
                req.add_header('Cookie', cookie)
            if data:
                response = urllib2.urlopen(req, data, timeout=3)
            else:
                response = urllib2.urlopen(req, timeout=3)
            httpdata = response.read()
            if response.headers.get('content-encoding', None) == 'gzip':
                httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
            response.close()
            match = re.compile('encoding=(.+?)"').findall(httpdata)
            if not match:
                match = re.compile('meta charset="(.+?)"').findall(httpdata)
            if match:
                charset = match[0].lower()
                if (charset != 'utf-8') and (charset != 'utf8'):
                    httpdata = unicode(httpdata, charset).encode('utf8')
            break
        except Exception:
            print_exc()
            httpdata = '{"status": "Fail"}'
    return httpdata


def get_local_qua():
    addressfile = xbmcvfs.File(LOCAL_QUA_PATH)
    data = addressfile.read()
    addressfile.close()
    if data == '':
        # data = '{"qua":"QV=1&PR=VIDEO&PT=CH&CHID=10009&RL=1920*1080&VN=3.0.0&VN_CODE=120&SV=4.4.2&DV=MiBOX2&VN_BUILD=0"}'
        data = '{"qua":"QV=1&VN=1.1.27&PT=PVS&RL=1920x1080&IT=12117592000&OS=1.1.27&CHID=13032&DV=tencent_macaroni"}'
    data = json.loads(data)
    return urllib.quote_plus(data['qua'])


if xbmc.getCondVisibility('system.platform.Android'):
    LOCAL_QUA_PATH = '/data/data/qua'
else:
    LOCAL_QUA_PATH = ADDON.getSetting('qua')
qua = get_local_qua()
