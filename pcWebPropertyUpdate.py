# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:41:45 2018

@author: wwlh
"""

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
#男性使用率
    manP = 0
    #女性
    womenP = 0
    #年龄
    #18岁以下
    yunger18 = 0
    age19_24 = 0
    age25_30 = 0
    age31_35 = 0
    age36_40 = 0
    older_41 = 0
    
    for msg in msglist:
        #print("%s\t%.2f"%(msg['TypeName'], msg['Proportion'] ))
        if(msg['RootType'] == 3):
            continue
        
        #数据提取不完整
        typeId = msg['TypeID']
       
        if (typeId == 4):
            manP =  msg['Proportion']
        elif typeId == 5 :
            womenP = msg['Proportion']
        elif typeId == 6:
            yunger18 = msg['Proportion']
        elif typeId == 7:
            age19_24 = msg['Proportion']
        elif typeId == 8:
            age25_30 = msg['Proportion']
        elif typeId == 9:
            age31_35 = msg['Proportion']
        elif typeId == 10:
            age36_40 = msg['Proportion']
        elif typeId == 46:
            older_41 = msg['Proportion']

    result =str(manP) + "," +str(womenP) + ","+str(yunger18) +"," + str(age19_24)+"," + str(age25_30)\
    +"," + str(age31_35) + "," + str(age36_40) + "," + str(older_41)
    return  result   
         



#url = 'http://index.iresearch.com.cn/pcNew/GetAttrlist/?aid=6788&kid=123&tid=65&typeid=1'
#url = 'http://index.iresearch.com.cn/pcNew/GetAttrlist/?aid=8133&kid=38&tid=66&typeid=1'
#print(getProportion(url))



#获取applist 并且提取app名, 领域, 行业
#放回app排名,appid,appname, fclassName(领域),kclassName(行业),appType(app类型)
def saveAppList(fileName, msg):
    f_write = open(fileName, 'a+')
    f_write.writelines(msg)
    f_write.flush
    f_write.close
    
def getWeblist(url):
    req = requests.get(url)
    html = req.text
    jsonDate = json.loads(html)
    applist = jsonDate['List']
    webListFile = 'webList.csv'
    for app in applist:
        appRank = app['Rank']
        appId = app['Appid']
        kid = app['Kclassid']
        tid = app['TimeId']
        appName = app['AppName']
        fclassName = app['FclassName']
        kclassName = app['KclassName']
        appType = app['AppType']
        webdomain = app['Domain']
        print("%d, %d,%s,%s,%s,%d"%(appRank,appId, appName,fclassName,kclassName,appType))
        webinfoUrl = 'http://index.iresearch.com.cn/pcNew/GetAttrlist/?aid='+str(appId)+'&kid='+str(kid)+'&tid='+str(tid)+'&typeid=1'
        #print(webinfoUrl)
        #appinfoUrl = 'http://index.iresearch.com.cn/app/attrlist/?aid=' + str(appId) + '&tid=66&typeid='+str(appType)
        webdetail = getProportion(webinfoUrl)
        #排名, appid,app名,域名,领域,行业,类型(app/web),男性概率,女性概率,<19岁,18~24,25~30,31~35,36~40,>40
        webstr = str(appRank) + "," +str(appId) + "," + appName +"," +webdomain+ "," + fclassName + "," + kclassName + "," + str(appType)+"," + webdetail+"\n"
        saveAppList(webListFile,webstr)



#url = 'http://index.iresearch.com.cn/app/GetDataList/?classId=0&classLevel=0&timeId=66&orderBy=2&pageIndex=5&pageSize=undefined'
#getAPPlist(url)

#url = 'http://index.iresearch.com.cn/pcNew/GetDataList/?classId=0&classLevel=0&timeId=65&orderBy=2&pageIndex=93&pageSize=undefined'
#getWeblist(url)




if __name__ == '__main__':
    #target = 'http://index.iresearch.com.cn/app/detail?id=1&Tid=66'
    #一页20,100页 共 2000app
    maxCount = 120
    count = 1
    while count<maxCount:
        listurl = 'http://index.iresearch.com.cn/pcNew/GetDataList/?classId=0&classLevel=0&timeId=66&orderBy=2&pageIndex='+str(count)+'&pageSize=undefined'
        #listurl = 'http://index.iresearch.com.cn/app/GetDataList/?classId=0&classLevel=0&timeId=66&orderBy=2&pageIndex='+str(count)+'&pageSize=undefined'
        getWeblist(listurl)
        count = count + 1
