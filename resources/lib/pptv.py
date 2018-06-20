#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2015 PivosGroup
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

import xbmc
import util


class PPTVClass():
    HOMEHOST = 'tv.api.pptv.com'
    LISTHOST = 'epg.androidtv.cp61.ott.cibntv.net'
    DETAILHOST = 'epg.api.cp61.ott.cibntv.net'
    RELATEHOST = 'recommend.cp61.ott.cibntv.net'
    APPHOST = 'market.ott.cdn.pptv.com'
    TOPICHOST = 'tv.api.cp61.ott.cibntv.net'
    HOMEAPI = 'http://' + HOMEHOST + '/ppos/'
    LISTAPI = 'http://' + LISTHOST + '/'
    DETAILAPI = 'http://' + DETAILHOST + '/'
    RELATEAPI = 'http://' + RELATEHOST + '/'
    APPAPI = 'http://' + APPHOST + '/api/v2/'
    SHOPAPI = 'http://' + HOMEHOST + '/shop/'
    TOPICAPI = 'http://' + TOPICHOST + '/atvcibn/special/'
    PPI = 'AgACAAAAAgAATksAAAACAAAAAFhhPoA6c6A7DfvkYyt22APc1w5-U9eq5FEUyr9iLBpUpnnnNllkZwqRN9RI3cu6j9lIVJKHmXQgCh4K15mHQ1Cd8drT'

    def __init__(self, LocalDebug=False):
        self.LOCAL_DEBUG = LocalDebug

    def get_home_content(self):
        return util.GetHttpData(self.HOMEAPI + 'four/home?version={version}&channel_id={channel_id}&ppi={ppi}'.format(version="4.0.3", channel_id="1110141", ppi=self.PPI))

    def get_recommended_config(self):
        return util.GetHttpData(self.HOMEAPI + 'rcmdNavConfig?version={version}&channel_id={channel_id}&ppi={ppi}'.format(version="4.0.3", channel_id="1110141", ppi=self.PPI), use_qua=False)

    def get_channel_config(self):
        return util.GetHttpData(self.HOMEAPI + 'channel_config?version={version}&channel_id={channel_id}&ppi={ppi}'.format(version="4.0.3", channel_id="1110141", ppi=self.PPI), use_qua=False)

    def get_channel_list_config(self, typeId, pn, ps, str_filter, sortType):
        url = self.LISTAPI + 'newList.api?auth={auth}&appver={appver}&canal={canal}&appid={appid}&appplt={appplt}&hasVirtual={hasVirtual}&typeId={typeId}&ps={ps}&pn={pn}&sortType={sortType}&contype={contype}&coverPre={coverPre}&ppi={ppi}&format={format}&isShowNav={isShowNav}&cannelSource={cannelSource}&ver={ver}'
        url = url.format(
            auth="1",
            appver="4.0.4",
            canal="CIBN",
            appid="PPTVLauncherSafe",
            appplt="launcher",
            hasVirtual=False,
            typeId=typeId,
            ps=ps,
            pn=pn,
            sortType=sortType,
            contype=0,
            coverPre="sp160",
            ppi=self.PPI,
            format="json",
            isShowNav="true",
            cannelSource="VST",
            ver="1"
        )
        if str_filter:
            url = url + '&' + str_filter
        return util.GetHttpData(url, use_qua=False)

    def get_video_detail(self, vid):
        url = self.DETAILAPI + 'detail.api?auth={auth}&virtual={virtual}&ppi={ppi}&token={token}&appplt={appplt}&appid={appid}&appver={appver}&username={username}&type={type}&platform={platform}&vid={vid}&ver={ver}&lang={lang}&vvid={vvid}&gslbversion={gslbversion}&userLevel={userLevel}&coverPre={coverPre}&format=json'
        url = url.format(
            auth="1",
            virtual="0",
            ppi=self.PPI,
            token="",
            appplt="launcher",
            appid="com.pptv.launcher",
            appver="4.0.3",
            username="",
            type="ppbox.launcher",
            platform="launcher",
            vid=vid,
            ver="3",
            lang="zh_CN",
            vvid="90f1d8a5-106c-48d4-b806-fec3e5fa58fe",
            gslbversion="2",
            userLevel="0",
            coverPre="sp423")
        return util.GetHttpData(url, use_qua=False)

    def get_video_relate(self, cid):
        url = self.RELATEAPI + 'recommend?appplt={appplt}&appid={appid}&appver={appver}&src={src}&video={video}&uid={uid}&num={num}&ppi={ppi}&extraFields={extraFields}&userLevel={userLevel}&vipUser={vipUser}&format=json'
        url = url.format(
            appplt="launcher",
            appid="pptvLauncher",
            appver="4.0.4",
            src="34",
            video=cid,
            uid="pptv",
            num=7,
            ppi=self.PPI,
            extraFields="douBanScore,isPay,vt,vipPrice,coverPic,isVip,score,epgCatas",
            userLevel="1",
            vipUser="0")
        return util.GetHttpData(url, use_qua=False)

    def get_playinfo(self, vid):
        if not xbmc.getCondVisibility('system.platform.Android'):
            return '[{"url":"C:/Download/20160810-111059351.mkv","ft":0}]'
        return util.GetHttpData('http://127.0.0.1:6666/pivos/getVideoURL?vid={vid}'.format(vid=vid), use_qua=False)

    def get_userinfo(self):
        if not xbmc.getCondVisibility('system.platform.Android'):
            return '{"token": "baioHxWw7aoKgFgkQLKuZft9YzUwONazKPnAG8ZATRCr1lEKBsc5MJsA0Yi4Nu9KBPlGYNNxCxlv\nCoXFfLaS7QNBE8x7sEZz9vjlXW7UjtttKPloeqUJ6yxzaElK_vzhkHMUHq9Rpq9K5CQNMLPv9q6Q\nRjF6xmzFiZeZRXoIuXs\n", "username": "13868191875", "vipgrade": 0, "face": ""}'
        return util.GetHttpData('http://127.0.0.1:6667/pivos/getUserInfo?vid=1234', use_qua=False)

    def get_video_subscribe(self, vid):
        if not xbmc.getCondVisibility('system.platform.Android'):
            return '{"nameValuePairs": {"userBuyed": false, "buyedExpired": true, "userBuyedValidTime": 0, "errorCode": "0", "shareStatus": 0, "ticketStatus": 0, "message": "success", "channel": {"nameValuePairs": {"shareStatus": 0, "id": 8947, "title": "\u591c\u884c\u52a8\u7269", "channelVT": 3, "channelID": 25476815, "liveEndTime": 0, "buyStartTime": 0, "status": 0, "liveStartTime": 0, "filmSource": "", "vipPrice": 2.0, "parentChannelID": 0, "cataId": 1, "epFreeNum": 0, "ticketStatus": 0, "vodFreeTime": 300, "vodBuyTime": 604800, "sectionID": 0, "promotePrice": 5.0, "policyId": "", "liveBuyTime": 0, "listPrice": 5.0}}}}'
        url = 'http://127.0.0.1:6667/pivos/getDdpContentInfo?vid={vid}'.format(vid=vid)
        return util.GetHttpData(url, use_qua=False)

    def get_app_config(self):
        return util.GetHttpData(self.APPAPI + 'launRec?platform={platform}&cno={cno}&ver={ver}'.format(platform="launcher", cno="1110141", ver="4.0"), use_qua=False)

    def get_video_topic(self, tid):
        return util.GetHttpData(self.TOPICAPI + tid + '?version={version}&channel_id={channel_id}&user_level={user_level}'.format(version="4.0.3", channel_id="200026", user_level="0"))

    def get_sport_config(self):
        return util.GetHttpData(self.HOMEAPI + 'sportNav?version=4.0.3', use_qua=False)

    def get_shopping_config(self):
        return util.GetHttpData(self.SHOPAPI + 'getGoods', use_qua=False)