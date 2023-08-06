import json, os
import copy
from . import __Orchestrator__
from .Server import app,IdentifyAuthorize # FAST API SERVER
#ControlPanelDict
from pyOpenRPA.Tools import CrossOS
if CrossOS.IS_WINDOWS_BOOL: #CrossOS
    from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)

if CrossOS.IS_LINUX_BOOL: import pyscreeze

from http import cookies
import uuid # generate UUID4
import time # sleep functions
import datetime # datetime functions
import threading # Multi-threading
from .Web import Basic
from ..Tools import Usage
from . import BackwardCompatibility # Support old up to 1.2.0 defs
from . import Processor
from . import SettingsTemplate
from fastapi import FastAPI, Form, Request, HTTPException, Depends, Header, Response, Body
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import io
import subprocess
from starlette.responses import StreamingResponse
from typing import Union
from fastapi.responses import JSONResponse
import asyncio

# # # # # # # # # # # #
# v 1.2.0 Functionallity
# # # # # # # # # # # #
# Generate JS when page init
def HiddenJSInitGenerate(inAuthTokenStr):
    inGSettings = __Orchestrator__.GSettingsGet()
    dUAC = lambda inKeyList: __Orchestrator__.WebUserUACCheck(inAuthTokenStr=inAuthTokenStr, inKeyList=inKeyList)
    lUACCPTemplateKeyList=["pyOpenRPADict","CPKeyDict"]
    lL = inGSettings["Logger"] # Alias for logger
    lJSInitResultStr = ""
    lRenderFunctionsRobotDict = inGSettings["ServerDict"]["ControlPanelDict"]
    for lItemKeyStr in lRenderFunctionsRobotDict:
        lItemDict = lRenderFunctionsRobotDict[lItemKeyStr]
        lUACBool = dUAC(inKeyList=lUACCPTemplateKeyList+[lItemKeyStr]) # Check if render function is applicable User Access Rights (UAC)
        if lItemKeyStr=="VersionCheck": lUACBool=True # For backward compatibility for the old fron version which not reload page when new orch version is comming
        if lUACBool: # Run function if UAC is TRUE
            # JSONGeneratorDef
            lJSInitResultStr = lJSInitResultStr + ";" + lItemDict.OnInitJSStr(inAuthTokenStr=inAuthTokenStr)
    return lJSInitResultStr

# Generate CP HTML + JSON
# Return {"Key":{"",""}}
def HiddenCPDictGenerate(inAuthTokenStr):
    inGSettings = __Orchestrator__.GSettingsGet()
    dUAC = lambda inKeyList: __Orchestrator__.WebUserUACCheck(inAuthTokenStr=inAuthTokenStr, inKeyList=inKeyList)
    #dUAC = d_uac #inRequest.UACClientCheck # Alias.
    lUACCPTemplateKeyList=["pyOpenRPADict","CPKeyDict"]
    lL = inGSettings["Logger"] # Alias for logger
    # Create result JSON
    lCPDict = {}
    lRenderFunctionsRobotDict = inGSettings["ServerDict"]["ControlPanelDict"]
    for lItemKeyStr in lRenderFunctionsRobotDict:
        lItemDict = lRenderFunctionsRobotDict[lItemKeyStr]
        lUACBool = dUAC(inKeyList=lUACCPTemplateKeyList+[lItemKeyStr]) # Check if render function is applicable User Access Rights (UAC)
        if lItemKeyStr=="VersionCheck": lUACBool=True # For backward compatibility for the old fron version which not reload page when new orch version is comming
        if lUACBool: # Run function if UAC is TRUE
            lCPItemDict = {"HTMLStr": None, "JSONDict":None}
            try:
                # HTML Render
                lCPItemDict["HTMLStr"] = lItemDict.OnRefreshHTMLStr(inAuthTokenStr=inAuthTokenStr)
                # JSONGeneratorDef
                lCPItemDict["JSONDict"] = lItemDict.OnRefreshJSONDict(inAuthTokenStr=inAuthTokenStr)
            except Exception as e:
                lL.exception(f"EXCEPTION WHEN HTML/ JSON RENDER")
            # Insert CPItemDict in result CPDict
            lCPDict[lItemKeyStr]=lCPItemDict
    return lCPDict

