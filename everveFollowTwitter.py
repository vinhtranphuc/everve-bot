from contextlib import nullcontext
import time
import numpy as np
from clicknium import clicknium as cc, ui, locator
from common import *

idFollowTwitterBlackList = []
isRefreshFollowTwitter = False
isStopFollowTwitter = False
def initFollowTwitter():

    global isRefreshFollowTwitter, isStopFollowTwitter, idFollowTwitterBlackList
    isSkip = False
    everveTab = cc.chrome.open("https://everve.net/dashboard/")
    # everveTab.activate()
    everveTab.wait_appear(locator.everve.menu_open_perform_tasks)
    everveTab.find_element(locator.everve.menu_open_perform_tasks).click()
    everveTab.find_element(locator.everve.menu_twitter_followers).click()
    time.sleep(1)
    def followTwitter(i):
        print('-----START ACTION : %d----------'%i)
        global isRefreshFollowTwitter, isStopFollowTwitter, idFollowTwitterBlackList

        if(i == 1 or isRefreshFollowTwitter):
            isRefreshFollowTwitter = False
            everveTab.wait_appear(locator.everve.button_follow_profile_twitter)

        trContainer = everveTab.find_element_by_xpath('//tr[contains(@class, "table_row")][not(contains(@style, "none"))]')
        idFollowEl = trContainer.find_element(locator.everve.id_follow_twitter)
        idFollow = idFollowEl.get_text()
        btnFollow = trContainer.find_element(locator.everve.button_follow_profile_twitter)

        try:
            btnFollow.click()
            print('btnFollow cliked',idFollow)
        except Exception as e:
            print(e)
            everveTab.refresh()
            isRefreshFollowTwitter = True
            return
            # isStopFollowTwitter = True

        twitterTab = waitAppearTab(everveTab.browser, 'twitter.com', 5)
        if twitterTab is nullcontext:
            print('cannot find twitter tab')
            print('Follow %d : Failed'%i)
            if(not everveTab.is_existing(locator.everve.button_follow_profile_tiktok)):
                isStopFollowTwitter = True
                return
            # everveTab.refresh()
            # isRefreshFollowTwitter = True
            return

        time.sleep(2)
        isFollowing = False
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
                    isFollowing = True
                    twitterTab.refresh()
                else:
                    print('twitter.button_follow_main: not found')
                    print('twitter.button_following: not found')
                    print('skip this action...')

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
                if(isFollowing):
                    idFollowTwitterBlackList.append(idFollow)

        print('-----END ACTION : %d----------'%i)
        return

    # for i in range(1,10000):
    #     if(isStopFollowTwitter):
    #         break
    #     followTwitter(i)
        i = 0
    while True:
        i += 1
        if(isStopFollowTwitter):
            break
        followTwitter(i)
    return