#-*- coding:utf-8 -*-

__author__ = 'wujiajia'

import requests
import config
from selenium.webdriver import PhantomJS
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup

class InspectAddress(object):
    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
        self.driver = PhantomJS(executable_path=r'phantomjs-2.1.1-windows\bin\phantomjs.exe',desired_capabilities=dcap)

    def get_dev_cookie(self):
        logurl = 'https://www.bidinghuo.cn/api/backend/login.json'
        # jsondata_url = 'https://www.bidinghuo.cn/api/backend/platform/query.json'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        data = {
            u'username': config.developers_account[0],
            u'password': config.developers_account[1]
        }
        value = ''
        try:
            res = requests.post(logurl, data=data)
            if res.status_code==200:
                print '开发平台账户登录-成功'
                value = res.cookies['laravel_session']
            else:
                print '开发平台账户登录-失败'

        except:
            print '开发平台账户登录-失败'

        cookies = {u'domain': u'.bidinghuo.cn',
                   u'secure': False,
                   u'value': value,
                   u'expiry': None,
                   u'path': u'/',
                   u'httpOnly': True,
                   u'name': u'laravel_session'}
        return cookies

    def get_brand_cookie(self):
        logurl = 'https://pyf123.bidinghuo.cn/api/admin/login.json'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        data = {
            u'username': config.brand_user[0],
            u'password': config.brand_user[1]
        }
        value = ''
        try:
            res = requests.post(logurl, data=data)
            if res.status_code==200:
                print '品牌商账户登录-成功'
                value = res.cookies['laravel_session']
            else:
                print '品牌商账户登录-失败'
        except:
            print '品牌商账户登录-失败'
        cookies = {u'domain': u'.bidinghuo.cn',
                   u'secure': False,
                   u'value': value,
                   u'expiry': None,
                   u'path': u'/',
                   u'httpOnly': True,
                   u'name': u'laravel_session'}
        return cookies

    def developer_platform(self):
        '''访问品牌商管理开发平台'''
        url = config.developers_platform
        try:
            self.driver.add_cookie(self.get_dev_cookie())
            self.driver.get(url)
            self.driver.set_page_load_timeout(30)
        except:
            print '访问品牌商管理开发平台-异常'

        try:
            page = self.driver.page_source
            page_soup = BeautifulSoup(page)
            username = page_soup.find_all(class_='user-name')[0]
            assert username.string==config.developers_account[0]
            print '品牌商管理开发平台-访问正常'
        except:
            print '品牌商管理开发平台-访问异常'


    def brand_platform(self):
        '''访问品牌商后台'''
        url = config.brand_platform
        try:
            self.driver.add_cookie(self.get_brand_cookie())
            self.driver.get(url)
            self.driver.set_page_load_timeout(30)
            bdh_title = BeautifulSoup(self.driver.page_source).find_all(class_='ovh')[0].h2.string
            nsgj_title = BeautifulSoup(self.driver.page_source).find_all(class_='ovh')[1].h2.string
            assert bdh_title == u'必订火'
            assert nsgj_title == u'内审管家'
            print '访问品牌商后台-正常'
        except:
            print '访问品牌商后台-异常'
        try:
            page = self.driver.page_source
            nsgj_href = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[2]/div/div[2]/div/div[2]/a').get_attribute('href')
            bdh_href = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div/div[2]/a').get_attribute(
                'href')
            assert requests.get(bdh_href).status_code==200
            self.driver.get(bdh_href)
            self.driver.set_page_load_timeout(30)
            dhh_title = BeautifulSoup(self.driver.page_source).find_all(class_='meeting-name text-overflow')[0].string
            assert dhh_title==u'测试订货会'
            print '访问品牌商订货会-正常'
        except:
            print '访问品牌商订货会-异常'
        try:
            assert requests.get(bdh_href).status_code == 200
            self.driver.get(nsgj_href)
            self.driver.set_page_load_timeout(30)
            nsh_title = BeautifulSoup(self.driver.page_source).find_all(class_='meeting-name text-overflow')[0].string
            assert nsh_title==u'认同与人体'
            print '访问品牌商内审管家-正常'
        except:
            print '访问品牌商内审管家-异常'

if __name__=='__main__':
     inspadd = InspectAddress()
     inspadd.developer_platform()
     inspadd.brand_platform()
     inspadd.driver.close()
     inspadd.driver.quit()