# Return {"Key":{"",""}}
def HiddenRDPDictGenerate(inAuthTokenStr):
    inGSettings = __Orchestrator__.GSettingsGet()
    dUAC = lambda inKeyList: __Orchestrator__.WebUserUACCheck(inAuthTokenStr=inAuthTokenStr, inKeyList=inKeyList)
    lUACRDPTemplateKeyList=["pyOpenRPADict","RDPKeyDict"]
    lRDPDict = {"HandlebarsList":[]}
    # Iterate throught the RDP list
    for lRDPSessionKeyStrItem in inGSettings["RobotRDPActive"]["RDPList"]:
        # Check UAC
        if dUAC(inKeyList=lUACRDPTemplateKeyList+[lRDPSessionKeyStrItem]):
            lRDPConfiguration = inGSettings["RobotRDPActive"]["RDPList"][
                lRDPSessionKeyStrItem]  # Get the configuration dict
            lDataItemDict = {"SessionKeyStr": "", "SessionHexStr": "", "IsFullScreenBool": False,
                             "IsIgnoredBool": False}  # Template
            lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem  # Session key str
            lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"]  # Session Hex
            lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGSettings["RobotRDPActive"][
                "FullScreenRDPSessionKeyStr"] else False  # Check  the full screen for rdp window
            lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"]  # Is ignored
            lRDPDict[lDataItemDict["SessionKeyStr"]]=lDataItemDict
            lHandlebarsDataItemDict = copy.deepcopy(lDataItemDict)
            lHandlebarsDataItemDict["SessionKeyStr"]=lDataItemDict["SessionKeyStr"]
            lRDPDict["HandlebarsList"].append(lHandlebarsDataItemDict)
    return lRDPDict

# Return {"HostNameUpperStr;UserUpperStr":{"IsListenBool":True}, "HandlebarsList":[{"HostnameUpperStr":"","UserUpperStr":"","IsListenBool":True}]}
def HiddenAgentDictGenerate(inAuthTokenStr):
    inGSettings = __Orchestrator__.GSettingsGet()
    dUAC = lambda inKeyList: __Orchestrator__.WebUserUACCheck(inAuthTokenStr=inAuthTokenStr, inKeyList=inKeyList)
    lUACAgentTemplateKeyList=["pyOpenRPADict","AgentKeyDict"]
    lAgentDict = {"HandlebarsList":[]}
    # Iterate throught the RDP list
    for lAgentItemKeyStrItem in inGSettings["AgentDict"]:
        # Check UAC
        lKeyStr = f"{lAgentItemKeyStrItem[0]};{lAgentItemKeyStrItem[1]}" # turple ("HostNameUpperStr","UserUpperStr") > Str "HostNameUpperStr;UserUpperStr"
        if dUAC(inKeyList=lUACAgentTemplateKeyList+[lKeyStr]):
            lDataItemDict = inGSettings["AgentDict"][lAgentItemKeyStrItem]
            lDataItemAgentDict = copy.deepcopy(lDataItemDict)
            lDataItemAgentDict["ActivityList"] = []
            lAgentDict[lKeyStr]=lDataItemAgentDict
            lHandlebarsDataItemDict = copy.deepcopy(lDataItemDict)
            lHandlebarsDataItemDict["HostnameUpperStr"]=lAgentItemKeyStrItem[0]
            lHandlebarsDataItemDict["UserUpperStr"]=lAgentItemKeyStrItem[1]
            lHandlebarsDataItemDict["ActivityList"] = []
            lAgentDict["HandlebarsList"].append(lHandlebarsDataItemDict)
    return lAgentDict


#v1.2.0 Send data container to the client from the server
# /pyOpenRPA/ServerData return {"HashStr" , "ServerDataDict": {"CPKeyStr":{"HTMLStr":"", DataDict:{}}}}

# Client: mGlobal.pyOpenRPA.ServerDataHashStr
# Client: mGlobal.pyOpenRPA.ServerDataDict

