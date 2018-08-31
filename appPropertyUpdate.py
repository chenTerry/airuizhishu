# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 14:36:22 2018

@author: wwlh
"""
#导入函数库
from bs4 import BeautifulSoup
import requests
import json


def getProportion(url):
    req = requests.get(url)
    html = req.text
    jsondate = json.loads(html)
    msglist = jsondate['List']
    result = ''
    for msg in msglist:
        #print("%s\t%.2f"%(msg['TypeName'], msg['Proportion'] ))
        if(msg['RootType'] == 3):
            continue
        result += msg['TypeName'] + "," +str(msg['Proportion']) + ","
    return  result   
         


#url = "http://index.iresearch.com.cn/app/attrlist/?aid=1&tid=66&typeid=0"
#print(getProportion(url))



#获取applist 并且提取app名, 领域, 行业
#放回app排名,appid,appname, fclassName(领域),kclassName(行业),appType(app类型)
def saveAppList(fileName, msg):
    f_write = open(fileName, 'a+')
    f_write.writelines(msg)
    f_write.flush
    f_write.close
    
def getAPPlist(url):
    req = requests.get(url)
    html = req.text
    jsonDate = json.loads(html)
    applist = jsonDate['List']
    applistFile = 'applist'
    appinfoUrl = ''
    for app in applist:
        appRank = app['Rank']
        appId = app['Appid']
        appName = app['AppName']
        fclassName = app['FclassName']
        kclassName = app['KclassName']
        appType = app['AppType']
        print("%d, %d,%s,%s,%s,%d"%(appRank,appId, appName,fclassName,kclassName,appType))
        appinfoUrl = 'http://index.iresearch.com.cn/app/attrlist/?aid=' + str(appId) + '&tid=66&typeid='+str(appType)
        appdetail = getProportion(appinfoUrl)
        appstr = str(appRank) + "," +str(appId) + "," + appName + "," + fclassName + "," + kclassName + "," + str(appType)+"," + appdetail+"\n"
        saveAppList(applistFile,appstr)



#url = 'http://index.iresearch.com.cn/app/GetDataList/?classId=0&classLevel=0&timeId=66&orderBy=2&pageIndex=5&pageSize=undefined'
#getAPPlist(url)



if __name__ == '__main__':
    #target = 'http://index.iresearch.com.cn/app/detail?id=1&Tid=66'
    #一页20,100页 共 2000app
    maxCount = 101
    count = 1
    while count<maxCount:
        #listurl = 'http://index.iresearch.com.cn/app/detail?id='+str(count)+'&Tid=66'
        listurl = 'http://index.iresearch.com.cn/app/GetDataList/?classId=0&classLevel=0&timeId=66&orderBy=2&pageIndex='+str(count)+'&pageSize=undefined'
        getAPPlist(listurl)
        count = count + 1
