#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import StaleElementReferenceException, \
    WebDriverException,TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.keys import Keys

import copy,time,json,random

# 采用utf-8编码
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class onionBrowser():
    
    
    def __init__(self):
        #在切换线路时会有四个实际URL，全部放在此即可
        self.url = [
            "http://deepmixaasic2p6vm6f4d4g52e4ve6t37ejtti4holhhkdsmq3jsf3id.onion",
            "http://deepmixjso4ero6h3psxskkb756offo3uznx4a44vuc5464mjkqwndyd.onion",

            ]



        self.table_file = "data/Table.json" #储存列表

        self.data_file = "data/Total_detail_Final.json" #储存所有数据

        fireFoxOptions = FirefoxOptions()
        #headless模式(必须添加)
        fireFoxOptions.add_argument("--headless")
        #确认浏览器源（必须是tor browser 中的火狐浏览器， 普通火狐浏览器会卡在登录界面）
        binary = FirefoxBinary("/home/student/tor-browser/Browser/firefox")
        #禁用js
        fireFoxOptions.set_preference("javascript.enabled", False)

        fireFoxOptions.set_preference('network.proxy.type', 1)
        ## 设置代理IP
        fireFoxOptions.set_preference('network.proxy.http', '127.0.0.1')
        ## 设置代理端口
        fireFoxOptions.set_preference('network.proxy.http_port', 8118)
        ## 设置https协议
        fireFoxOptions.set_preference('network.proxy.ssl', '127.0.0.1')
        fireFoxOptions.set_preference('network.proxy.ssl_port', 8118)
        #启动浏览器
        self.browser = webdriver.Firefox(firefox_options=fireFoxOptions,firefox_binary=binary)

    def __del__(self):
        #单窗口模式用quit()
        self.browser.quit()


    def first_requests(self):
        #第一次访问：进入登录界面
        
        self.browser.get(random.choice(self.url))
        WebDriverWait(self.browser, 30, 0.5).until(EC.title_is(u"暗网交易市场 - 用户控制面板 - 登录"))
        print "成功进入登录界面"
        


    def login(self,username,password):
        '''
        # Note: 
            进入登录界面后调用
            
        # Brief: 
            登录，进入主页
        '''
        
        self.browser.find_element_by_id('username').send_keys(username)# 要登录的用户名
        time.sleep(1)
        self.browser.find_element_by_id('password').send_keys(password)# 对应的密码
        time.sleep(1)
        self.browser.find_element_by_name("login").click()
        
        WebDriverWait(self.browser, 30, 0.5).until(EC.title_is(u"暗网交易市场 - 网站首页"))
        print "成功进入主页"
# '''
#     def getIndex(self, url, username, password):
#         self.first_requests(url)
#         for i in range(30):
#             if self.browser.title == '暗网交易市场 - 用户控制面板 - 登录':
#                 print "In login site"
#                 break
#             time.sleep(1)
#             if i == 29:
#                 raise BlockError("BeforeLogin")

#         self.login(username, password)