@app.post("/orpa/client/server-data",response_class=JSONResponse, tags=["Client"])
#{"Method": "POST", "URL": "/orpa/client/server-data", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerData, "ResponseContentType": "application/json"},
async def pyOpenRPA_ServerData(inRequest: Request, inAuthTokenStr:str=Depends(IdentifyAuthorize)):
    inGSettings = __Orchestrator__.GSettingsGet()
    # Extract the hash value from request
    lValueStr = await inRequest.body()
    lValueStr= lValueStr.decode("utf8")
    # Generate ServerDataDict
    lFlagDoGenerateBool = True
    while lFlagDoGenerateBool:
        lServerDataDict = {
            "CPDict": HiddenCPDictGenerate(inAuthTokenStr=inAuthTokenStr),
            "RDPDict": HiddenRDPDictGenerate(inAuthTokenStr=inAuthTokenStr),
            "AgentDict": HiddenAgentDictGenerate(inAuthTokenStr=inAuthTokenStr),
            "UserDict": {"UACClientDict": __Orchestrator__.WebUserUACHierarchyGet(inAuthTokenStr=inAuthTokenStr), "CWDPathStr": os.getcwd(), "VersionStr": inGSettings["VersionStr"]},
        }
        # Create JSON
        lServerDataDictJSONStr = json.dumps(lServerDataDict)
        # Generate hash
        lServerDataHashStr = str(hash(lServerDataDictJSONStr))
        if lValueStr!=lServerDataHashStr and lServerDataHashStr!= "" and lServerDataHashStr!= None: # Case if Hash is not equal
            lFlagDoGenerateBool = False
        else: # Case Hashes are equal
            await asyncio.sleep(inGSettings["Client"]["Session"]["ControlPanelRefreshIntervalSecFloat"])
    # Return the result if Hash is changed
    lResult = {"HashStr": lServerDataHashStr, "ServerDataDict": lServerDataDict}
    return lResult

# GET
# /pyOpenRPA/ServerJSInit return JavaScript to init on page
@app.get("/orpa/client/server-js-init",response_class=PlainTextResponse, tags=["Client"])
def pyOpenRPA_ServerJSInit(inRequest: Request, inAuthTokenStr:str=Depends(IdentifyAuthorize)):
    lResultStr = HiddenJSInitGenerate(inAuthTokenStr=inAuthTokenStr)
    if lResultStr is None:
        lResultStr = ""
    # Write content as utf-8 data
    return lResultStr

#v1.2.0 Send data container to the client from the server
# /pyOpenRPA/ServerLog return {"HashStr" , "ServerLogList": ["row 1", "row 2"]}
# Client: mGlobal.pyOpenRPA.ServerLogListHashStr
# Client: mGlobal.pyOpenRPA.ServerLogList
@app.post("/orpa/client/server-log",response_class=JSONResponse, tags=["Client"])
async def pyOpenRPA_ServerLog(inRequest: Request, inAuthTokenStr:str=Depends(IdentifyAuthorize)):
    inGSDict = __Orchestrator__.GSettingsGet()
    # Extract the hash value from request
    lValueStr = await inRequest.body()
    lValueStr= lValueStr.decode("utf8")
    # Generate ServerDataDict
    lFlagDoGenerateBool = True
    while lFlagDoGenerateBool:
        lServerLogList = inGSDict["Client"]["DumpLogList"]
        # Get hash
        lServerLogListHashStr = inGSDict["Client"]["DumpLogListHashStr"]
        if lValueStr!=lServerLogListHashStr and lServerLogListHashStr!= "" and lServerLogListHashStr!= None: # Case if Hash is not equal Fix because None can be obtained without JSON decode
            lFlagDoGenerateBool = False
        else: # Case Hashes are equal
            await asyncio.sleep(inGSDict["Client"]["DumpLogListRefreshIntervalSecFloat"])
    # Return the result if Hash is changed
    lResult = {"HashStr": lServerLogListHashStr, "ServerLogList": lServerLogList}
    return lResult

# Get thread list /orpa/threads
@app.get(path="/orpa/client/screenshot-get",response_class=PlainTextResponse,tags=["Client"])
def pyOpenRPA_Screenshot():
    # Get Screenshot
    def SaveScreenshot(inFilePath):
        lScreenshot = getScreenAsImage()
        lScreenshot.save('screenshot.png', format='png')
    # Сохранить файл на диск
    if CrossOS.IS_WINDOWS_BOOL:
        SaveScreenshot("screenshot.png")
        lFileObject = open("screenshot.png", "rb")
        # Write content as utf-8 data
        lImage = lFileObject.read()
        # Закрыть файловый объект
        lFileObject.close()
    else: 
        result = subprocess.run(["scrot", "--file", "screenshot.png", "-o"])
        lFileObject = open("screenshot.png", "rb")
        # Write content as utf-8 data
        lImage = lFileObject.read()
        # Закрыть файловый объект
        lFileObject.close()
    return StreamingResponse(io.BytesIO(lImage), media_type="image/png")

