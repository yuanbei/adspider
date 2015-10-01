#coding:utf8

"""
crawler.py
~~~~~~~~~~~~~

主要模块，爬虫的具体实现。
"""

from urlparse import urljoin,urlparse
from collections import deque
import re
import traceback
from locale import getdefaultlocale
import logging
import time

from bs4 import BeautifulSoup 

from database import Database
from webPage import WebPage
from threadPool import ThreadPool
import threading  
import json
from tld import get_tld

log = logging.getLogger('Main.crawler')

mylock = threading.RLock() 

class Crawler(object):

    def __init__(self, args):
        #指定网页深度
        self.depth = args.depth  
        #标注初始爬虫深度，从1开始
        self.currentDepth = 1  
        #指定关键词,使用console的默认编码来解码
        self.keyword = args.keyword.decode(getdefaultlocale()[1]) 
        #数据库
        self.database =  Database(args.dbFile)
        #线程池,指定线程数
        self.threadPool = ThreadPool(args.threadNum)  
        #已访问的链接
        self.visitedHrefs = set()   
        #待访问的链接 
        self.unvisitedHrefs = deque()    
        #添加首个待访问的链接
        #self.unvisitedHrefs.append(args.url) 
        #标记爬虫是否开始执行任务
        self.isCrawling = False

        self.domainPattern = re.compile(r"^([0-9a-zA-Z][0-9a-zA-Z-]{0,62}\.)+([0-9a-zA-Z][0-9a-zA-Z-]{0,62})\.?$")
        self.maxDomainSeeds = args.maxDomainSeeds
        self._initDomainSeedsList(args.domainSeeds)

    def _initDomainSeedsList(self, domainSeedsFile):
        fp = open(domainSeedsFile, 'r+')
        urlList = fp.readlines()
        for url in urlList:
            formattedUrl = self._formatUrl(url)
            if len(formattedUrl) > 0 and len(self.unvisitedHrefs) <= self.maxDomainSeeds:
                self.unvisitedHrefs.append(formattedUrl)
        fp.close()
        print 'We have got %d domain feeds.'%len(self.unvisitedHrefs)

    def _formatUrl(self, rawValue):
        rawValueStr = rawValue.strip().strip('\n')
        if len(rawValueStr) <= 0:
            return '' 
        if not self.domainPattern.match(rawValueStr):
            return ''
        if not rawValueStr.startswith('http'):
            value = 'http://' + rawValueStr
        else:
            value = rawValueStr
        return value

    def start(self):
        print '\nStart Crawling\n'
        if not self._isDatabaseAvaliable():
            print 'Error: Unable to open database file.\n'
        else:
            self.isCrawling = True
            self.threadPool.startThreads() 
            while self.currentDepth < self.depth+1:
                #分配任务,线程池并发下载当前深度的所有页面（该操作不阻塞）
                self._assignCurrentDepthTasks ()
                #等待当前线程池完成所有任务,当池内的所有任务完成时，即代表爬完了一个网页深度
                #self.threadPool.taskJoin()可代替以下操作，可无法Ctrl-C Interupt
                while self.threadPool.getTaskLeft():
                    time.sleep(8)
                print 'Depth %d Finish. Totally visited %d links. \n' % (
                    self.currentDepth, len(self.visitedHrefs))
                log.info('Depth %d Finish. Total visited Links: %d\n' % (
                    self.currentDepth, len(self.visitedHrefs)))
                self.currentDepth += 1
            self.stop()

    def stop(self):
        self.isCrawling = False
        self.threadPool.stopThreads()
        self.database.close()

    def getAlreadyVisitedNum(self):
        #visitedHrefs保存已经分配给taskQueue的链接，有可能链接还在处理中。
        #因此真实的已访问链接数为visitedHrefs数减去待访问的链接数
        return len(self.visitedHrefs) - self.threadPool.getTaskLeft()

    def _assignCurrentDepthTasks(self):
        mylock.acquire()
        copiedUnvisitedHrefs = deque()
        while self.unvisitedHrefs:
            copiedUnvisitedHrefs.append(self.unvisitedHrefs.popleft())
        mylock.release()
        while copiedUnvisitedHrefs:
            url = copiedUnvisitedHrefs.popleft()
            #标注该链接已被访问,或即将被访问,防止重复访问相同链接
            self.visitedHrefs.add(url)
            #向任务队列分配任务
            self.threadPool.putTask(self._taskHandler, url)
 
    def _taskHandler(self, url):
        #先拿网页源码，再保存,两个都是高阻塞的操作，交给线程处理
        webPage = WebPage(url)
        retry =1
        if webPage.fetch(retry):
            print 'Visited URL : %s ' % url
            self._saveTaskResults(webPage)
            self._addUnvisitedHrefs(webPage)

    def _saveTaskResults(self, webPage):
        url, pageSource = webPage.getDatas()
        soup = BeautifulSoup(pageSource)
        image_tags = soup.find_all('img', src=True)
        log.error('pageSource %s' %pageSource)
        for image_tag in image_tags:
            log.error('image_tag %s' %image_tag.contents)
            image_tag_parent = image_tag.find_parent('a')
            if not image_tag_parent == None:
                targetURL = image_tag_parent.get('href').encode('utf8')
                if not targetURL.startswith('http'):
                    targetURL = urljoin(url, targetURL)#处理相对链接的问题
                adsURL = image_tag.get('src').encode('utf8') 
                if not adsURL.startswith('http'):
                    adsURL = urljoin(url, adsURL)#处理相对链接的问题
                print "We got an ads"
                print "adsURL %s" %adsURL
                print "targetURL %s" %targetURL
                print "referURL %s" %url
                print get_tld(adsURL)
                print get_tld(targetURL)
                print get_tld(url)
                log.error("adsURL %s" %adsURL)
                log.error("targetURL %s" %targetURL)
                log.error("referURL %s" %url)
            try:
                self.database.saveData(adsURL, targetURL, url)
            except Exception, e:
                 log.error(' URL: %s ' % url + traceback.format_exc())

    def _saveTaskResultsForSelfTest(self, url, pageSource):
        soup = BeautifulSoup(pageSource)
        image_tags = soup.find_all('img', src=True)
        for image_tag in image_tags:
            image_tag_parent = image_tag.find_parent('a')
            if not image_tag_parent == None:
                targetURL = image_tag_parent.get('href').encode('utf8')
                if not targetURL.startswith('http'):
                    targetURL = urljoin(url, targetURL)#处理相对链接的问题
                adsURL = image_tag.get('src').encode('utf8') 
                if not adsURL.startswith('http'):
                    adsURL = urljoin(url, adsURL)#处理相对链接的问题
                print "We got an ads"
                print "adsURL %s" %adsURL
                print "targetURL %s" %targetURL
                print "referURL %s" %url
                print get_tld(adsURL)
                print get_tld(targetURL)
                print get_tld(url)
            try:
                self.database.saveData(adsURL, targetURL, url)
            except Exception, e:
                 log.error(' URL: %s ' % url + traceback.format_exc())
    def _addUnvisitedHrefs(self, webPage):
        '''添加未访问的链接。将有效的url放进UnvisitedHrefs列表'''
        #对链接进行过滤:1.只获取http或https网页;2.保证每个链接只访问一次
        url, pageSource = webPage.getDatas()
        hrefs = self._getAllHrefsFromPage(url, pageSource)
        mylock.acquire()
        for href in hrefs:
            if self._isHttpOrHttpsProtocol(href):
                if not self._isHrefRepeated(href):
                    self.unvisitedHrefs.append(href)
        mylock.release()

    def _getAllHrefsFromPage(self, url, pageSource):
        '''解析html源码，获取页面所有链接。返回链接列表'''
        hrefs = []
        soup = BeautifulSoup(pageSource)
        results = soup.find_all('a',href=True)
        for a in results:
            #必须将链接encode为utf8, 因为中文文件链接如 http://aa.com/文件.pdf 
            #在bs4中不会被自动url编码，从而导致encodeException
            href = a.get('href').encode('utf8')
            if not href.startswith('http'):
                href = urljoin(url, href)#处理相对链接的问题
            hrefs.append(href)
        return hrefs

    def _isHttpOrHttpsProtocol(self, href):
        protocal = urlparse(href).scheme
        if protocal == 'http' or protocal == 'https':
            return True
        return False

    def _isHrefRepeated(self, href):
        if href in self.visitedHrefs or href in self.unvisitedHrefs:
            return True
        return False

    def _isDatabaseAvaliable(self):
        if self.database.isConn():
            return True
        return False

    def selfTesting(self, args):
        url = 'http://www.baidu.com/'
        print '\nVisiting www.baidu.com'
        #测试网络,能否顺利获取百度源码
        pageSource = WebPage(url).fetch()
        if pageSource == None:
            print 'Please check your network and make sure it\'s connected.\n'
        #数据库测试
        elif not self._isDatabaseAvaliable():
            print 'Please make sure you have the permission to save data: %s\n' % args.dbFile
        #保存数据
        else:
            self._saveTaskResultsForSelfTest(url, pageSource)
            print 'Create logfile and database Successfully.'
            print 'Already save Baidu.com, Please check the database record.'
            print 'Seems No Problem!\n'
