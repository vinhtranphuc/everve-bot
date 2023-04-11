from contextlib import nullcontext
import time
from clicknium import clicknium as cc, locator
from common import *
import threading

idList = []
idClikedList = []

# def createTab(browser, idStr):
#     newTab = browser.new_tab("https://everve.net/tasks/traffic-exchange/")
#     try:
#         id = newTab.find_element_by_xpath('//small[contains(@class, "tx-12 tx-color-03 mg-b-0")][text()="'+idStr+'"]')
#         print('+ Has found '+id.get_text())

#         # row = id.find_element_by_xpath('//parent::tr[contains(@class, "table_row")]')
#         row = id.find_element_by_xpath('.//ancestor::tr')

#         # btn = row.find_element(locator.everve.button_a_view_website)
#         # btn = row.find_element_by_xpath('//a[contains(@class, "btn btn-xs btn-light")][text()="View Website"]')
#         btn = row.children[2].children[0]

#         # btn.click()
#         idClikedList.append(id.get_text())
#         print('+ Btn '+id.get_text()+' : clicked')
#         time.sleep(2)
        
#         # print('test id'+btn.find_element_by_xpath('//parent::tr[contains(@class, "table_row")]').find_element_by_xpath('//small').get_text())
#         print('+ Test '+btn.parent.parent.children[0].children[0].children[0].children[1].children[1].get_text())

#         # hideIcon = id.find_element_by_xpath('//parent::tr[contains(@class, "table_row")]')
#         # hideIcon = hideIcon.find_element_by_xpath('//i[contains(@class, "far fa-eye-slash")]')
#     except Exception as e:
#         print('+Error:'+e)
#         newTab.close()

def newTrafficTab(event, browser, idStr):
    global idClikedList

    print('START TAB '+idStr)
    # if idStr in idClikedList:
    #     print('+ ID clicked '+idStr)
    #     print('----------------')
    #     return
    
    # createTab(browser, idStr)
    try:
        newTab = browser.new_tab("https://everve.net/tasks/traffic-exchange/", True, 40)
    except Exception as e:
        print('+Error open new tab:')
        print(e.__cause__)
        # newTab.close()
        return

    try:
        id = newTab.find_element_by_xpath('//small[contains(@class, "tx-12 tx-color-03 mg-b-0")][text()="'+idStr+'"]')
        print('+ Has found '+id.get_text())

        # row = id.find_element_by_xpath('//parent::tr[contains(@class, "table_row")]')
        row = id.find_element_by_xpath('.//ancestor::tr')

        # btn = row.find_element(locator.everve.button_a_view_website)
        # btn = row.find_element_by_xpath('//a[contains(@class, "btn btn-xs btn-light")][text()="View Website"]')
        btn = row.children[2].children[0]

        btn.click()
        print('\n+ Btn '+id.get_text()+' : clicked')

        event.wait(1)
        if newTab.is_existing(locator.everve.status_spinner_border_text_secondary):
            event.wait(32)
            print('\nexit wait')
            print('\nClosing thread')
            idClikedList.append(id.get_text())
            return True
        else:
            newTab.close()
            print('\nInvalid...')
            print('\nClosing thread')
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
        return

    print('----------------------')

def trafficExchange():
    idElList = []
    initTab = cc.chrome.open("https://everve.net/tasks/traffic-exchange/")
    idElList = initTab.find_elements_by_xpath('//tr[contains(@class, "table_row")][not(contains(@style, "none"))]//small')
    print('NUmber of ID found : ',len(idElList))
    if len(idElList) < 1:
        print('Not found any ID')
        return

    for i in range(0, len(idElList)):
       idList.append(idElList[i].get_text())
    event = threading.Event()
    for id in idList:
        # threading.stack_size(100000)
        thread = threading.Thread(target=newTrafficTab, args=(event, initTab.browser, id))
        # thread.
        thread.start()
        # thread.join()

    isFinish = False
    while not isFinish:
        aliveThreads = threading.enumerate()
        print('Alive threads: ',len(aliveThreads))
        time.sleep(1)
        if(len(aliveThreads) < 2):
            isFinish = True
            break

    if (isFinish):
        for idx, tab in enumerate(initTab.browser.tabs):
            if(idx == 0):
                continue
            if not "everve.net/tasks/traffic-exchange" in tab.url:
                print('Closing tab: ',tab.url)
                tab.close()
        
        for idx, tab in enumerate(initTab.browser.tabs):
            if "everve.net/tasks/traffic-exchange" in tab.url:
                print('Next click tab: ',tab.url)
                # tab.wait_appear(locator.everve.button_next,{"name":"test"},30)
                if tab.is_existing(locator.everve.button_next):
                    tab.find_element(locator.everve.button_next).click()
                else:
                    print('Not found locator.everve.button_next :', tab.url)
                print('Closing tab: ',tab.url)
                time.sleep(1)
                tab.close()

        trafficExchange()

def initTrafficExchange():
    global idList, idClikedList
    trafficExchange()

initTrafficExchange()