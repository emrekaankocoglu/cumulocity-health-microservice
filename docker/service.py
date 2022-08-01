import requests,json,base64
from datetime import datetime, date, time,timedelta
import os
import json

C8Y_BASEURL = os.getenv('C8Y_BASEURL')
C8Y_BOOTSTRAP_USER = os.getenv('C8Y_BOOTSTRAP_USER')
C8Y_BOOTSTRAP_TENANT = os.getenv('C8Y_BOOTSTRAP_TENANT')
C8Y_BOOTSTRAP_PASSWORD = os.getenv('C8Y_BOOTSTRAP_PASSWORD')
C8Y_USER = os.getenv('C8Y_USER')
C8Y_TENANT = os.getenv('C8Y_TENANT')
C8Y_PASSWORD = os.getenv('C8Y_PASSWORD')
url=C8Y_BASEURL
def generateCredentials(tenant,username,password):
    credentials=tenant+"/"+username+":"+password
    return "Basic " + base64.b64encode(credentials.encode()).decode()

def authenticateUser(authHeader,role):
    requestURL=url+"/user/currentUser"
    response=requests.request("GET", requestURL, headers=authHeader)
    if (response.status_code==200):
        roles=response.json()["effectiveRoles"]
        for x in roles:
            if (x["name"]==role):
                return True
        return False
    else:
        return False

headers={"Authorization":""}
headers["Authorization"]=generateCredentials(C8Y_TENANT,C8Y_USER,C8Y_PASSWORD)
longTime=30
shortTime=7
        
def getTime(timePeriod):
    range=[]
    timeNow=datetime.utcnow()
    range.append((timeNow+timedelta(days=1)).strftime('%Y-%m-%d'))
    range.append((timeNow-timedelta(days=timePeriod)).strftime('%Y-%m-%d'))
    return range

def getAlarmCount(period, severity, source, status=""):
    if (period=="LONG"):
        timePeriod=getTime(longTime)
        requestURL=url+"/alarm/alarms/count?dateFrom="+timePeriod[1]+"&dateTo="+timePeriod[0]
    elif (period=="SHORT"):
        timePeriod=getTime(shortTime)
        requestURL=url+"/alarm/alarms/count?dateFrom="+timePeriod[1]+"&dateTo="+timePeriod[0]
    if (status!=""):
        requestURL=requestURL+"&status="+status
    requestURL=requestURL+"&severity="+severity+"&source="+source
    response=requests.request("GET", requestURL,headers=headers)
    return int(response.text)

def deviceHealth(source):
    activeStatus=getAlarmCount("LONG","CRITICAL",source,"ACTIVE")
    longTermCount=getAlarmCount("LONG","MAJOR",source,"ACTIVE")
    shortTermCount=getAlarmCount("SHORT","MAJOR",source,"ACTIVE")
    if(activeStatus>0):
        status="INOPERATIVE"
    elif ((longTermCount/longTime)*(1.20)<(shortTermCount/shortTime)):
        status="POOR"
    elif ((longTermCount/longTime)*(1.10)<(shortTermCount/shortTime)):
        status="GOOD"
    else:
        status="EXCELLENT"
    return status

