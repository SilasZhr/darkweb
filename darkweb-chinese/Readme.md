# 暗网中文交易市场爬虫

### 网址
http://deepmixaasic2p6vm6f4d4g52e4ve6t37ejtti4holhhkdsmq3jsf3id.onion
### 数据爬取时间
2019-08-26

### 环境搭建

1. 安装tor
	
    ```
    sudo yum install tor
    sudo service tor start
    ```
2. 安装privoxy

    ```
    $ sudo yum install privoxy
    $ sudo vi /etc/privoxy/config
    ```
    添加
    ```
    listen-address localhost:8118
    forward-socks5 / 127.0.0.1:9050 .
    ```
    之后输入
    ```
    $ sudo cd  /usr/share/
    $ sudo mkdir privoxy
    $ cd privoxy
    $ vi config
    ```
    添加
    
    ```
    listen-address localhost:8118
    forward-socks5 / 127.0.0.1:9050 .
    ```
    再在命令行启动privoxy：
    ```
    $ sudo service privoxy start
    ```
    > 如果配置失败可以在网上查找教程

3. （optional）国内用户可能需要安装SS 或 SSR , 境外服务器跳过  
    [参考教程](https://blog.whsir.com/post-2711.html)

4. 安装tor broswer   
    [官网](https://www.torproject.org/download/)

5. 安装selenium,geckodriver  
    [教程](https://blog.csdn.net/u014283248/article/details/80631072)

### 文件

```
#
|--Browser.py  用于被调用爬取数据
|
|--Crawl.py 主函数入口
|
|--data 数据储存文件夹
	|
	|--Table.json 储存列表数据（不含详情）
	|
	|--Total_detail_Final.json 储存所有数据（含详情）
|--Exception 异常文件
	|
	|--ExceptionPage.txt 储存失败页数，格式为num:page
	|
	|--Page%d.html 储存非图片类附件网页信息
```

### 总数据格式
```
{  
	"Status" : 爬取是否成功 1:成功 0：详情爬取失败 2：附件爬取失败,   
	"Tartget" : 发布人,    
	"Title" : 标题,    
	"Type" : 商品类型,  
	"Price" : 单价（单位是BTC）,   
	"Trend" : 关注度,     
	"PublishTime" : 发布时间,    
	"Detail" : 详情,    
	"Volume" : 本单成交量,  
	"Attach" : 附件链接或源,   
	"Attach-class" : 附件类型,    
	"href" : 详情页连接,    
	"ID" : 条目ID 由于会更新所以没有用处,  
	"TransactionStatus" : 交易状态,  
	"TransactionType" : 交易类型,  
	"Sold" : 售出数量,    
	"Remaining" : 商品剩余数量,  
	"Quantity" : 商品数量 Sold + Remaining (有的Sold 或 Remaining 是科学计数法表示 所以后半部分数据没有这个属性)  
}   
```