# Add activity item or activity list to the processor queue
# Body is Activity item or Activity List
# body inauthtoken JSON
@app.post(path="/orpa/api/processor-queue-add",response_class=JSONResponse,tags=["API"])
def pyOpenRPA_Processor(inRequest:Request, inAuthTokenStr:str = Depends(IdentifyAuthorize), inBodyStr:str = Body("")):
    inGSettings = __Orchestrator__.GSettingsGet()
    lL = __Orchestrator__.OrchestratorLoggerGet()
    # Recieve the data
    lValueStr = inBodyStr
    # Превращение массива байт в объект
    lInput = json.loads(lValueStr)
    lResult=[]
    # If list - operator plus
    if type(lInput) is list:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inAuthTokenStr=inAuthTokenStr):
            lActivityTypeListStr = ""
            try:
                for lActivityItem in lInput:
                    lActivityTypeListStr += f"{lActivityItem['Def']}; "
            except Exception as e:
                lActivityTypeListStr = "Ошибка чтения типа активности"
            lHostStr = __Orchestrator__.WebRequestHostGet(inRequest=inRequest)
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inAuthTokenStr=inAuthTokenStr, inHostStr = lHostStr,inOperationCodeStr=lActivityTypeListStr, inMessageStr="pyOpenRPA_Processor")
            if lL: lL.info(lWebAuditMessageStr)
        # Separate into 2 lists - sync and async
        lSyncActvityList = []
        lAsyncActivityList = []
        for lActivityItem in lInput:
            lResult.append(__Orchestrator__.ProcessorActivityItemAppend(inActivityItemDict=lActivityItem))
            if lActivityItem.get("ThreadBool", False) == False:
                lSyncActvityList.append(lActivityItem)
            else:
                lAsyncActivityList.append(lActivityItem)
        # Sync: Append in list
        inGSettings["ProcessorDict"]["ActivityList"]+=lSyncActvityList
        # Async: go to run
        if len(lAsyncActivityList)>0:
            for lActivityItem in lAsyncActivityList:
                lActivityItemArgsDict = {"inGSettings":inGSettings,"inActivityList":[lActivityItem]}
                lThread = threading.Thread(target=Processor.ActivityListExecute, kwargs=lActivityItemArgsDict)
                lThread.start()
    else:
        lResult=__Orchestrator__.ProcessorActivityItemAppend(inActivityItemDict=lInput)
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inAuthTokenStr=inAuthTokenStr):
            lActivityTypeListStr = ""
            try:
                lActivityTypeListStr = lInput['Def']
            except Exception as e:
                lActivityTypeListStr = "Ошибка чтения типа активности"
            lHostStr = __Orchestrator__.WebRequestHostGet(inRequest=inRequest)
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inAuthTokenStr=inAuthTokenStr, inHostStr = lHostStr, inOperationCodeStr=lActivityTypeListStr, inMessageStr="pyOpenRPA_Processor")
            if lL: lL.info(lWebAuditMessageStr)
        if lInput.get("ThreadBool",False) == False:
            # Append in list
            inGSettings["ProcessorDict"]["ActivityList"].append(lInput)
        else:
            lActivityItemArgsDict = {"inGSettings": inGSettings, "inActivityList": [lInput]}
            lThread = threading.Thread(target=Processor.ActivityListExecute, kwargs=lActivityItemArgsDict)
            lThread.start()
    return lResult

# Execute activity list
@app.post(path="/orpa/api/activity-list-execute",response_class=JSONResponse,tags=["API"])
def pyOpenRPA_ActivityListExecute(inRequest:Request, inAuthTokenStr:str = Depends(IdentifyAuthorize), inBodyStr:str = Body("")):
    # Recieve the data
    inGSettings = __Orchestrator__.GSettingsGet()
    lL = __Orchestrator__.OrchestratorLoggerGet()
    lValueStr = inBodyStr
    # Превращение массива байт в объект
    lInput = json.loads(lValueStr)
    # If list - operator plus
    if type(lInput) is list:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inAuthTokenStr=inAuthTokenStr):
            lActivityTypeListStr = ""
            try:
                for lActivityItem in lInput:
                    lActivityTypeListStr += f"{lActivityItem['Def']}; "
            except Exception as e:
                lActivityTypeListStr = "Ошибка чтения типа активности"
            lHostStr = __Orchestrator__.WebRequestHostGet(inRequest=inRequest)
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inAuthTokenStr=inAuthTokenStr, inHostStr = lHostStr,inOperationCodeStr=lActivityTypeListStr, inMessageStr="pyOpenRPA_ActivityListExecute")
            if lL: lL.info(lWebAuditMessageStr)
        # Execution
        lResultList = Processor.ActivityListExecute(inGSettings = inGSettings, inActivityList = lInput)
        return lResultList
        #inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lResultList), "utf8")
    else:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inAuthTokenStr=inAuthTokenStr):
            lActivityTypeListStr = ""
            try:
                lActivityTypeListStr = lInput['Def']
            except Exception as e:
                lActivityTypeListStr = "Ошибка чтения типа активности"
            lHostStr = __Orchestrator__.WebRequestHostGet(inRequest=inRequest)
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inAuthTokenStr=inAuthTokenStr, inHostStr = lHostStr,
                                                                         inOperationCodeStr=lActivityTypeListStr,
                                                                         inMessageStr="pyOpenRPA_ActivityListExecute")
            if lL: lL.info(lWebAuditMessageStr)
        # Execution
        lResultList = Processor.ActivityListExecute(inGSettings = inGSettings, inActivityList = [lInput])
        return lResultList
        #inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lResultList[0]), "utf8")

