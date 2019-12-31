#-*- coding: utf-8 -*-
# Main 函数


from selenium.common.exceptions import StaleElementReferenceException, \
    WebDriverException,TimeoutException

import Browser

import json, time

# 采用utf-8编码
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main():

    dic = {
      "data":10001,"server":10006, "vitrual":10002,
      "basic":10005,"real": 10007,"tech":10003,"other":10010, "basic":10005,"private":10009,
      "video":10004,"card":10008
     }

    i = 4
    username = [
        "sjtudarkweb","sjtudarkweb1","sjtudarkweb2","sjtudarkweb3","sjtudarkweb4"
    ]
    
    password = "SJTUdark123"
    

    for (key, item) in dic.items():
        #如果失败可以重新访问 最多进行三次
        for it in range(3): 
            try:
                crawl = Browser.onionBrowser()  
                crawl.first_requests()
                crawl.login(username[i],password)
                crawl.getTable(item)
                break

            except TimeoutException:
                time.sleep(5)
                i = (i + 1) % len(username)
                del crawl
                continue
    
    crawl = Browser.onionBrowser()
    with open(crawl.table_file,"r") as f:
        lines = f.readlines()
        
    for it in range(3):
        try:
            crawl = Browser.onionBrowser()
            crawl.first_requests()
            crawl.login(username[i],password)
            
            num = 1
            for line in lines[num-1:]:
                raw_data = json.loads(line)

                #由于host不固定 需要变换host 
                href = raw_data['href']
                href = href[href.find("viewtopic.php"):]
                host = crawl.browser.current_url[:crawl.browser.current_url.find("onion/")+6]
                href = host + href

                detail_dict = crawl.getDetail(raw_data['Title'], href, num)
                with open(crawl.data_file,"a") as f:
                    json.dump(dict(detail_dict.items() + raw_data.items()) , f, ensure_ascii=False)
                    f.write("\n")
                    f.flush()
                    
                num = num + 1
                if num % 100 == 0:
                    print "have crawl %d"%num
        except TimeoutException:
            time.sleep(5)
            i = (i + 1) % len(username)
            del crawl
            continue
        
            
if __name__ == '__main__':
    main()