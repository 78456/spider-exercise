#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'huangxin'

import urllib.request
from lxml import etree
import re
from multiprocessing.dummy import Pool as ThreadPool

class Tool(object):
    removeImg = re.compile('<img.*?>|\s{7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB(object):

    #初始化
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.tool = Tool()

    #获取页面html代码
    def getPage(self, pageIndex):
        try:
            url = self.baseUrl + '&pn=' + str(pageIndex)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
            return html
        except urllib.request.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
                return None
            if hasattr(e, 'reason'):
                print('连接百度贴吧失败，错误原因是,',e.reason)
                return None

    #获取标题
    def getTitle(self):
        pageCode = self.getPage(1)
        selector = etree.HTML(pageCode)
        title = selector.xpath('//h3/text()')
        if title:
            return title[0].strip()
        else:
            return None
    #获取总页数
    def getPageNum(self):
        pageCode = self.getPage(1)
        selector = etree.HTML(pageCode)
        pageNum = selector.xpath('//li[@class="l_reply_num"]/span[@class="red"]/text()')
        return pageNum[1]

    #获取内容
    def getContent(self, page):
        contents = []
        pageCode = self.getPage(page)
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, pageCode)
        for item in items:
            content = '\n'+self.tool.replace(item)+'\n'
            contents.append(content)
        return contents

    #写入文件
    def wirtefile(self, contents):
        with open(self.getTitle()+'.txt', 'w') as f:
            for item in contents:
                for content in item:
                    f.write('\n'+'--------------------------------------------------华丽丽的分割线----------------------------'
                                 '---------------------'+'\n')
                    f.write(content)

if __name__ == "__main__":
    baseURL = 'http://tieba.baidu.com/p/3138733512?see_lz=1'
    bdtb = BDTB(baseURL)
    size = []
    for i in range(int(bdtb.getPageNum())):
        size.append(i+1)
    #多线程
    pool = ThreadPool(8)
    result = pool.map(bdtb.getContent, size)
    pool.close()
    pool.join()
    bdtb.wirtefile(result)







