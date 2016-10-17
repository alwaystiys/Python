import io 
import sys  
import urllib.request 
import urllib.parse 
import http.cookiejar 
import requests
import collections
import time
import json

from html.parser import HTMLParser
from html.entities import name2codepoint
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

contentStr = '''
Hey,Dear.We have checked and packed your parcel and Sent .
Tracking the parcel on this web in few days .(http://www.17track.net/zh-cn)
Hope you received it soon. 
**If you have any problem like shipping delay or product quality,please talk with Louise at first before open dispute or bad feedback. 
She will offer best solution for you.**
Thank you for order and have a nice day!!  
Best wishes
Louise
'''
trackNumberList = []
packageNumberList = []

# 保存跟踪号到列表
def splitStr(tempStr):
    tempList = tempStr.split("'")
    return tempList

def subStr(tempStr):
    strLen = len(tempStr)
    return tempStr[1:strLen-1]

def saveTrackNumberToList(trackNumber):
    trackNumberList.append(trackNumber)

def savePackageNumberToList(packageId):
    packageNumberList.append(packageId)

class MyHTMLParser(HTMLParser):

    # def writeToFile(self, data):
    #     f = open('html.txt', 'a+', encoding='utf-8', errors='ignore')
    #     f.write(data)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'onclick':
                    if "doTrack" in value:
                        tempList = splitStr(value)
                        saveTrackNumberToList(tempList[1])
                        savePackageNumberToList(subStr(tempList[2]))


mySession = requests.session()

# 登录
def login():
    data = {'account':'*******','password':'**********'}
    loginUrl = 'http://www.dianxiaomi.com/user/login.htm'
    res = mySession.post(loginUrl, data)
    if res.status_code == 200:
        print("登录成功，当前状态码%s" %(res.status_code))
        return True
    else:
        print("登录失败，当前状态码%s" %(res.status_code))
        return False

# 上传图片
def uploadImage(packageId):
    tempTime = int(time.time()*1000)
    dic = collections.OrderedDict()
    dic["imgFile"] = ('blank.jpg', open('blank.jpg', 'rb'), 'image/jpeg')
    dic["uploadCall"] = (None, 
        '''function (files,data){
            $('#loading').modal('hide');
            data = $.parseJSON(data);
            if(data != null){
                if(data.code == 0){
                    $("#imgPath").val(data.url);
                    var picStr = getPicStrSmt(data.url);
                    $.fn.message({type:"success",msg:"上传成功"});
                    $("#importPicName").append(picStr);
                }else{
                    $.fn.message({type:"error",msg:data.msg, existTime:1000*60});
                }
            }
        }''')
    dic["onSelectCall"] = (None, 
        '''function (){
            //判断只能插入一张图片
            var imgNum = $("#importPicName img.imgCss").length;
            if(imgNum >= 1){
                $.fn.message({type:"error",msg:"只可插入一张图片！"});
                return false;
            }else {
                return true;
            }
        } ''')
    dic["shopId"] = (None, '55463')
    dic["fileName"] = (None, 'blank.jpg')
    dic["lastModifiedDate"] = (None, str(tempTime))
    files = dic

    uploadUrl = 'http://www.dianxiaomi.com/smtMessage/toUploadPicFromNative.json'
    res = mySession.post(uploadUrl, files=files)
    print(res.status_code)
    print(res.json())
    jsonDict = res.json()
    codeStatus = jsonDict["code"]
    if codeStatus == 0:
        print("上传图片成功，当前图片路径%s" %(jsonDict["url"]))
        print(packageId, jsonDict["url"])
        sendMsg(packageId, jsonDict["url"])
    else:
        print("上传图片失败，只发送留言 %s" %(packageId))
        sendMsg(packageId, "")
    

# 发送留言以及图片
def sendMsg(packageId, imageUrl):
    print("sendMsg")
    sendMsgUrl = "http://www.dianxiaomi.com/replyMsg/reply.json"
    data = {'packageId':packageId, 'content':contentStr, 'imgPath':imageUrl}
    res = mySession.post(sendMsgUrl, data)
    if res.status_code == 200:
        print("send msg succ")
    else:
        print("send msg fail")



# 获取今日订单
def getOrderList():
    orderUrl = "http://www.dianxiaomi.com/package/list.htm?pageNo=1&pageSize=100&shopId=-1&state=shipped&platform=&isSearch=1&searchType=orderId&authId=-1&startTime=2016-10-16&endTime=2016-10-16&country=&orderField=shipped_time&isVoided=0&ruleId=-1&sysRule=&applyType=&applyStatus=&printJh=-1&printMd=-1&commitPlatform=&productStatus=&jhComment=-1&storageId=0"
    res = mySession.get(orderUrl)
    if res.status_code == 200:
        print("获取订单列表成功，当前状态码%s" %(res.status_code))
        # print(res.text)
        # print("Get orderlist succ!!")
        parser = MyHTMLParser()
        parser.feed(res.text)
        totalLen = len(trackNumberList)
        print("当前跟踪号个数：", totalLen)
        testlen = 1
        testTrackNumber = "RA167201302FI"
        testpackageNumber = "2267262063585630"

        for index in range(testlen):
            print('正在处理当前第%d个跟踪号%s，包裹号%s, 请稍后..........' %(index + 1, trackNumberList[index], packageNumberList[index]))
            # searchUrl = "http://www.dianxiaomi.com/package/searchPackage.htm?pageNo=0&pageSize=100&state=shipped&searchType=trackNumber&content=%s&isVoided=0" %(trackNumberList[index])
            testsearchUrl = "http://www.dianxiaomi.com/package/searchPackage.htm?pageNo=0&pageSize=100&state=shipped&searchType=trackNumber&content=%s&isVoided=0" %(testTrackNumber)
            res = mySession.get(testsearchUrl)
            if res.status_code == 200:  
                print('成功取得当前跟踪号订单')
                # uploadImage(packageNumberList[index])
                uploadImage(testpackageNumber)
            else:
                print('fucking!!!')

        return True
    else:
        print("获取订单列表失败，当前状态码%s" %(res.status_code))
        return False



def main():
    res = login()
    if res:
        getOrderList()

main()


















