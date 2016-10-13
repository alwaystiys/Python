
# import io  
# import sys  
# import urllib.request

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
# url = "http://www.dianxiaomi.com/index.htm"
# webPage=urllib.request.urlopen(url)
# data = webPage.read()
# data = data.decode('utf8')

# f = open('html.txt', 'w')
# f.write(data)
# f.close()

# print(data)
# print(type(webPage))
# print(webPage.geturl())
# print(webPage.info())
# print(webPage.getcode())


# webheader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
# req = urllib.request.Request(url=weburl, headers=webheader)  
# webPage=urllib.request.urlopen(req)

import io  
import sys  
import urllib.request  

weburl = "http://www.dianxiaomi.com/"
webheader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
webheader2 = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.douban.com',
    'DNT': '1'
    }
req = urllib.request.Request(url=weburl, headers=webheader2)  
res=urllib.request.urlopen(req)  
htmlBytes=res.read()  
data = htmlBytes.decode('utf-8', 'ignore')
localprint = data.encode('gbk','ignore')
print(localprint)  
f = open('html.txt', 'w', encoding='utf-8', errors='ignore')
f.write(data)
f.close()