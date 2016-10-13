import urllib.parse 
import http.cookiejar 

# POST http://www.dianxiaomi.com/user/login.htm HTTP/1.1
# Host: www.dianxiaomi.com
# Connection: keep-alive
# Content-Length: 32
# Cache-Control: max-age=0
# Origin: http://www.dianxiaomi.com
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36
# Content-Type: application/x-www-form-urlencoded
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Referer: http://www.dianxiaomi.com/index.htm?ts=1476340130
# Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.8

header = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cache-Control': 'max-age=0',
    'Host': 'www.dianxiaomi.com',
}

#post的内容 
values = { 
	'account':'Tommyace', 
	'password':'ace039' 
} 

# 构造请求头以及Cookie
def getOpener(head):
    # deal with the Cookies
    cookie = http.cookiejar.CookieJar()
    cookiePro = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookiePro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
 
 # 模拟请求登录页面
def simulateReqLogin(openner):
	loginUrl = "http://www.dianxiaomi.com/user/login.htm" 
	# openner = getOpener(header) 
	r = openner.open(loginUrl, urllib.parse.urlencode(values).encode()) 
	# print(r.read().decode('gbk')) 

# 模拟请求订单管理页
def reqOrderIndex(opener):
	orderUrl = "http://www.dianxiaomi.com/order/index.htm" 
	r = openner.open(orderUrl)

# 模拟请求某个时间段订单，缺省配置 时间段为 今天
def reqOrderListByTimes(openner, startTime, endTime):
    orderListUrl = "http://www.dianxiaomi.com/package/list.htm?pageNo=2&pageSize=100&shopId=-1&state=shipped&platform=&isSearch=1&searchType=orderId&authId=-1&startTime=2016-10-13&endTime=2016-10-13&country=&orderField=shipped_time&isVoided=0&ruleId=-1&sysRule=&applyType=&applyStatus=&printJh=-1&printMd=-1&commitPlatform=&productStatus=&jhComment=-1&storageId=0"
    r = openner.open(orderListUrl)
    # print(r.read().decode('gbk')) 
    htmlBytes = r.read()  
    data = htmlBytes.decode('utf-8', 'ignore')
    f = open('html.txt', 'w', encoding='utf-8', errors='ignore')
    f.write(data)
    f.close()


# 解析订单列表，




def justForTest(openner):
    # order lists
    testUrl = "http://www.dianxiaomi.com/package/index.htm?pageNo=1&pageSize=&shopId=-1&state=shipped&isVoided=0&isSearch=1&orderField=shipped_time&startTime=2016-10-06&endTime=2016-10-12"
    r = openner.open(testUrl) 

# 测试图片上传
# need : multipart request 
# test path : http://www.dianxiaomi.com/smtMessage/toUploadPicFromNative.json

# def uploadPicByMultipartRequest():


# -----------------------------------------------------------------------------
opener = getOpener(header)
simulateReqLogin(opener)
reqOrderListByTimes(opener, 1, 2)







