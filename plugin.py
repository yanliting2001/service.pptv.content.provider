#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012 Team-XBMC
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
#
#    This script is based on service.skin.widgets
#    Thanks to the original authors

import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from resources.lib import data

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_LANGUAGE = ADDON.getLocalizedString


def log(txt):
    message = '%s: %s' % (ADDON_NAME, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


class Main:

    def __init__(self):
        self._init_vars()
        self._parse_argv()
        for content_type in self.TYPE.split("+"):
            full_liz = list()
            if content_type == "recommendedsvip":
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
                data.parse_movies('recommendedsvip', 31074, full_liz, self.USECACHE, self.PLOT_ENABLE, self.LIMIT)
                xbmcplugin.addDirectoryItems(int(sys.argv[1]), full_liz)
            if content_type == "recommendedmovies":
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
                data.parse_movies('recommendedmovies', 31068, full_liz, self.USECACHE, self.PLOT_ENABLE, self.LIMIT)
                xbmcplugin.addDirectoryItems(int(sys.argv[1]), full_liz)
            elif content_type == "recommendedepisodes":
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                data.parse_tvshows_recommended('recommendedepisodes', 31013, full_liz, self.USECACHE, self.PLOT_ENABLE, self.LIMIT)
                xbmcplugin.addDirectoryItems(int(sys.argv[1]), full_liz)
            elif content_type == "recommendedvarieties":
                data.parse_movies('recommendedvarieties', 31069, full_liz, self.USECACHE, self.PLOT_ENABLE, self.LIMIT)
                xbmcplugin.addDirectoryItems(int(sys.argv[1]), full_liz)
            elif content_type == "recommendedchildren":
                data.parse_tvshows_recommended('recommendedchildren', 31070, full_liz, self.USECACHE, self.PLOT_ENABLE, self.LIMIT)
                xbmcplugin.addDirectoryItems(int(sys.argv[1]), full_liz)
            elif content_type == "recommendedcartoon":
                data.parse_tvshows_recommended('recommendedcartoon', 31071, full_liz, self.USECACHE, self.PLOT_ENABLE, self.LIMIT)
                xbmcplugin.addDirectoryItems(int(sys.argv[1]), full_liz)
            elif content_type == "recommendedmusicvideo":
                data.parse_tvshows_recommended('recommendedmusicvideo', 31075, full_liz, self.USECACHE, self.PLOT_ENABLE, self.LIMIT)
                xbmcplugin.addDirectoryItems(int(sys.argv[1]), full_liz)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))

    def _init_vars(self):
        self.WINDOW = xbmcgui.Window(10000)
        self.SETTINGSLIMIT = int(ADDON.getSetting("limit"))
        self.PLOT_ENABLE = ADDON.getSetting("plot_enable") == 'true'
        self.RANDOMITEMS_UNPLAYED = ADDON.getSetting("randomitems_unplayed") == 'true'

    def _parse_argv(self):
        try:
            params = dict(arg.split("=") for arg in sys.argv[2].split("&"))
        except Exception:
            params = {}
        self.TYPE = params.get("?type", "")
        self.ALBUM = params.get("album", "")
        self.USECACHE = params.get("reload", False)
        self.path = params.get("id", "")
        if self.USECACHE is not False:
            self.USECACHE = True
        self.LIMIT = int(params.get("limit", "-1"))
        self.dbid = params.get("dbid", "")
        self.dbtype = params.get("dbtype", False)


log('script version %s started' % ADDON_VERSION)
Main()
log('script version %s stopped' % ADDON_VERSION)
