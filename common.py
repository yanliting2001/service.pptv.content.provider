#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import traceback
import urllib
import time

ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
CHANNEL_ID_MAP = {"movie": "1",
                  "tv": "2",
                  "cartoon": "3",
                  "variety": "4",
                  "children": "210784",
                  "svip": "75099",
                  "music": "75199"}


def log(txt):
    message = '%s: %s' % (ADDON_NAME, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


def print_exc():
    traceback.print_exc()


def item_remap(detail, landscape, is_tvshow=False):
    pptv_id = detail['vid']
    art_dict = {"fanart": "",
                "landscape": landscape,
                "poster": detail['imgurl']}
    casts = []
    str_id = "tvshowid" if is_tvshow else "movieid"
    for (count, k) in enumerate(detail['actors']):
        item = {"name": k['name'],
                "order": count,
                "role": "",
                "thumbnail": ""}
        casts.append(item)
    return {
        "art": art_dict,
        "cast": casts,
        "country": detail.get('area').split(','),
        "dateadded": detail.get('onlinetime')[:10],
        "director": detail.get('director'),
        "file": "plugin://plugin.proxy.video?action=pptv_play&amp;cid={0}&amp;vid={1}".format(pptv_id, pptv_id),
        "path": "plugin://plugin.proxy.video?action=pptv_play&amp;cid={0}&amp;vid={1}".format(pptv_id, pptv_id),
        "genre": detail.get('catalog').split(','),
        "imdbnumber": "",
        "label": detail.get('title'),
        "lastplayed": "",
        str_id: pptv_id,
        "mpaa": "",
        "originaltitle": detail.get('title'),
        "playcount": 0,
        "plot": detail.get('content'),
        "plotoutline": detail.get('moreTitle'),
        "rating": '0.0' if not detail.get('mark') else detail.get('mark'),
        "resume": {"position": 0, "total": 0},
        "runtime": 0,
        "streamdetails": {},
        "studio": [],
        "tagline": detail.get('moreTitle'),
        "title": detail.get('title'),
        "trailer": "",
        "votes": "",
        "writer": [],
        "year": detail.get('year')
    }


def item_episode(data, tv_item, total_num):
    listitem = {}
    video_num = total_num
    episode = data[0]
    epi_id = episode['_attributes']['id']
    listitem["art"] = {"season.poster": tv_item['art']['poster'],
                       "thumb": episode['_attributes']['sloturl'],
                       "tvshow.fanart": tv_item['art']['fanart'],
                       "tvshow.poster": tv_item['art']['poster']}
    listitem["cast"] = tv_item['cast']
    listitem["dateadded"] = episode['_attributes']['createTime'][:10]
    listitem["director"] = tv_item['director']
    listitem["episode"] = video_num
    listitem["episodeid"] = epi_id
    listitem["file"] = "plugin://plugin.proxy.video?action=pptv_play&amp;cid={0}&amp;vid={1}".format(tv_item['tvshowid'], epi_id)
    listitem["path"] = "plugin://plugin.proxy.video?action=pptv_play&amp;cid={0}&amp;vid={1}".format(tv_item['tvshowid'], epi_id)
    listitem["firstaired"] = tv_item['dateadded']
    listitem["label"] = episode['_attributes']['subtitle']
    listitem["lastplayed"] = 0
    listitem["playcount"] = 0
    listitem["plot"] = tv_item['plot']
    listitem["rating"] = 0
    listitem["resume"] = tv_item['resume']
    listitem["runtime"] = episode['_attributes']['duration']
    listitem["season"] = 1
    listitem["showtitle"] = tv_item['tagline']
    listitem["streamdetails"] = tv_item['streamdetails']
    listitem["title"] = tv_item['label']
    listitem["tvshowid"] = tv_item['tvshowid']
    listitem["writer"] = tv_item['writer']
    return listitem


def create_json_rpc(listitems, channel):
    json_query = {}
    json_query['id'] = 1
    json_query['jsonrpc'] = 2.0
    if listitems:
        json_query['result'] = {}
        json_query['result'][channel] = listitems
    return json_query


def set_image_path(url):
    path = "image://"
    if url:
        path = path + urllib.quote_plus(url) + "/"
    return path


def get_datetime_str():
    return time.strftime("%Y-%m-%d") + " " + time.strftime("%H:%M:%S")
