from contextlib import nullcontext
import time
from clicknium import clicknium as cc, locator
from common import *
import threading

idList = []
idClickedList = []
idBlackList = []
isStop = False
targetUrl = 'https://everve.net/tasks/vkontakte-groups/'

def doAction(vkontakteTab):
    print('Start Do Join :', vkontakteTab.url)
    try:
        if vkontakteTab.is_existing(locator.everve.vkontakte.span_join_community):
            print('vkontakte.span_join_community: detected')
            vkontakteTab.find_element(locator.everve.vkontakte.span_join_community).click()
            print('vkontakte.span_join_community: clicked')
        else:
            if vkontakteTab.is_existing(locator.everve.vkontakte.span_follow):
                print('vkontakte.span_follow: detected')
                vkontakteTab.find_element(locator.everve.vkontakte.span_follow).click()
                print('vkontakte.span_follow: clicked')

            # if vkontakteTab.is_existing(locator.everve.vkontakte.span_message):
            #     print('Dectect joining ...')

    except Exception as e:
        print('+Error do follow vkontakte')
        print(e.__cause__)
        # newTab.close()
    finally:
        print('End Do Join :', vkontakteTab.url)
        vkontakteTab.close()

def newJoin(event, browser, idStr):

    global idClickedList, idBlackList

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

        row = id.find_element_by_xpath('.//ancestor::tr')

        btn = row.children[2].children[0]

        btn.click()
        print('\n+ Btn '+id.get_text()+' : clicked')

        event.wait(1)
        if newTab.is_existing(locator.everve.status_spinner_border_text_secondary):

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

def joinVkontakte():
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

    event = threading.Event()
    event.clear()
    for id in availbleList:
        thread = threading.Thread(target=newJoin, args=(event, initTab.browser, id),daemon=True)
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
            if not "everve.net/tasks/vkontakte-followers" in tab.url:
                doAction(tab)
        
        for idx, tab in enumerate(initTab.browser.tabs):
            if "everve.net/tasks/vkontakte-groups" in tab.url:
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

def initJoin():
    global idList, idBlackList
    while True:
        if(isStop):
            return
        joinVkontakte()

initJoin()