# See docs in Agent (pyOpenRPA.Agent.O2A)
@app.post(path="/orpa/agent/o2a",response_class=JSONResponse,tags=["Agent"])
async def pyOpenRPA_Agent_O2A(inRequest:Request, inAuthTokenStr:str = Depends(IdentifyAuthorize), inBodyDict = Body({})):
    inGSettings = __Orchestrator__.GSettingsGet()
    lL = __Orchestrator__.OrchestratorLoggerGet()
    lConnectionLifetimeSecFloat = inGSettings["ServerDict"]["AgentConnectionLifetimeSecFloat"] # 300.0 # 5 min * 60 sec 300.0
    lActivityItemLifetimeLimitSecFloat = inGSettings["ServerDict"]["AgentActivityLifetimeSecFloat"]
    lAgentLoopSleepSecFloat = inGSettings["ServerDict"]["AgentLoopSleepSecFloat"]
    lTimeStartFloat = time.time()
    # Recieve the data
    #lValueStr = inBodyDict
    # Превращение массива байт в объект
    lInput = inBodyDict#json.loads(lValueStr)
    # Check if item is created
    lAgentDictItemKeyTurple = (lInput["HostNameUpperStr"],lInput["UserUpperStr"])
    if lAgentDictItemKeyTurple not in inGSettings["AgentDict"]:
        inGSettings["AgentDict"][lAgentDictItemKeyTurple] = SettingsTemplate.__AgentDictItemCreate__()
    lThisAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
    lThisAgentDict["IsListenBool"]=True # Set is online
    lThisAgentDict["ConnectionCountInt"] += 1  # increment connection count
    # Test solution
    lDoLoopBool = True
    try:
        while lDoLoopBool:
            # Check if lifetime is over
            if time.time() - lTimeStartFloat > lConnectionLifetimeSecFloat: # Lifetime is over
                lThisAgentDict["IsListenBool"] = False  # Set is offline
                lDoLoopBool = False
            else: # Lifetime is good - do alg
                lThisAgentDict["IsListenBool"] = True  # Set is online
                lQueueList = lThisAgentDict["ActivityList"]
                if len(lQueueList)>0:# Do some operations if has queue items
                    # check if delta datetime is < than ActivityLifeTimeSecFloat
                    lActivityItem = lThisAgentDict["ActivityList"][0]
                    lActivityLifetimeSecFloat = (datetime.datetime.now() - lActivityItem["CreatedByDatetime"]).total_seconds()
                    # Check case if limit is expired - remove item
                    if lActivityLifetimeSecFloat > lActivityItemLifetimeLimitSecFloat:
                        lActivityItem = lThisAgentDict["ActivityList"].pop(0)
                    else:
                        lReturnActivityItemList = []
                        lReturnActivityItemDict = None
                        # If lInput['ActivityLastGUIDStr'] is '' > return 0 element for send in Agent
                        if lInput['ActivityLastGUIDStr'] == "":
                            lReturnActivityItemList=lQueueList # 2022 02 21 - Maslov Return list - not one item
                        else:
                            # go from the end - search element with GUIDStr
                            lForTriggerGetNextItem = False
                            for lForActivityItemDict in lQueueList:
                                if lForTriggerGetNextItem == True:
                                    lReturnActivityItemDict = lForActivityItemDict
                                    lReturnActivityItemList.append(lReturnActivityItemDict) # 2022 02 21 - Maslov Return list - not one item
                                    #break
                                if lForActivityItemDict['GUIDStr'] == lInput['ActivityLastGUIDStr']: lForTriggerGetNextItem = True
                            # CASE if GUID is not detected - return 0 element
                            if (len(lQueueList)>0 and lForTriggerGetNextItem==False):
                                #lReturnActivityItemDict = lThisAgentDict["ActivityList"][0]
                                lReturnActivityItemList=lQueueList # 2022 02 21 - Maslov Return list - not one item
                        # Send QUEUE ITEM
                        if len(lReturnActivityItemList) > 0:
                            lReturnActivityItemList = copy.deepcopy(lReturnActivityItemList)
                            for lItemDict in lReturnActivityItemList:
                                if "CreatedByDatetime" in lItemDict:
                                    del lItemDict["CreatedByDatetime"]
                            # Log full version if bytes size is less than limit . else short
                            lBodyLenInt = len(lReturnActivityItemList)
                            lAgentLimitLogSizeBytesInt = inGSettings["ServerDict"]["AgentLimitLogSizeBytesInt"]
                            if lL: lL.debug(f"ActivityItem to Agent ({lInput['HostNameUpperStr']}, {lInput['UserUpperStr']}): Item count: {len(lReturnActivityItemList)}, bytes size: {lBodyLenInt}")                            
                            lThisAgentDict["ConnectionCountInt"] -= 1  # Connection go to be closed - decrement the connection count
                            return lReturnActivityItemList
                        else: # Nothing to send - sleep for the next iteration
                            await asyncio.sleep(lAgentLoopSleepSecFloat)
                else: # no queue item - sleep for the next iteration
                    await asyncio.sleep(lAgentLoopSleepSecFloat)
    except Exception as e:
        if lL: lL.exception("pyOpenRPA_Agent_O2A Exception!")
    lThisAgentDict["ConnectionCountInt"] -= 1  # Connection go to be closed - decrement the connection count

