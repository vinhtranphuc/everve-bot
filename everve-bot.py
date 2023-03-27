from contextlib import nullcontext
import time
from clicknium import clicknium as cc, ui, locator

btnFollowList = []
isRefreshFollowTwitter = False
isStopFollowTwitter = False
def initFollowTwitter():

    global btnFollowList, isRefreshFollowTwitter, isStopFollowTwitter
    everveTab = cc.chrome.open("https://everve.net/dashboard/")
    everveTab.activate()
    everveTab.wait_appear(locator.everve.menu_open_perform_tasks)
    everveTab.find_element(locator.everve.menu_open_perform_tasks).click()
    everveTab.find_element(locator.everve.menu_twitter_followers).click()

    def followTwitter(i):
        global btnFollowList, isRefreshFollowTwitter, isStopFollowTwitter

        if(i == 1 or isRefreshFollowTwitter):
            if(isRefreshFollowTwitter):
                time.sleep(1)
            isRefreshFollowTwitter = False
            everveTab.wait_appear(locator.everve.button_follow_profile_twitter)
            btnFollowList = everveTab.find_elements(locator.everve.button_follow_profile_twitter)

        try:
            if(i > 1):
                time.sleep(2)
            btnFollowList[0].click()
            print('first btnFollow cliked')
        except:
            print('cannot click butotn_follow_profile_twitter')
            everveTab.refresh()
            isRefreshFollowTwitter = True
            # isStopFollowTwitter = True
            return

        twitterTab = waitAppearTab(everveTab.browser, 'twitter.com', 5)
        if twitterTab is nullcontext:
            print('cannot find twitter tab')
            print('Follow %d : Failed'%i)
            btnFollowList = everveTab.find_elements(locator.everve.button_follow_profile_twitter)
            # everveTab.refresh()
            # isRefreshFollowTwitter = True
            return

        time.sleep(2)
        if twitterTab.is_existing(locator.everve.twitter.button_follow_main):
            print('twitter.button_follow_main: detected')
            twitterTab.find_element(locator.everve.twitter.button_follow_main).click()
            print('twitter.button_follow_main: clicked')
        else:
            if twitterTab.is_existing(locator.everve.twitter.span_yes_view_profile):
                twitterTab.find_element(locator.everve.twitter.span_yes_view_profile).click()
                twitterTab.wait_appear(locator.everve.twitter.button_follow_main)
                twitterTab.find_element(locator.everve.twitter.button_follow_main).click()
            else:
                if twitterTab.is_existing(locator.everve.twitter.button_following):
                    print('twitter.button_following: detected')
                    twitterTab.refresh()
                else:
                    print('twitter.button_follow_main: not found')
                    print('twitter.button_following: not found')
                    print('skip this action...')
                    print('Follow %d : Failed'%i)

        twitterTab.close()
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

        # remove first btn
        btnFollowList.pop(0)
        return

    for i in range(1,10000):
        # if i > 1:
        #     everveTab.refresh()
        if(isStopFollowTwitter):
            break
        followTwitter(i)
    return

btnFollowTiktokList = []
isRefreshFollowTiktok = False
isStopFollowTiktok = False
def initFollowTiktok():

    global btnFollowTiktokList, isRefreshFollowTiktok, isStopFollowTiktok
    everveTab = cc.chrome.open("https://everve.net/dashboard/")
    everveTab.activate()
    everveTab.wait_appear(locator.everve.menu_open_perform_tasks)
    everveTab.find_element(locator.everve.menu_open_perform_tasks).click()
    everveTab.find_element(locator.everve.menu_tiktok_followers).click()

    def followTiktok(i):
        global btnFollowTiktokList, isRefreshFollowTiktok, isStopFollowTiktok

        if(i == 1 or isRefreshFollowTiktok):
            if(isRefreshFollowTwitter):
                time.sleep(1)
            isRefreshFollowTiktok = False
            everveTab.wait_appear(locator.everve.button_follow_profile_twitter)
            btnFollowTiktokList = everveTab.find_elements(locator.everve.button_follow_profile_twitter)

        try:
            if(i > 1):
                time.sleep(1)
            btnFollowTiktokList[0].click()
            print('first btnFollow cliked')
            time.sleep(3)
            # btnFollowTiktokList.pop(0)
        except:
            print('cannot click butotn_follow_profile_twitter')
            everveTab.refresh()
            isRefreshFollowTwitter = True
            # isStopFollowTiktok = True
            return

        tiktokTab = waitAppearTab(everveTab.browser, 'tiktok.com', 3)
        if tiktokTab is nullcontext:
            print('cannot find tiktok tab')
            print('Follow %d : Failed'%i)

            btnFollowTiktokList[1].click()
            print('first btnFollow cliked')
            tiktokTab = waitAppearTab(everveTab.browser, 'tiktok.com', 3)
            if tiktokTab is nullcontext:
                print('cannot find tiktok tab')
                print('Follow %d : Failed'%i)
                everveTab.refresh()
                isRefreshFollowTiktok = True
            return

        time.sleep(2)
        if tiktokTab.is_existing(locator.everve.tiktok.button_follow_main):
            print('tiktok.button_follow_main: detected')
            tiktokTab.find_element(locator.everve.tiktok.button_follow_main).click()
            print('tiktok.button_follow_main: clicked')
        else:
            if tiktokTab.is_existing(locator.everve.tiktok.button_following):
                print('tiktok.button_following: detected')
                tiktokTab.refresh()
            else:
                if tiktokTab.is_existing(locator.everve.tiktok.not_found_user):
                    print('tiktok: not_found_user')
                else:
                    print('tiktok.button_follow_main: not found')
                    print('tiktok.button_following: not found')
                    print('skip this action...')
                    print('Follow %d : Failed'%i)

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

        # remove first btn
        btnFollowTiktokList.pop(0)
        return

    for i in range(1,10000):
        # if i > 1:
        #     everveTab.refresh()
        if(isStopFollowTiktok):
            break
        followTiktok(i)
    return

def waitAppearTab(browser, hostUrl:str, waitSecond:int):
    try:
        for i in range(waitSecond):
            for tab in browser.tabs:
                if hostUrl in tab.url:
                    print('Detected tab: %s',hostUrl)
                    return tab
            time.sleep(1)
    except:
        print('Cannot find tab: %s',hostUrl)
    return nullcontext

def main():
    initFollowTwitter()
    print('FOLLOW_TWITTER: STOPPED')

main()
