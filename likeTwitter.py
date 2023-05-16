from contextlib import nullcontext
import time
from clicknium import clicknium as cc, locator
from common import *
import threading

idList = []
idClickedList = []
idBlackList = []
isStop = False
targetUrl = 'https://everve.net/tasks/twitter-likes/'

def doLike(twitterTab):
    print('Start Do like :', twitterTab.url)
    try:
        if twitterTab.is_existing(locator.everve.twitter.icon_like_main):
            print('twitter.icon_like_main: detected')
            twitterTab.find_element(locator.everve.twitter.icon_like_main).click()
            print('twitter.icon_like_main: clicked')
        else:
            if twitterTab.is_existing(locator.everve.twitter.icon_liked):
                print('twitter.icon_liked: detected')
                # twitterTab.refresh()
            else:
                print('twitter.icon_like_main: not found')
                print('twitter.icon_liked: not found')
                print('skip this action...')
    except Exception as e:
        print('+Error do like twitter')
        print(e.__cause__)
        # newTab.close()
    finally:
        print('End Do like :', twitterTab.url)
        twitterTab.close()

def newLikeTwitter(event, browser, idStr):

    global idClickedList, idBlackList

    # print('START TAB '+idStr)
    # if idStr in idBlackList:
    #     print('\n+ ID clicked '+idStr)
    #     print('\n----------------')
    #     event.clear()
    #     return
    
    # createTab(browser, idStr)
    try:
        newTab = browser.new_tab(targetUrl, True, 40)
    except Exception as e:
        print('+Error open new tab:')
        print(e.__cause__)
        # newTab.close()
        return

    try:
        id = newTab.find_element_by_xpath('//small[contains(@class, "tx-12 tx-color-03 mg-b-0")][text()="'+idStr+'"]')
        print('\n+ Has found '+id.get_text())

        # row = id.find_element_by_xpath('//parent::tr[contains(@class, "table_row")]')
        row = id.find_element_by_xpath('.//ancestor::tr')

        # btn = row.find_element(locator.everve.button_a_view_website)
        # btn = row.find_element_by_xpath('//a[contains(@class, "btn btn-xs btn-light")][text()="Follow Profile"]')
        btn = row.children[2].children[0]

        btn.click()
        print('\n+ Btn '+id.get_text()+' : clicked')

        event.wait(1)
        if newTab.is_existing(locator.everve.status_spinner_border_text_secondary):
            # event.wait(32)
            # print('\nexit wait')
            print('\nClosing thread')
            if(id.get_text() in idClickedList):
                if(id.get_text() not in idBlackList):
                    idBlackList.append(id.get_text())
            else:
                idClickedList.append(id.get_text())

            event.clear()
            return True
        else:
            newTab.close()
            print('\nInvalid...')
            print('\nClosing thread')
            event.clear()
            return False

        # print('test id'+btn.find_element_by_xpath('//parent::tr[contains(@class, "table_row")]').find_element_by_xpath('//small').get_text())
        # print('+ Test '+btn.parent.parent.children[0].children[0].children[0].children[1].children[1].get_text())

        # hideIcon = id.find_element_by_xpath('//parent::tr[contains(@class, "table_row")]')
        # hideIcon = hideIcon.find_element_by_xpath('//i[contains(@class, "far fa-eye-slash")]')
    except Exception as e:
        print('\n+Error')
        print(e)
        print('\nClosing thread')
        newTab.close()
        event.clear()
        return
    finally:
        print('----------------------')

def getIdList(tab):
    idList = []
    idElList = tab.find_elements_by_xpath('//tr[contains(@class, "table_row")][not(contains(@style, "none"))]//small')
    print('\nNUmber of ID found : ',len(idElList))
    for i in range(0, len(idElList)):
       idList.append(idElList[i].get_text())
    return idList

def likeTwitter():
    global isStop
    idElList = []
    idList = []
    initTab = cc.chrome.open(targetUrl)
    idList = getIdList(initTab)
        
    if(len(idList) < 1):
        print('\nNot found any ID')
        isStop = True
        return

    exceptList = []
    availbleList = idList
    if(len(idBlackList) > 0):
        availbleList = list(set(idList) - set(idBlackList))
        print('\nAvailble List :',len(availbleList))
        exceptList = list(set(idList) - set(availbleList))
        print('\Except List :',len(exceptList))

    # hide except list
    for id in exceptList:
        try:
            idEl = initTab.find_element_by_xpath('//small[contains(@class, "tx-12 tx-color-03 mg-b-0")][text()="'+id+'"]')
            print('\n+ Has found '+idEl.get_text())
            row = idEl.find_element_by_xpath('.//ancestor::tr')
            hideIcon = row.children[2].children[0].children[1]
            hideIcon.click()
        except:
            print('not found hideIcon :', id)

    time.sleep(1)
    # availbleList = list(set(idList) - set(exceptList))
    # availbleList = idList
    # if(len(exceptList) > 0):
    #     availbleList = getIdList(initTab)

    event = threading.Event()
    event.clear()
    for id in availbleList:
        thread = threading.Thread(target=newLikeTwitter, args=(event, initTab.browser, id),daemon=True)
        thread.start()
        # thread.join()

    isFinish = False
    while not isFinish:
        aliveThreads = threading.enumerate()
        print('\nAlive threads: ',len(aliveThreads))
        time.sleep(1)
        if(len(aliveThreads) < 2):
            isFinish = True
            break

    if (isFinish):
        for idx, tab in enumerate(initTab.browser.tabs):
            if(idx == 0):
                continue
            if not "everve.net/tasks/twitter-likes" in tab.url:
                doLike(tab)
        
        for idx, tab in enumerate(initTab.browser.tabs):
            if "everve.net/tasks/twitter-likes" in tab.url:
                print('\nNext click tab: ',tab.url)
                # tab.wait_appear(locator.everve.button_next,{"name":"test"},30)
                if tab.is_existing(locator.everve.button_next):
                    tab.find_element(locator.everve.button_next).click()
                else:
                    if tab.is_existing(locator.everve.status_spinner_border_text_secondary):
                        tab.wait_disappear(locator.everve.status_spinner_border_text_secondary)
                        tab.find_element(locator.everve.button_next).click()
                print('\nClosing tab: ',tab.url)
                tab.close()

        threading.Event().clear()
        threading.Event().set()
        return

def initLikeTwitter():
    global idList, idBlackList
    while True:
        if(isStop):
            return
        likeTwitter()

initLikeTwitter()