#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'huangxin'
import urllib
import urllib.request
from lxml import etree
from time import sleep

class QSBK(object):

    #初始化变量
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.pageIndex = 1
        self.headers = {'User-Agent': self.user_agent}

    #获取页面html代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
            return html
        except urllib.request.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
                return None
            if hasattr(e, 'reason'):
                print(e.reason)
                return None

    #获取页面想要的内容
    def getPageItem(self, pageIndex):
        #存放所有内容
        stories = []
        pagebegin = pageIndex
        #获取此页html代码
        pageCode = self.getPage(pagebegin)
        while pageCode and len(stories) < 35:
            #获取xpath可解析的格式
            selector = etree.HTML(pageCode)
            #解析想要的内容
            content = selector.xpath('//div[@class="content"]/text()')
            stories.append(content)
            next_page = selector.xpath('//ul[@class="pagination"]/li/a/span[@class="next"]/text()')
            #判断是否有下一页，如果有下一页则获取下一页html代码，如果没有终止循环
            if next_page:
                pagebegin += 1
                pageCode = self.getPage(pagebegin)
                sleep(1)
                print('第{}页的段子已经被爬下来'.format(len(stories)))
                print(content)
            else:
                break
        return stories


spider = QSBK()
c = spider.getPageItem(1)
for each in c:
    print(each)


