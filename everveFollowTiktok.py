from contextlib import nullcontext
import time
from clicknium import clicknium as cc, locator
from common import *

idFollowTiktokBlackList = []
isRefreshFollowTiktok = False
isStopFollowTiktok = False
def initFollowTiktok():

    global isRefreshFollowTiktok, isStopFollowTiktok, idFollowTiktokBlackList
    everveTab = cc.chrome.open("https://everve.net/tasks/tiktok-followers/")

    def followTiktok(i):
        print('-----START ACTION : %d----------'%i)
        global isRefreshFollowTiktok, isStopFollowTiktok, idFollowTiktokBlackList

        if(i == 1 or isRefreshFollowTiktok):
            isRefreshFollowTiktok = False
            everveTab.wait_appear(locator.everve.button_follow_profile_tiktok)
        else:
            time.sleep(1)

        try:
            trContainer = everveTab.find_element_by_xpath('//tr[contains(@class, "table_row")][not(contains(@style, "none"))]')
            trContainer.find_element(locator.everve.button_follow_profile_tiktok).click() #btnFollow
            print('btnFollow cliked')
        except Exception as e:
            print(e)
            if(not everveTab.is_existing(locator.everve.button_follow_profile_tiktok)):
                isStopFollowTiktok = True
                return
            everveTab.refresh()
            isRefreshFollowTiktok = True
            return
            # isStopFollowTiktok = True
        if everveTab.is_existing(locator.everve.button_next):
            everveTab.find_element(locator.everve.button_next).click()
            return
        else:
            tiktokTab = waitAppearTab(everveTab.browser, 'tiktok.com', 7)

        if tiktokTab is nullcontext:
            print('cannot find tiktok tab')
            print('Follow %d : Failed'%i)
            if everveTab.is_existing(locator.everve.button_next):
                everveTab.find_element(locator.everve.button_next).click()
            else:
                everveTab.refresh()
                isRefreshFollowTiktok = True
            return

        time.sleep(5)
        if everveTab.browser.tabs[1].is_existing(locator.everve.tiktok.button_follow_main):
            print('tiktok.button_follow_main: detected')
            tiktokTab.find_element(locator.everve.tiktok.button_follow_main).click()
            print('tiktok.button_follow_main: clicked')
            time.sleep(1)
        else:
            if tiktokTab.is_existing(locator.everve.tiktok.button_following):
                print('tiktok.button_following: detected')
                tiktokTab.refresh()
                time.sleep(1)
            else:
                if tiktokTab.is_existing(locator.everve.tiktok.not_found_user):
                    print('tiktok: not_found_user')
                    tiktokTab.refresh()
                else:
                    if tiktokTab.is_existing(locator.everve.tiktok.button_follow_main):
                        print('tiktok.button_follow_main: detected')
                        tiktokTab.find_element(locator.everve.tiktok.button_follow_main).click()
                        print('tiktok.button_follow_main: clicked')
                    print('twitter.button_follow_main: not found')
                    print('twitter.button_following: not found')
                    print('twitter.not_found_user: not found')
                    print('skip this action...')
        
        tiktokTab.close()
        everveTab.wait_disappear(locator.everve.status_spinner_border_text_secondary)
        if everveTab.is_existing(locator.everve.button_next):
            everveTab.find_element(locator.everve.button_next).click()
            print('button_next: clicked')
            print('Follow %d : Success'%i)
        else:
            if everveTab.is_existing(locator.everve.button_next_error):
                everveTab.find_element(locator.everve.button_next_error).click()
                print('button_next_error: clicked')
                print('Follow %d : Failed'%i)

        print('-----END ACTION : %d----------'%i)
        return

    i = 0
    while True:
        i += 1
        if(isStopFollowTiktok):
            break
        followTiktok(i)
    return

# initFollowTiktok()