@app.get(path="/orpa/api/helper-def-list/{inTokenStr}",response_class=JSONResponse,tags=["API"])
def pyOpenRPA_Debugging_HelperDefList(inRequest:Request, inAuthTokenStr:str = Depends(IdentifyAuthorize), inBodyStr:str = Body("")):
    # Parse query
    lResultDict = {
        "success": True,
        "results": []
    }
    # Get the path
    lPathSplitList = inRequest.url.path.split('/')
    lQueryStr = None
    if "HelperDefList" != lPathSplitList[-1] and "" != lPathSplitList[-1]: lQueryStr = lPathSplitList[-1]
    if lQueryStr != "" and lQueryStr is not None:
        lDefList = __Orchestrator__.ActivityItemHelperDefList(inDefQueryStr=lQueryStr)
        for lDefStr in lDefList:
            lResultDict["results"].append({"name": lDefStr, "value": lDefStr, "text": lDefStr})
    return lResultDict

@app.get(path="/orpa/api/helper-def-autofill/{inTokenStr}",response_class=JSONResponse,tags=["API"])
def pyOpenRPA_Debugging_HelperDefAutofill(inRequest:Request, inAuthTokenStr:str = Depends(IdentifyAuthorize), inBodyStr:str = Body("")):
    # Parse query
    # Get the path
    lPathSplitList = inRequest.url.path.split('/')
    lQueryStr = None
    if "HelperDefAutofill" != lPathSplitList[-1] and "" != lPathSplitList[-1]: lQueryStr = lPathSplitList[-1]
    lResultDict = __Orchestrator__.ActivityItemHelperDefAutofill(inDef = lQueryStr)
    return lResultDict

