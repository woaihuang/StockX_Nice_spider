#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
from Ebook_spider.IP_pool import The_agent_poll
from bs4 import BeautifulSoup
import requests, random, os
import time




def choseagent():
    """
    构建User-Agent池，并调用返回一个User-Agent
    :return:User-Agent
    """
    user_agent_list = [
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"},
        {"user-agent": "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"},
        {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
    ]
    OneUserAgent = random.choice(user_agent_list)

    return OneUserAgent






def getHtml(link):
    """
    获取列表页的html，将页面写入到本地html文件
    :param link:
    :return:
    """
    print("****************************************开始执行获取章节列表函数****************************************")
    proxy_list = getproxy()

    header = choseagent()

    Html = requests.get(link, headers=header, proxies=random.choice(proxy_list))

    Html.encoding = 'gbk'

    return Html.text





def GetDirectory(deailurl, link):
    """
    获取章节名字、地址链接
    :return:章节名字列表、章节链接地址列表
    """
    print("****************************************开始执行章节、地址函数****************************************")
    chapterUrl = []
    chapterName = []

    htmlpage = getHtml(link)

    soup = BeautifulSoup(htmlpage, features="html.parser")

    a_tag = soup.select("div[id='list'] a")

    num = 1
    for i in a_tag:
        # chapterName.append("第{}章 {}".format(str(num), str(i.text).strip().split(' ')[1]))
        chapterName.append(i.text)
        num += 1
        chapterUrl.append('{}{}'.format(deailurl, i['href']))

    return chapterName, chapterUrl





def process(parameter):
    """
    多线程for循环函数，解决乱序问题，章节名字、章节内容、章节序号
    :param parameter:
    :return: 返回列表
    """
    ProDict = random.choice(parameter[2])

    header = choseagent()

    getTxtHtml = requests.get(parameter[0], headers=header, proxies=ProDict)

    getTxtHtml.encoding = 'gbk'

    soup = BeautifulSoup(getTxtHtml.text, features="lxml")

    txtfile = soup.select('div[id="content"]')

    time.sleep(random.randint(2, 4))

    for i in txtfile:
        repx = "新书上传，求收藏，求推荐！卖身求乳啊！亲,点击进去,给个好评呗,分数越高更新越快,据说给新笔趣阁打满分的最后都找到了漂亮的老婆哦!手机站全新改版升级地址：http://m.xbiquge.la，数据和书签与电脑站同步，无广告清新阅读！"
        chapterTxt = str(i.text).replace('    ', '\n\t').replace(repx, '').replace('*', '')

        return [parameter[1], chapterTxt, parameter[3]]







def getproxy():
    """
    获得一个代理IP和端口
    :return:
    """
    print("****************************************开始执行IP池函数****************************************")
    path = '/Users/huanghaoran/PycharmProject/my_spider_projects/Ebook_spider/IP_pool/ip.txt'

    if os.path.exists(path):
        os.remove(path)

    The_agent_poll.agent_poll().main()                      #调用IP池生成文件

    with open('/Users/huanghaoran/PycharmProject/my_spider_projects/Ebook_spider/IP_pool/ip.txt', 'r') as r:
        proxylist = r.readlines()

    proxy_list = []
    for i in proxylist:
        proxy_list.append(eval(i[:-1]))

    return proxy_list







def downlocldTxtFile(name, deailurl, link):
    """
    下载小说正文
    :return:
    """
    chapterName, chapterUrl = GetDirectory(deailurl, link)

    proxy_list = getproxy()

    all_parameter, name_content_list = [], []

    #**************************************创建for循环需要的列表******************************************
    for TxtUrl in range(len(chapterName)):
        one_list = []
        one_list.append(chapterUrl[TxtUrl])
        one_list.append(chapterName[TxtUrl])
        one_list.append(proxy_list)
        one_list.append(TxtUrl)
        all_parameter.append(one_list)

    #******************************为for循环创建多线程提供爬取速度*************************************************
    pool = ThreadPool(100)
    print("****************************************开始执行for循环多线程函数****************************************")
    name_content_list = pool.map(process, all_parameter)
    pool.close()
    pool.join()

    print("****************************************开始写入txt文件****************************************")
    name_content_list.sort(key=lambda x: x[2])                                                               #按照列表的第3列排序

    #*********************************将文本写入txt文件中***********************************************
    for i in name_content_list:
        with open('/Users/huanghaoran/PycharmProject/my_spider_projects/Ebook_spider/Ebook_files/{}.txt'.format(name), 'a') as f:
            f.write(i[0])
            f.write('\n')

            f.write(i[1])
            f.write('\n')







if __name__=="__main__":

    link_name = [['https://www.biquge.cm/0/278/', '无限恐怖', 'https://www.biquge.cm']]
    for i in link_name:
        downlocldTxtFile(i[1], i[2], i[0])