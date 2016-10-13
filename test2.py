import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse
#解压函数
def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data
#构造文件头
def getOpener(head):
    #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。   
header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            "Referer":"http://www.dianxiaomi.com/index.htm",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'http://www.dianxiaomi.com',
        }
url = 'http://www.dianxiaomi.com/index.htm'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
data = ungzip(data)     # 解压
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
account = 'Tommyace'
password = 'ace039'
#构造Post数据，他也是从抓大的包里分析得出的。

postDict = {
            "account":account,
            "password":password
        }
#需要给Post数据编码  

postData = urllib.parse.urlencode(postDict).encode()
response = opener.open(url,postData)


# postData = urllib.parse.urlencode(postDict).encode('utf-8')
# op = opener.open(url, postData)
# htmlBytes = op.read()
# data = ungzip(htmlBytes)

# localprint = htmlBytes.decode('utf-8', 'ignore').encode('gbk','ignore')
# print(localprint)

# outdata = htmlBytes.decode('utf-8', 'ignore')
# f = open('html.txt', 'w', encoding='utf-8', errors='ignore')
# f.write(outdata)
# f.close()