# See docs in Agent (pyOpenRPA.Agent.A2O)
@app.post(path="/orpa/agent/a2o",response_class=JSONResponse,tags=["Agent"])
def pyOpenRPA_Agent_A2O(inRequest:Request, inAuthTokenStr:str = Depends(IdentifyAuthorize), inBodyDict = Body({})):
    inGSettings = __Orchestrator__.GSettingsGet()
    lL = __Orchestrator__.OrchestratorLoggerGet()
    # Recieve the data
    #lValueStr = inBodyStr
    # Превращение массива байт в объект
    lInput = inBodyDict#json.loads(lValueStr)
    lAgentDictItemKeyTurple = (lInput["HostNameUpperStr"], lInput["UserUpperStr"])
    if "LogList" in lInput:
        for lLogItemStr in lInput["LogList"]:
            inGSettings["Logger"].info(lLogItemStr)
    if "ActivityReturnDict" in lInput:
        for lActivityReturnItemKeyStr in lInput["ActivityReturnDict"]:
            lActivityReturnItemValue = lInput["ActivityReturnDict"][lActivityReturnItemKeyStr]
            # Create item in gSettings
            inGSettings["AgentActivityReturnDict"][lActivityReturnItemKeyStr]=SettingsTemplate.__AgentActivityReturnDictItemCreate__(inReturn=lActivityReturnItemValue)
            lLogStr = "x байт"
            try:
                if lActivityReturnItemValue is not None:
                    lLogStr = f"{len(lActivityReturnItemValue)} байт"
            except Exception as e:
                pass 
            if lL: lL.debug(f"СЕРВЕР: Функция pyOpenRPA_Agent_A2O:: Получена активность от агента! Идентификатор активности: {lActivityReturnItemKeyStr}; Длина переданной активности: {lLogStr}")
            # Delete the source activity item from AgentDict
            if lAgentDictItemKeyTurple in inGSettings["AgentDict"]:
                lAgentDictActivityListNew = []
                lAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
                for lActivityItem in lAgentDict["ActivityList"]:
                    if lActivityReturnItemKeyStr != lActivityItem.get("GUIDStr",None):
                        lAgentDictActivityListNew.append(lActivityItem)
                    else:
                        del lActivityItem
                        if lL: lL.debug(f"СЕРВЕР: Функция pyOpenRPA_Agent_A2O:: Активность была удалена из процессорной очереди. Идентификатор активности: {lActivityReturnItemKeyStr}")
                inGSettings["AgentDict"][lAgentDictItemKeyTurple]["ActivityList"] = lAgentDictActivityListNew

from pyOpenRPA.Utils.Render import Render
lFileStr = CrossOS.PathJoinList(CrossOS.PathSplitList(__file__)[:-2] + ["Resources","Web","orpa","orc.xhtml"])
gRender = Render(inTemplatePathStr=lFileStr,inTemplateRefreshBool=True)
from pyOpenRPA import __version__
def pyOpenRPA_Index():
    # Пример использования
    global gRender
    lStr = gRender.Generate(inDataDict={"title":"ОРКЕСТРАТОР PYOPENRPA", "subtitle":"ПАНЕЛЬ УПРАВЛЕНИЯ", "version":__version__})
    __Orchestrator__.WebRequestResponseSend(inResponeStr=lStr,inContentTypeStr="text/html")

