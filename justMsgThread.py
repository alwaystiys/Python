# 脚本需要python 3.x 环境才能运行
# 当前所采用的Python版本为3.5
# 需要python库支持 xlrd
# 安装完Python后，在cmd执行如下命令：
# python -m pip install xlrd

import xlrd  
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

# 日志文件 文件名为当前系统时间戳 str(int(time.time()*1000)
logFile = open("justMsglog\\" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".txt", 'a', encoding='utf-8', errors='ignore')

# excel文件名
# 内容格式
# trackNum msg
# xxxxxxxx xxx 
# xxxxxxxx xxx
# xxxxxxxx xxx
trackFile = "trackFile.xls"

mySession = requests.session()

# 打印日志并保存到文件
def printAndWriteFile(msg, *list):
    print(msg, end=" ")
    logFile.write(str(msg))
    logFile.write(" ")
    for x in list:
        print(x, end=" ")
        logFile.write(str(x))
        logFile.write(" ")
    logFile.write("\n") 
    print("\n")


# file.xls
# id trackNum msg
def getTableFromFle(filename):
    wb = xlrd.open_workbook(filename) # 打开文件  
    sheetNames = wb.sheet_names() # 查看包含的工作表 
    table  = wb.sheet_by_name(sheetNames[0]) # 打开第一个表
    return table

# 登录
def login():
    printAndWriteFile('请求登录...')
    data = {'account':'*****','password':'*******'}
    loginUrl = 'http://www.dianxiaomi.com/user/login.htm'
    res = mySession.post(loginUrl, data)
    if res.status_code == 200:
        printAndWriteFile("登录成功，当前状态码：%s" %(res.status_code))
        return True
    else:
        printAndWriteFile("登录失败，当前状态码：%s" %(res.status_code))
        return False


# 处理字符串
def splitStr(tempStr):
    tempList = tempStr.split("'")
    return tempList

def subStr(tempStr):
    strLen = len(tempStr)
    return tempStr[1:strLen-1]

# 这里可以开线程
def getDetailByTrackNum(trackNum):
    detailUrl = "http://www.dianxiaomi.com/package/searchPackage.htm?pageNo=0&pageSize=100&state=shipped&searchType=trackNumber&content=%s&isVoided=0" %(trackNum)
    res = mySession.get(detailUrl)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        soup = BeautifulSoup(soup.prettify(), "html.parser")
        dataList = soup.find_all("td", class_="tableOrderId")
        count = len(dataList)
        for value in dataList:
            try:
                tempSibling = value.next_sibling.next_sibling.next_sibling.next_sibling
                tempValue = tempSibling.contents[3].contents[1].contents[1]['onclick']
                tempList = tempValue.split("'")
                tempStr = tempList[2]
                packageId = tempStr[1:len(tempStr) - 1]
                printAndWriteFile("获得追踪号 %s 对应包裹ID：%s" %(trackNum, packageId))
                return packageId
            except Exception as err:
                printAndWriteFile("异常捕获: ", err)
    else:
        printAndWriteFile("获取包裹ID失败，追踪号：", trackNum)


def sendMsg(trackNum, packageId, contentStr, imageUrl):
    printAndWriteFile("正在对追踪号 %s 发送消息..." %(trackNum))
    printAndWriteFile("消息内容：", contentStr)
    sendMsgUrl = "http://www.dianxiaomi.com/replyMsg/reply.json"
    data = {'packageId':packageId, 'content':contentStr, 'imgPath':imageUrl}
    res = mySession.post(sendMsgUrl, data)
    if res.status_code == 200:
        printAndWriteFile("成功发送消息！")
    else:
        printAndWriteFile("发送消息失败！")
    printAndWriteFile("------------------------------------\n")


def run(trackNum, msg, row):
    packageId = getDetailByTrackNum(trackNum)
    sendMsg(trackNum, packageId, msg, "")


def main():
    res = login()
    if res:
        # getDetailByTrackNum("RF302837585CN")
        table = getTableFromFle(trackFile)
        count = table.nrows - 1
        printAndWriteFile("总追踪号数：", count)
        for row in range(table.nrows):
            if row == 0: 
                pass
            else:
                trackNum = table.cell(row, 0).value
                msg = table.cell(row, 1).value
                
                # run(trackNum, msg, row)

                t = threading.Thread(target=run, args=(trackNum, msg, row))
                t.start()
                t.join()

        printAndWriteFile("=================end=======================")   
             
main()