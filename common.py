from contextlib import nullcontext
import time
# import numpy as np

class btnId:
    def __init__(self, id, btn, hideIcon):
        self.id = id
        self.btn = btn
        self.hideIcon = hideIcon

def waitAppearTab(browser, hostUrl:str, waitSecond:int):
    try:
        print('start waitAppearTab')
        for i in range(waitSecond):
            print('waitAppearTab s:%d'%i)
            try:
                for tab in browser.tabs:
                    if hostUrl in tab.url:
                        print('Detected tab: %s',hostUrl)
                        print('end waitAppearTab')
                        return tab
            except:
                print('Error find tab')
            finally:
                time.sleep(1)
    except:
        print('Cannot find tab: %s',hostUrl)
    print('end waitAppearTab')
    return nullcontext

# def waitAppearTabThread(event, browser, hostUrl:str, waitSecond:int):
#     try:
#         print('start waitAppearTab')
#         for i in range(waitSecond):
#             print('waitAppearTab s:%d'%i)
#             try:
#                 for tab in browser.tabs:
#                     if hostUrl in tab.url:
#                         print('Detected tab: %s',hostUrl)
#                         print('end waitAppearTab')
#                         return tab
#             except:
#                 print('Error find tab')
#             finally:
#                 event.sleep(1)
#     except:
#         print('Cannot find tab: %s',hostUrl)
#     print('end waitAppearTab')
#     return nullcontext

def combineBtnIdList(idList, btnList):
    result = []
    for id in idList:
        index = idList.index(id)
        btn = btnList[index]
        result.append(btnId(id,btn))
    return result

def getIdList(spanIdList):
    result = []
    for idElement in spanIdList:
        result.append(idElement.get_text())
    return result

# def findChildEleInList(wrapList, childLocator):
#     result = []
#     for e in wrapList:
#         # result = result + e.find_elements(childLocator)
#         result = np.append(result, e.find_elements(childLocator))
#     return result

def createTargetBtnList(btnIdList, blackIdList):
    result = []
    for btnId in btnIdList:
        if btnId.id not in blackIdList:
            result.append(btnId)
    return result