def SettingsUpdate():
    import os
    import pyOpenRPA.Orchestrator
    gSettingsDict = __Orchestrator__.GSettingsGet()
    if CrossOS.IS_WINDOWS_BOOL: lOrchestratorFolder = "\\".join(pyOpenRPA.Orchestrator.__file__.split("\\")[:-1])
    if CrossOS.IS_LINUX_BOOL: lOrchestratorFolder = "/".join(pyOpenRPA.Orchestrator.__file__.split("/")[:-1])
    lURLList = \
    lURLList = \
        [ #List of available URLs with the orchestrator server
            #{
            #    "Method":"GET|POST",
            #    "URL": "/index", #URL of the request
            #    "MatchType": "", #"BeginWith|Contains|Equal|EqualCase",
            #    "ResponseFilePath": "", #Absolute or relative path
            #    "ResponseFolderPath": "", #Absolute or relative path
            #    "ResponseContentType": "", #HTTP Content-type
            #    "ResponseDefRequestGlobal": None #Function with str result
            #}
            #Orchestrator basic dependencies # Index page in server.py because of special settings
            {"Method":"GET", "URL": gSettingsDict["ServerDict"]["URLIndexStr"],"MatchType": "EqualNoParam", "ResponseDefRequestGlobal": pyOpenRPA_Index},
            {"Method":"GET", "URL": "/metadata.json", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, CrossOS.PathStr("..\\Resources\\Web\\orpa\\metadata.json")), "ResponseContentType": "application/json","UACBool":False,},
            #{"Method":"GET", "URL": "/Index.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.js"), "ResponseContentType": "text/javascript"},
            {"Method":"GET", "URL": "/orpa/resources/", "MatchType": "BeginWith", "ResponseFolderPath": os.path.join(lOrchestratorFolder, CrossOS.PathStr("..\\Resources")),"UACBool":False, "UseCacheBool": True},            
            {"Method":"GET", "URL": "/orpa/client/resources/", "MatchType": "BeginWith", "ResponseFolderPath": os.path.join(lOrchestratorFolder, "Web"),"UACBool":False, "UseCacheBool": True},            

            #{"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.css"), "ResponseContentType": "text/css", "UACBool":False, "UseCacheBool": True},
            #{"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.js"), "ResponseContentType": "application/javascript", "UACBool":False, "UseCacheBool": True},
            #{"Method":"GET", "URL": "/3rdParty/jQuery/jquery-3.1.1.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\jQuery\\jquery-3.1.1.min.js"), "ResponseContentType": "application/javascript", "UACBool":False, "UseCacheBool": True},
            #{"Method":"GET", "URL": "/3rdParty/Google/LatoItalic.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Google\\LatoItalic.css"), "ResponseContentType": "font/css", "UACBool":False, "UseCacheBool": True},
            #{"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/themes/default/assets/fonts/icons.woff2", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default\\assets\\fonts\\icons.woff2"), "ResponseContentType": "font/woff2", "UACBool":False, "UseCacheBool": True},
            #{"Method":"GET", "URL": "/themes/default/", "MatchType": "BeginWith", "ResponseFolderPath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default"),"UACBool":False, "UseCacheBool": True},            
            {"Method":"GET", "URL": "/favicon.ico", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, CrossOS.PathStr("..\\Resources\\Web\\orpa\\favicon.ico")), "ResponseContentType": "image/x-icon", "UACBool":False, "UseCacheBool": True},
            #{"Method":"GET", "URL": "/3rdParty/Handlebars/handlebars-v4.1.2.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Handlebars\\handlebars-v4.1.2.js"), "ResponseContentType": "application/javascript", "UACBool":False, "UseCacheBool": True},
            #{"Method": "GET", "URL": "/Monitor/ControlPanelDictGet", "MatchType": "Equal", "ResponseDefRequestGlobal": BackwardCompatibility.v1_2_0_Monitor_ControlPanelDictGet_SessionCheckInit, "ResponseContentType": "application/json"},
            #{"Method": "GET", "URL": "/GetScreenshot", "MatchType": "BeginWith", "ResponseDefRequestGlobal": pyOpenRPA_Screenshot, "ResponseContentType": "image/png"},
            #{"Method": "GET", "URL": "/pyOpenRPA_logo.png", "MatchType": "Equal", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\pyOpenRPA_logo.png"), "ResponseContentType": "image/png", "UACBool":False, "UseCacheBool": True},
            {"Method": "POST", "URL": "/orpa/client/user-role-hierarchy-get", "MatchType": "Equal","ResponseDefRequestGlobal": BackwardCompatibility.v1_2_0_UserRoleHierarchyGet, "ResponseContentType": "application/json"},
            # New way of the v.1.2.0 functionallity (all defs by the URL from /pyOpenRPA/...)
            #{"Method": "POST", "URL": "/orpa/client/server-data", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerData, "ResponseContentType": "application/json"},
            #{"Method": "GET", "URL": "/orpa/client/server-js-init", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerJSInit, "ResponseContentType": "application/javascript"},
            #{"Method": "POST", "URL": "/orpa/client/server-log", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerLog, "ResponseContentType": "application/json"},
            #{"Method": "GET", "URL": "/orpa/client/screenshot-get", "MatchType": "Equal", "ResponseDefRequestGlobal": pyOpenRPA_Screenshot, "ResponseContentType": "image/png"},
            # API
            #{"Method": "POST", "URL": "/orpa/api/processor-queue-add", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Processor, "ResponseContentType": "application/json"},
            #{"Method": "POST", "URL": "/orpa/api/activity-list-execute", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ActivityListExecute, "ResponseContentType": "application/json"},
            #{"Method": "GET", "URL": "/orpa/api/helper-def-list/", "MatchType": "BeginWith","ResponseDefRequestGlobal": pyOpenRPA_Debugging_HelperDefList, "ResponseContentType": "application/json"},
            #{"Method": "GET", "URL": "/orpa/api/helper-def-autofill/", "MatchType": "BeginWith","ResponseDefRequestGlobal": pyOpenRPA_Debugging_HelperDefAutofill, "ResponseContentType": "application/json"},
            # AGENT
            #{"Method": "POST", "URL": "/orpa/agent/o2a", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Agent_O2A, "ResponseContentType": "application/json"},
            #{"Method": "POST", "URL": "/orpa/agent/a2o", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Agent_A2O, "ResponseContentType": "application/json"}
    ]
    Usage.Process(inComponentStr="Orchestrator")
    gSettingsDict["ServerDict"]["URLList"]=gSettingsDict["ServerDict"]["URLList"]+lURLList
    return gSettingsDict
