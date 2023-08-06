from ... import Orchestrator
import jinja2
import os
from inspect import signature # For detect count of def args
from ..Web import Basic
import operator
import math
from pyOpenRPA.Tools import CrossOS

class ControlPanel():
    """
    Manage your control panel on the orchestrator

    Control panel has 3 events types:
    - onRefreshHTML - run every n (see settings) second to detect changes in HTML control panel.
    - onRefreshJSON - run every n (see settings) second to detect changes in JSON data container to client side.
    - onInitJS - run when client reload the Orchestrator web page

    .. code-block:: python

        # Usage example:
        lCPManager = Orchestrator.Managers.ControlPanel(inControlPanelNameStr="TestControlPanel",
            inRefreshHTMLJinja2TemplatePathStr="ControlPanel\\test.html", inJinja2TemplateRefreshBool = True)
        
        

    If you use Jinja2 you can use next data context:
    StorageRobotDict: Orchestrator.StorageRobotGet(inRobotNameStr=self.mRobotNameStr),
    ControlPanelInstance: self,
    OrchestratorModule:Orchestrator,
    RequestInstance: inRequest,
    UserInfoDict: Orchestrator.WebUserInfoGet(inRequest=inRequest),
    UserUACDict: Orchestrator.UACUserDictGet(inRequest=inRequest),
    UserUACCheckDef: inRequest.UACClientCheck,
    EnumerateDef: enumerate,
    OperatorModule: operator,
    MathModule: math

    You can modify jinja context by use the function:
    Jinja2DataUpdateDictSet 

    .. code-block:: html
    
        Hello my control panel!
        You can use any def from Orchestrator module here in Jinja2 HTML template:
        Example: OrchestratorModule.OSCMD(inCMDStr="notepad")
        {{MathModule.pi}}
        {% if UserInfoDict['UserNameUpperStr']=="ND" %}
        YES - IT IS ND
        {% endif %}

    """
    mControlPanelNameStr = None
    # Jinja2 consolidated
    mJinja2TemplateRefreshBool = None
    mJinja2DataUpdateDict = None

    # RefreshHTML block
    mRefreshHTMLJinja2TemplatePathStr = None
    mRefreshHTMLJinja2TemplateFileNameStr = None
    mRefreshHTMLJinja2Loader = None
    mRefreshHTMLJinja2Env = None
    mRefreshHTMLJinja2Template = None

    # InitJS block
    mInitJSJinja2TemplatePathStr = None
    mInitJSJinja2TemplateFileNameStr = None
    mInitJSJinja2Loader = None
    mInitJSJinja2Env = None
    mInitJSJinja2Template = None

    mBackwardCompatibilityHTMLDef = None
    mBackwardCompatibilityJSDef = None
    mBackwardCompatibilityJSONDef = None

    mRobotNameStr = None

    def __init__(self, inControlPanelNameStr, inRefreshHTMLJinja2TemplatePathStr = None, inJinja2TemplateRefreshBool = False, inRobotNameStr = None):
        """
        Constructor of the control panel manager

        :param inControlPanelNameStr:
        :param inJinja2TemplatePathStr:
        """
        # Connect self witch pyOpenRPA via ControlPanelNameStr
        if inControlPanelNameStr in Orchestrator.GSettingsGet()["ServerDict"]["ControlPanelDict"]:
            raise Exception(f"Ошибка: Ранее уже была инициализирована панель управления с идентификатором: {inControlPanelNameStr}. Устраните ошибку и перезапустите оркестратор")
        Orchestrator.GSettingsGet()["ServerDict"]["ControlPanelDict"][inControlPanelNameStr] = self
        self.mControlPanelNameStr = inControlPanelNameStr # Set the name of the control panel
        self.RefreshHTMLJinja2TemplatePathSet(inJinja2TemplatePathStr = inRefreshHTMLJinja2TemplatePathStr)
        self.mJinja2TemplateRefreshBool = inJinja2TemplateRefreshBool
        self.mRobotNameStr = inRobotNameStr # Set the robot name for robot it execute

    def Jinja2DataUpdateDictSet(self, inJinja2DataUpdateDict):
        """
        Set the data dict from the Jinja2 context (you can add some new params)

        :param inJinja2DataUpdateDict: dict, which will be appended to main data context
        :return: None
        """
        self.mJinja2DataUpdateDict = inJinja2DataUpdateDict

    def RefreshHTMLJinja2TemplatePathSet(self, inJinja2TemplatePathStr):
        """
        Create Jinja2 env and load the template html

        :param inJinja2TemplatePathStr:
        :return:
        """
        try:
            if inJinja2TemplatePathStr is not None:
                lSystemLoaderPathStr = "/".join(CrossOS.PathSplitList(inPathStr=inJinja2TemplatePathStr)[0:-1])
                lTemplateFileNameStr = CrossOS.PathSplitList(inPathStr=inJinja2TemplatePathStr)[-1]
                self.mRefreshHTMLJinja2TemplateFileNameStr = lTemplateFileNameStr
                self.mRefreshHTMLJinja2Loader = jinja2.FileSystemLoader(lSystemLoaderPathStr)
                self.mRefreshHTMLJinja2Env = jinja2.Environment(loader=self.mRefreshHTMLJinja2Loader, trim_blocks=True, autoescape=True)
                self.mRefreshHTMLJinja2Template = self.mRefreshHTMLJinja2Env.get_template(lTemplateFileNameStr)
        except Exception as e:
            Orchestrator.OrchestratorLoggerGet().exception(f"Ошибка при инициализации Jinja2 ({inJinja2TemplatePathStr}). Панель управления: {self.mControlPanelNameStr}")

    def RefreshHTMLJinja2StrGenerate(self, inDataDict):
        """
        Generate the HTML str from the Jinja2. Pass the context inDataDict
        :param inDataDict:
        :return:
        """
        if self.mJinja2TemplateRefreshBool == True:
            self.mRefreshHTMLJinja2Template = self.mRefreshHTMLJinja2Env.get_template(self.mRefreshHTMLJinja2TemplateFileNameStr)
        lHTMLStr = self.mRefreshHTMLJinja2Template.render(**inDataDict) # Render the template into str
        return lHTMLStr

    def InitJSJinja2TemplatePathSet(self, inJinja2TemplatePathStr):
        """
        Create Jinja2 env and load the template html

        :param inJinja2TemplatePathStr:
        :return:
        """
        try:
            if inJinja2TemplatePathStr is not None:
                lSystemLoaderPathStr = "/".join(CrossOS.PathSplitList(inPathStr=inJinja2TemplatePathStr)[0:-1])
                lTemplateFileNameStr = CrossOS.PathSplitList(inPathStr=inJinja2TemplatePathStr)[-1]
                self.mInitJSJinja2TemplateFileNameStr = lTemplateFileNameStr
                self.mInitJSJinja2Loader = jinja2.FileSystemLoader(lSystemLoaderPathStr)
                self.mInitJSJinja2Env = jinja2.Environment(loader=self.mInitJSJinja2Loader, trim_blocks=True, autoescape=True)
                self.mInitJSJinja2Template = self.mInitJSJinja2Env.get_template(lTemplateFileNameStr)
        except Exception as e:
            Orchestrator.OrchestratorLoggerGet().exception(f"Ошибка при инициализации Jinja2 ({inJinja2TemplatePathStr}). Панель управления: {self.mControlPanelNameStr}")

    def InitJSJinja2StrGenerate(self, inDataDict):
        """
        Generate the HTML str from the Jinja2. Pass the context inDataDict
        :param inDataDict:
        :return:
        """
        if self.mJinja2TemplateRefreshBool == True:
            self.mInitJSJinja2Template = self.mInitJSJinja2Env.get_template(self.mInitJSJinja2TemplateFileNameStr)
        lHTMLStr = self.mInitJSJinja2Template.render(**inDataDict) # Render the template into str
        return lHTMLStr

    def DataDictGenerate(self, inAuthTokenStr=None):
        """ Сформировать словарь для генерации шаблона

        :param inAuthTokenStr: Текстовый токен авторизации пользователя
        :return:
        """
        lData = {
            "StorageRobotDict": None,
            "ControlPanelInstance":self,
            "OrchestratorModule":Orchestrator,
            "UserInfoDict": Orchestrator.WebUserInfoGet(inAuthTokenStr=inAuthTokenStr),
            "UserUACDict": Orchestrator.WebUserUACHierarchyGet(inAuthTokenStr=inAuthTokenStr),
            "UserUACCheckDef": lambda inKeyList: Orchestrator.WebUserUACCheck(inAuthTokenStr=inAuthTokenStr,inKeyList=inKeyList),
            "EnumerateDef": enumerate,
            "OperatorModule": operator,
            "MathModule": math
        }
        # Get the robot storage by the robot name (if you set robot name when init)
        if self.mRobotNameStr is not None:
            lData["StorageRobotDict"] = Orchestrator.StorageRobotGet(inRobotNameStr=self.mRobotNameStr)
        # Checkj Jinja2DataUpdateDict
        if self.mJinja2DataUpdateDict is not None:
            lData.update(self.mJinja2DataUpdateDict)
        return lData

    def OnRefreshHTMLStr(self, inAuthTokenStr=None):
        """
        Event to generate HTML code of the control panel when refresh time is over.
        Support backward compatibility for previous versions.

        :param inAuthTokenStr: request handler (from http.server import BaseHTTPRequestHandler)
        :return:
        """
        lHTMLStr = None
        lL = Orchestrator.OrchestratorLoggerGet()
        if self.mBackwardCompatibilityHTMLDef is None:
            if self.mRefreshHTMLJinja2Template is not None or (self.mJinja2TemplateRefreshBool == True and self.mRefreshHTMLJinja2TemplateFileNameStr is not None):
                lDataDict = self.OnRefreshHTMLDataDict(inAuthTokenStr = inAuthTokenStr)
                # Jinja code
                lHTMLStr = self.RefreshHTMLJinja2StrGenerate(inDataDict=lDataDict)
        else:
            lHTMLStr = self.BackwardAdapterHTMLDef(inAuthTokenStr=inAuthTokenStr)
        # return the str
        return lHTMLStr

    def OnRefreshHTMLDataDict(self, inAuthTokenStr):
        """
        Event to prepare data context for the futher Jinja2 HTML generation. You can override this def if you want some thing more data

        :param inRequest: request handler (from http.server import BaseHTTPRequestHandler)
        :return: dict
        """
        return self.DataDictGenerate(inAuthTokenStr=inAuthTokenStr)

    def OnRefreshHTMLHashStr(self, inAuthTokenStr):
        """
        Generate the hash the result output HTML. You can override this function if you know how to optimize HTML rendering.
        TODO NEED TO MODIFY ServerSettings to work with Hash because of all defs are need do use Hash

        :param inRequest: request handler (from http.server import BaseHTTPRequestHandler)
        :return: None - default, hash function is not determined. Str - hash function is working on!
        """
        return None

    def OnRefreshJSONDict(self, inAuthTokenStr):
        """
        Event to transmit some data from server side to the client side in JSON format. Call when page refresh is initialized

        :param inRequest: request handler (from http.server import BaseHTTPRequestHandler)
        :return: Dict type
        """
        lResultDict = None
        if self.mBackwardCompatibilityJSONDef is None:
            pass
        else:
            lResultDict = self.BackwardAdapterJSONDef(inAuthTokenStr=inAuthTokenStr)
        return lResultDict

    def OnInitJSStr(self, inAuthTokenStr):
        """
        Event when orchestrator web page is init on the client side - you can transmit some java script code is str type to execute it once.

        :param inAuthTokenStr: request handler (from http.server import BaseHTTPRequestHandler)
        :return: ""
        """
        lJSStr = ""
        if self.mBackwardCompatibilityJSDef is None:
            if self.mInitJSJinja2Template is not None or (self.mJinja2TemplateRefreshBool == True and self.mInitJSJinja2TemplateFileNameStr is not None):
                lDataDict = self.OnInitJSDataDict(inAuthTokenStr = inAuthTokenStr)
                # Jinja code
                lJSStr = self.InitJSJinja2StrGenerate(inDataDict=lDataDict)
        else:
            lJSStr = self.BackwardAdapterJSDef(inAuthTokenStr=inAuthTokenStr)
        return lJSStr

    def OnInitJSDataDict(self, inAuthTokenStr):
        """
        Event to prepare data context for the futher Jinja2 JS init generation. You can override this def if you want some thing more data

        :param inRequest: request handler (from http.server import BaseHTTPRequestHandler)
        :return: dict
        """
        return self.DataDictGenerate(inAuthTokenStr=inAuthTokenStr)

    def BackwardAdapterHTMLDef(self,inAuthTokenStr):
        lGS = Orchestrator.GSettingsGet()
        lL = Orchestrator.OrchestratorLoggerGet()
        # HTMLRenderDef
        lItemHTMLRenderDef = self.mBackwardCompatibilityHTMLDef
        lResultStr = ""
        if lItemHTMLRenderDef is not None:  # Call def (inRequest, inGSettings) or def (inGSettings)
            lHTMLResult = None
            lDEFSignature = signature(lItemHTMLRenderDef)  # Get signature of the def
            lDEFARGLen = len(lDEFSignature.parameters.keys())  # get count of the def args
            try:
                if lDEFARGLen == 1:  # def (inGSettings)
                    lHTMLResult = lItemHTMLRenderDef(lGS)
                elif lDEFARGLen == 2:  # def (inRequest, inGSettings)
                    lHTMLResult = lItemHTMLRenderDef(inAuthTokenStr, lGS)
                elif lDEFARGLen == 0:  # def ()
                    lHTMLResult = lItemHTMLRenderDef()
                # RunFunction
                # Backward compatibility up to 1.2.0 - call HTML generator if result has no "HTMLStr"
                if type(lHTMLResult) is str:
                    lResultStr = lHTMLResult
                elif "HTMLStr" in lHTMLResult or "JSONDict" in lHTMLResult:
                    lResultStr = lHTMLResult["HTMLStr"]
                else:
                    # Call backward compatibility HTML generator
                    lResultStr = Basic.HTMLControlPanelBC(inCPDict=lHTMLResult)
            except Exception as e:
                if lL: lL.exception(f"Ошибка в функции генерации HTML контента (HTMLRenderDef). Идентификатор панели управления: {self.mControlPanelNameStr}")
        return lResultStr


    def BackwardAdapterJSONDef(self,inAuthTokenStr):
        lGS = Orchestrator.GSettingsGet()
        lL = Orchestrator.OrchestratorLoggerGet()
        # HTMLRenderDef
        lItemJSONGeneratorDef = self.mBackwardCompatibilityJSONDef
        lResultDict = {}
        if lItemJSONGeneratorDef is not None:  # Call def (inRequest, inGSettings) or def (inGSettings)
            lJSONResult = None
            lDEFSignature = signature(lItemJSONGeneratorDef)  # Get signature of the def
            lDEFARGLen = len(lDEFSignature.parameters.keys())  # get count of the def args
            try:
                if lDEFARGLen == 1:  # def (inGSettings)
                    lJSONResult = lItemJSONGeneratorDef(lGS)
                elif lDEFARGLen == 2:  # def (inRequest, inGSettings)
                    lJSONResult = lItemJSONGeneratorDef(inAuthTokenStr, lGS)
                elif lDEFARGLen == 0:  # def ()
                    lJSONResult = lItemJSONGeneratorDef()
                # RunFunction
                # Backward compatibility up to 1.2.0 - call HTML generator if result has no "HTMLStr"
                lType = type(lJSONResult)
                if lType is str or lJSONResult is None or lType is int or lType is list or lType is dict or lType is bool or lType is float:
                    lResultDict = lJSONResult
                else:
                    if lL: lL.warning(f"Функция генерации JSON сформировала некорректную структуру: {str(type(lJSONResult))}, идентификатор панели управления: {self.mControlPanelNameStr}")
            except Exception as e:
                if lL: lL.exception(
                    f"Ошибка при формирвоании JSON (JSONGeneratorDef). Идентификатор панели управления {self.mControlPanelNameStr}")
        return lResultDict

    def BackwardAdapterJSDef(self,inAuthTokenStr):
        lGS = Orchestrator.GSettingsGet()
        lL = Orchestrator.OrchestratorLoggerGet()
        # HTMLRenderDef
        lJSInitGeneratorDef = self.mBackwardCompatibilityJSDef
        lResultStr = ""
        if lJSInitGeneratorDef is not None:  # Call def (inRequest, inGSettings) or def (inGSettings)
            lJSResult = ""
            lDEFSignature = signature(lJSInitGeneratorDef)  # Get signature of the def
            lDEFARGLen = len(lDEFSignature.parameters.keys())  # get count of the def args
            try:
                if lDEFARGLen == 1:  # def (inGSettings)
                    lJSResult = lJSInitGeneratorDef(lGS)
                elif lDEFARGLen == 2:  # def (inRequest, inGSettings)
                    lJSResult = lJSInitGeneratorDef(inAuthTokenStr, lGS)
                elif lDEFARGLen == 0:  # def ()
                    lJSResult = lJSInitGeneratorDef()
                if type(lJSResult) is str:
                    lResultStr = lJSResult  # Add delimiter to some cases
                else:
                    if lL: lL.warning(f"Функция JSInitGenerator вернула неверный формат данных: {str(type(lJSResult))}, идентификатор панели управления {self.mControlPanelNameStr}")
            except Exception as e:
                if lL: lL.exception(
                    f"Ошибка в функции формирования кода JavaScript (JSInitGeneratorDef). Идентификатор панели управления {self.mControlPanelNameStr}")
        return lResultStr