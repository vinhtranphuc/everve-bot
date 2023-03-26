from contextlib import nullcontext
import time
from clicknium import clicknium as cc, ui, locator

btnFollowList = []
isRefresh = False
def initFollowTwitter():
    global btnFollowList, isRefresh
    everveTab = cc.chrome.open("https://everve.net/dashboard/")
    everveTab.wait_appear(locator.everve.menu_open_perform_tasks)
    everveTab.find_element(locator.everve.menu_open_perform_tasks).click()
    everveTab.find_element(locator.everve.menu_twitter_followers).click()

    def followTwitter(i):
        global btnFollowList, isRefresh

        # if i > 1:
        #     everveTab.refresh()

        # everveTab.wait_appear(locator.everve.button_follow_profile_twitter)
        if(i == 1 or isRefresh):
            isRefresh = False
            everveTab.wait_appear(locator.everve.button_follow_profile_twitter)
            btnFollowList = everveTab.find_elements(locator.everve.button_follow_profile_twitter)

        try:
            btnFollowList[0].click()
            btnFollowList.pop(0)
        except:
            print('cannot click button_follow_profile_twitter')
            everveTab.refresh()
            isRefresh = True
            return

        # if everveTab.is_existing(locator.everve.button_follow_profile_twitter):
        #     everveTab.find_element(locator.everve.button_follow_profile_twitter).click()
        #     print('button_follow_profile_twitter: clicked')
        # else:
        #     print('button_follow_profile_twitter: not found')
        #     return
        
        time.sleep(4)

        twitterTab = nullcontext
        for tab in everveTab.browser.tabs:
            if 'twitter.com' in tab.url:
                twitterTab = tab

        if twitterTab is nullcontext:
            print('cannot find twitter tab')
            print('Follow %d : Failed'%i)
            everveTab.refresh()
            isRefresh = True
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
                    return

        twitterTab.close()
        # everveTab.wait_appear(locator.everve.button_next)
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
                return
        
        # if everveTab.is_existing(locator.everve.alert_success_follow_twitter):
        #     print('Follow %d : Success'%i)
        #     # everveTab.find_element(locator.everve.button_next).click()
        # else:
        #     print('Follow %d : Failed'%i)
        #     # everveTab.find_element(locator.everve.button_next_error).click()
        return

    for i in range(1,2000):
        # if i > 1:
        #     everveTab.refresh()
        followTwitter(i)
initFollowTwitter()
