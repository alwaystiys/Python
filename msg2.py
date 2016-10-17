import io 
import sys  
import os
import urllib.request 
import urllib.parse 
import http.cookiejar 
import requests
import collections
import time
import json
import time, threading
from bs4 import BeautifulSoup

from html.parser import HTMLParser
from html.entities import name2codepoint
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

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

def justPrint():
    print("sfsfs")

def formatPrint():
    print("sfsfs")

# 根据追踪号获取图片名称
def getFileName(trackNumber):
    tempStr = trackNumber
    imageName = tempStr[-6:-2]
    print("检查当前图片文件是否存在", imageName)
    if os.path.exists(imageName + ".jpg"):
        return imageName + ".jpg"
    elif os.path.exists(imageName + ".png"):
        return imageName + ".png"
    else:
        return ""

mySession = requests.session()

# 登录
def login():
    print('request login')
    data = {'account':'Tommyace','password':'ace039'}
    loginUrl = 'http://www.dianxiaomi.com/user/login.htm'
    res = mySession.post(loginUrl, data)
    if res.status_code == 200:
        print("登录成功，当前状态码%s" %(res.status_code))
        return True
    else:
        print("登录失败，当前状态码%s" %(res.status_code))
        return False

# 上传图片
def uploadImage(packageId, imageFullName):
    tempTime = int(time.time()*1000)
    dic = collections.OrderedDict()
    dic["imgFile"] = (imageFullName, open(imageFullName, 'rb'), 'image/jpeg')
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
    dic["fileName"] = (None, imageFullName)
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
    sendMsgUrl = "http://www.dianxiaomi.com/replyMsg/reply.json"
    data = {'packageId':packageId, 'content':contentStr, 'imgPath':imageUrl}
    res = mySession.post(sendMsgUrl, data)
    if res.status_code == 200:
        print("成功发送消息！")
    else:
        print("发送消息失败！")



# 获取今日订单
def getOrderList():

    # pageNo表示当前第几页
    # pageSize表示当前页显示订单个数
    # startTime endTime 表示订单时间段，相同表示今天，格式必须相同
    # 参数暂时手动修改 =================================================================
    pageNo = "1"               
    pageSize = "100"           
    startTime = "2016-10-16"    
    endTime = "2016-10-17"       
    # 参数暂时手动修改 =================================================================

    orderUrl = "http://www.dianxiaomi.com/package/list.htm?pageNo=%s&pageSize=%s&shopId=-1&state=shipped&platform=&isSearch=1&searchType=orderId&authId=-1&startTime%s&endTime=%s&country=&orderField=shipped_time&isVoided=0&ruleId=-1&sysRule=&applyType=&applyStatus=&printJh=-1&printMd=-1&commitPlatform=&productStatus=&jhComment=-1&storageId=0" % (pageNo, pageSize, startTime, endTime)
    res = mySession.get(orderUrl)
    if res.status_code == 200:
        print("获取订单列表成功，当前状态码%s" %(res.status_code))
        soup = BeautifulSoup(res.text, "html.parser")
        soup = BeautifulSoup(soup.prettify(), "html.parser")
        dataList = soup.find_all("td", class_="tableOrderId")
        count = len(dataList)
        for value in dataList:
            try:
                if str.strip(value.contents[5].text) == "":  # 是否未发过留言
                    tempSibling = value.next_sibling.next_sibling.next_sibling.next_sibling
                    tempValue = tempSibling.contents[3].contents[1].contents[1]['onclick']
                    tempList = splitStr(tempValue)
                    saveTrackNumberToList(tempList[1])
                    savePackageNumberToList(subStr(tempList[2]))
                    print("追踪号%s未留言" %(tempList[1]))
                    # print(tempValue)
                # else:
                #     print("already send msg")
            except Exception as err:
                print("异常处理: ", err)

        totalLen = len(trackNumberList)
        print("\n当前跟踪号个数：", totalLen)
        for index in range(totalLen):
            print('\n正在处理当前第%d个跟踪号%s，包裹号%s, 请稍后..' %(index + 1, trackNumberList[index], packageNumberList[index]))
            imageFullName = getFileName(trackNumberList[index])
            if imageFullName != "":
                print("上传%s图片中" %(imageFullName))
                uploadImage(packageNumberList[index], imageFullName)
            else:
                # sendMsg(packageNumberList[index], "")
                print("%s跟踪号的图片不存在, 只发送消息" %(trackNumberList[index]))

        return True
    else:
        print("获取订单列表失败，当前状态码%s" %(res.status_code))
        return False

def main():
    res = login()
    if res:
        getOrderList()

main()