#         for i in range(30):
#             if self.browser.title == '暗网交易市场 - 网站首页':
#                 break
#             time.sleep(1)
#             if i == 29:
#                 raise BlockError("InLogin")
# '''
    def getTable(self,num):
        '''
        # Note: 
            进入主页后调用
            
        # Brief: 
            进入分类界面,并逐页爬取列表
        '''
        
        # 找到分类的定位并点击
        first_links = self.browser.find_elements_by_class_name('text_index_top')
        for link in first_links:
            try:
                href = link.get_attribute('href')
            except StaleElementReferenceException:
                continue
            if "user_area.php?q_ea_id=%d"%num in href:
                link.click()
                
       # 显式等待30s
        WebDriverWait(self.browser, 30, 0.5).until(EC.title_is(u"分类查看"))
       
       # '''         
       #          # wait 20s
       #          for i in range(30):
       #              if self.browser.title == '分类查看':
       #                  break
       #              time.sleep(1)
       #              if i == 29:
       #                  raise TimeoutException
       # '''
        
        #获取此分类下的最大页数
        pages = []
        list = self.browser.find_elements_by_class_name("page_b1")
        for l in list:
            pages.append(int(l.text))
        Page_max = max(pages)
        for page in range(0, Page_max+1):
            #进行爬取 如果该页爬取失败则记录
            if self.get_Table_By_Page(page) == -1:
                with open("Exception/ExceptionPage.txt","a") as f:
                    f.write(str({num:page})+"\n")
                

    def get_Table_By_Page(self, page):
        
        '''
        # Note: 
            进入分类界面后调用，必须按页序调用，否则找不到页数
            
        # Brief: 
            按照page页爬取列表
            
        # arg:
            page: 需要爬取的页数
        '''

        rows = self.browser.find_elements_by_class_name('m_area_a')[0]\
            .find_elements_by_tag_name('tr')
        
        #如果不是第一页的话，就跳转到那一页
        if page != 1:
            pagelist = rows[0].find_elements_by_tag_name('a')
            location = "pagey="+str(page)
            for p in pagelist:
                try:
                    href = p.get_attribute('href')
                except StaleElementReferenceException:
                    continue
                if href == None:
                    continue
                if location in href:
                    p.find_elements_by_tag_name('button')[0].click()

                    
                    #显式等待30s
                    for i in range(60):
                        #判定是否转到该页
                        if self.browser.find_elements_by_class_name("page_b2")[0].text == u'%d'%page:
                            break
                        time.sleep(0.5)
                        if i == 59:
                            return -1

                            
                    rows = self.browser.find_elements_by_class_name('m_area_a')[0]\
                        .find_elements_by_tag_name('tr')
                    break
                    

        #列表爬取
        for row in rows[2:]:
            line = {}
            try:
                j = row.find_elements_by_tag_name('td')
                if len(j) == 10:
                    line["ID"] = j[0].text
                    line["PublishTime"] = j[1].text
                    line["Type"] = j[2].text
                    line["Tartget"] = j[3].text
                    line["Title"] = j[4].text
                    line["Price"] = j[5].text
                    line["Trend"] = j[7].text
                    line["href"] = j[8].find_elements_by_tag_name("a")[0].get_attribute("href")
                    #储存
                    with open(self.table_file, "a") as f:
                        json.dump(line, f, ensure_ascii=False)
                        f.write("\n")
                        f.flush()
                        
            except StaleElementReferenceException:
                    continue

        return 1

    def getDetail(self, Title , href, num):
        
        '''
        # Note: 
            进入主页后调用
            
        # Brief: 
            根据href  进入详情页并爬取
            
        # Arg:
            Title: 需要爬取的商品名称
            href : 需要爬取的商品链接
            num : 需要爬取的数据在self.table_file中的位置， 以便出现异常进行处理
            
        '''
        
        content = {}
        
        self.browser.get(href)
        #显式等待30s 跳转失败返回 0
        try:
            WebDriverWait(self.browser, 30, 0.5).until(EC.title_contains(Title))
        except TimeoutException :
            content["Status"] = "0"
            return content

        head = self.browser.find_elements_by_class_name("v_table_1")[0]\
            .find_elements_by_tag_name('tr')

        content["TransactionType"] = head[4].find_elements_by_tag_name('td')[1].text
        content["TransactionStatus"] = head[6].find_elements_by_tag_name('td')[1].text
        content["Volume"] = head[6].find_elements_by_tag_name('td')[3].text
        content["Remaining"] = head[8].find_elements_by_tag_name('td')[3].text
        content["Sold"] = head[8].find_elements_by_tag_name('td')[1].text
        content["Detail"] = self.browser.find_elements_by_class_name('content')[0].text
        
        # 有的是按照科学计数法来的， 所以不能直接计算
        #content["Quantity"] = str(int(content["Sold"]) + int(content["Remaining"]))
        
        
        Source = []
        AttchClass = set()
        
        #查看是否有附件，如果异常就是没有
        try:
            self.browser.find_elements_by_class_name('file')[0]
        except IndexError:
            content["Attach"] = []
            content["Status"] = "1"
            content["Attach-class"] = list(AttchClass)
            return content

        try:
            for attach in self.browser.find_elements_by_class_name('file'):
                att = attach.find_elements_by_tag_name('dt')[0]
                
                #图片类附件(绝大部分)
                if att.get_attribute('class') == 'attach-image':
                    Source.append(att.find_elements_by_tag_name('img')[0].get_attribute("src"))
                    AttchClass.add("img")
                    continue
                
                # '''    
                #     #文件类附件 很少所以没有编写，以异常抛出
                #     elif :
                # '''    
                    
                else:
                    file = open("Exception/Page%d.html"%num,"w")
                    file.write(self.browser.page_source)
                    file.close()
                    
                    content["Status"] = "2"
                    content["Attach"] = Source
                    content["Attach-Class"] = list(AttchClass)
                    
                    return content

        #出现了其他异常
        except Exception:
            file = open("Exception/Page%d.html"%num,"w")
            file.write(self.browser.page_source)
            file.close()
            content["Attach"] = Source
            content["Status"] = "2"
            content["Attach-Class"] = list(AttchClass)
            return content

        content["Status"] = "1"
        content["Attach"] = Source
        content["Attach-Class"] = list(AttchClass)
        return content



if __name__ == '__main__':
     # dic = { 
     #  "data":10001,"server":10006, "vitrual":10002,
     #  "basic":10005,"real": 10007,"tech":10003,"other":10010, "basic":10005,"private":10009,
     #   "video":10004,"card":10008
     # }

#     for (key, item) in dic.items():
#         test = onionBrowser()
#         test.getIndex("http://deepmixaasic2p6vm6f4d4g52e4ve6t37ejtti4holhhkdsmq3jsf3id.onion",
# "sjtudarkweb4", "SJTUdark123")
#         f = open("data/%s.json"%key, 'a')
#         test.spider(f, item)
#         print key+"finish"
#         del test
#         f.close()
#     print "Finish"

    f2 = open("data/Total_detail4.json","a")

    with open("data/Total_detail3.json","r") as f:
        lines = f.readlines()

    test = onionBrowser()
    test.getIndex("http://deepmixaasic2p6vm6f4d4g52e4ve6t37ejtti4holhhkdsmq3jsf3id.onion",
"sjtudarkweb", "SJTUdark123")
    i = 1
    # random.shuffle(lines)
    for line in lines:
        if json.loads(line)['Status'] == "0" : 
            tmp = json.loads(line)
            del tmp['Status']
            href = json.loads(line)['href']
            href = href[href.find("viewtopic.php"):]
            host = test.browser.current_url[:test.browser.current_url.find("onion/")+6]
            href = host + href
            # print href
            # test.func(href,json.loads(line)['Title'],i)
            # if i == 5:
            #     break

            detail_dict = test.getDetail(json.loads(line)['Title'], href, i)
            json.dump(dict(detail_dict.items() + tmp.items()) , f2, ensure_ascii=False)
            f2.write("\n")
            f2.flush()
            
        else:
            json.dump(dict(json.loads(line).items()), f2, ensure_ascii=False)
            f2.write("\n")
            f2.flush()
        i = i + 1
        if i % 100 == 0:
            print "have scrapy %d"%i
