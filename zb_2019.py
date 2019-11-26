#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-25 11:41:50
@LastEditors: Youshumin
@LastEditTime: 2019-11-25 14:19:34
@Description: 
'''
import json
import logging
import os
import re
import urllib
from distutils.filelist import findall
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

LOG = logging.getLogger(__name__)


def check_file(file_path):
    """检测文件是否存在不存则创建"""
    splist_file_path = file_path.split("/")
    if len(splist_file_path) > 1:
        file_path = "/".join(splist_file_path[:-1])
    if not os.path.exists(file_path):
        try:
            os.makedirs(file_path)
        except Exception:
            pass


def make_file_path(file_path_list):
    """组装文件路径 兼容windown和linxu"""
    file_path = ""
    for item in file_path_list:
        file_path = os.path.join(file_path, item)
    if file_path:
        check_file(file_path)
    return file_path


def make_request_url(url, value=None):
    """拼装请求地址"""
    if value:
        requests_url = "{}/{}".format(url, value)
    else:
        requests_url = "{}".format(url)
    print("请求地址是: %s" % requests_url)
    return requests_url


def handler_index_page(contents):
    """ 首页面bs处理 """
    reps_list = []
    soup = BeautifulSoup(contents, "html.parser")
    for tag in soup.find_all("ul", class_="game-index-list"):
        for item in tag.findAll("li"):
            m_href = item.find("a").get("herf")
            m_name = item.find("a").get_text()
            reps_list.append(dict(name=m_name, herf=".{}.heml".format(m_href)))
    return reps_list


def handler_game_sub_page(contents):
    """
    game 自页面处理
    """
    sub_list = []
    soup = BeautifulSoup(contents, "html.parser")
    for msg in soup.find_all('ul', class_='type-list-auto'):
        for lists in msg.findAll('li'):
            n_tag = lists.find('span', class_='type-tag').get_text()
            if (n_tag == "全民直播"):
                continue
            n_href = lists.find('a').get('href')
            n_bimg = lists.find('a').find('img',
                                          class_='type-bigimg').get('data-src')
            n_simg = lists.find('a').find('div', class_='type-txt').find(
                'img', class_='type-smallimg').get('data-src')
            n_title = lists.find('a').find('h5').get_text()
            n_name = lists.find('a').find('p').find('span',
                                                    class_='left').get_text()
            n_heat = lists.find('a').find('p').find('span',
                                                    class_='right').get_text()
            if (n_simg == ""):
                n_simg == "../img/und.jpg"
            sub_list.append({
                'name': n_name,
                'href': n_href,
                'bimg': n_bimg,
                'simg': n_simg,
                'tag': n_tag,
                'title': n_title,
                'heat': n_heat,
            })
    return sub_list


def get_page(urlBase, urlValue, fileList, urlRange=None):
    """获取页面内容后给bs处理并保存结果到文件"""
    req_url = make_request_url(urlBase, urlValue)
    w_data = []
    if urlRange:
        all_list = []
        for pageNum in range(1, urlRange):
            if "?" in req_url:
                req_url = "{}&page={}".format(req_url, pageNum)
            else:
                req_url = "{}?page={}".format(req_url, pageNum)
            page = urllib.request.urlopen("{}".format(req_url))
            pageContents = page.read()
            pageContents = pageContents.decode("utf-8")
            sub_list = handler_game_sub_page(pageContents)
            for item in sub_list:
                all_list.append(item)
        w_data = all_list
        # BeautifulSoup class = type-list-auto
    else:
        page = urllib.request.urlopen("{}".format(req_url))
        pageContents = page.read()
        pageContents = pageContents.decode("utf-8")
        # BeautifulSoup   class = game-index-list or
        w_data = handler_index_page(pageContents)

    w_file = make_file_path(fileList)
    if w_data:
        with open(w_file, "w+", encoding="utf-8") as f:
            f.write(json.dumps(w_data, indent=2, ensure_ascii=False))
            f.close()
    return


if __name__ == "__main__":
    URLBASE = "http://www.shengui.tv/game"
    GIRLBASE = "http://www.shengui.tv"
    index_game = dict(
        game_index=[URLBASE, "", ["data", "json", "data.json"], ""],
        game_page=[URLBASE, "", ["data", "json", "main-data.json"], 101],
        game_lol=[URLBASE, "lol", ["data", "json", "data-lol.json"], 99],
        game_jdqs=[URLBASE, "jdqs", ["data", "json", "data-jdqs.json"], 99],
        game_wzry=[URLBASE, "wzry", ["data", "json", "data-wzry.json"], 99],
        game_qhyx=[URLBASE, "qhyx", ["data", "json", "data-qhyx.json"], 99],
        game_sjcj=[URLBASE, "sjcj", ["data", "json", "data-sjcj.json"], 99],
        game_dnf=[URLBASE, "dnf", ["data", "json", "data-dnf.json"], 99],
        game_dota2=[URLBASE, "dota2", ["data", "json", "data-dota2.json"], 99],
        game_cf=[URLBASE, "cf", ["data", "json", "data-cf.json"], 99],
        game_swxf=[URLBASE, "swxf", ["data", "json", "data-swxf.json"], 99],
        game_yys=[URLBASE, "yys", ["data", "json", "data-yys.json"], 99],
        game_lscs=[URLBASE, "lscs", ["data", "json", "data-lscs.json"], 99],
        game_zjyx=[URLBASE, "zjyx", ["data", "json", "data-zjyx.json"], 99],
        game_qpyx=[URLBASE, "qhyx", ["data", "json", "data-qpyx.json"], 99],
        game_hyrzsy=[
            URLBASE, "hyrzsy", ["data", "json", "data-hyrzsy.json"], 99
        ],
        game_csgo=[URLBASE, "csgo", ["data", "json", "data-csgo.json"], 99],
        game_blzy=[URLBASE, "blzy", ["data", "json", "data-blzy.json"], 99],
        game_wdsj=[URLBASE, "wdsj", ["data", "json", "data-wdsj.json"], 99],
        game_mszb=[URLBASE, "mszb", ["data", "json", "data-mszb.json"], 99],
        girl_all=[GIRLBASE, "beauty", ["data", "json", "girl-all.json"], 99],
        girl_star=[
            GIRLBASE, "beauty?tagId=74", ["data", "json", "girl-all.json"], 99
        ],
        girl_music=[
            GIRLBASE, "beauty?tagId=121", ["data", "json", "girl-music.json"],
            99
        ],
        girl_talking=[
            GIRLBASE, "beauty?tagId=123",
            ["data", "json", "girl-talking.json"], 99
        ],
    )

    for name, info in index_game.items():
        urlBase = info[0]
        urlValue = info[1]
        fileList = info[2]
        urlRange = info[3]
        get_page(urlBase, urlValue, fileList, urlRange)