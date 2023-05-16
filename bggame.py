
from contextlib import nullcontext
import time
from clicknium import clicknium as cc, locator
from common import *
import threading

def doClickOut():
    wrapTile = tab.find_elements_by_xpath('//*[@id="game-HashDice"]//div[contains(@class, "game-control-panel")]//div[contains(@class, "ui-input small")]')
    wrapTile[1].children[1].click()

def getAmount():
    amount = 0
    headerEle = tab.find_elements_by_xpath('//div[contains(@class, "header-inner page-max-width-wrap")]')

    amountEles = headerEle[0].find_elements_by_xpath('//span[contains(@class, "amount-str")]')
    amountStr = amountEles[0].get_text()
    print('amount str :',amountStr)
    amount = amountStr.split('₫ ', 1)[1]
    amount= float(amount)
    return amount

def createSeat(exponent):

    amount = getAmount()

    result = amount/pow(2, exponent)
    print('createSeat :',result)

    # set seate
    seatInput = tab.find_elements_by_xpath('//*[@id="game-HashDice"]//div[contains(@class, "game-control-panel")]//div[contains(@class, "game-coininput")]//input[contains(@type, "text")]')
    print(seatInput[0].get_text())
    seatInput[0].set_text(result)
    seatInput[0].click()
    # seatInput[0].clear()
    # seatInput[0].send_keys(0.25)

    doClickOut()

    return result

def detectWin(currentAmount, waitSecond):
    for i in range(waitSecond):
        try:
           nextAmount = getAmount()
           if(nextAmount > currentAmount):
                return True
           if(nextAmount < currentAmount):
                return False
        except:
            print('Error')
        finally:
            time.sleep(1)

def doEarn(isWin): 
    print('Start doEarn :',isWin)
    if(isWin):
        createSeat(10)
    else:
        # set next seate
        seatInput = tab.find_elements_by_xpath('//*[@id="game-HashDice"]//div[contains(@class, "game-control-panel")]//div[contains(@class, "game-coininput")]//input[contains(@type, "text")]')
        print(seatInput[0].get_text())
        nextSeate = float(seatInput[0].get_text())*2
        seatInput[0].set_text(nextSeate)
        seatInput[0].click()
        doClickOut()

    seatBtn = tab.find_elements_by_xpath('//*[@id="game-HashDice"]//div[contains(@class, "game-control-panel")]//button[contains(@class, "bet-button")]')
    print(seatBtn[0].get_text())

    
    print('End doEarn :',isWin)

    #  do click
    seatBtn[0].click()
    # time.sleep(0.5)
    currentAmount = getAmount()

    checkWin = detectWin(currentAmount, 5)
    doEarn(checkWin)

hashDiceUrl = 'https://bcgame.top/vi/game/hash-dice'
tab = cc.chrome.open(hashDiceUrl)
time.sleep(1)
# set seate
wrapTile = tab.find_elements_by_xpath('//*[@id="game-HashDice"]//div[contains(@class, "game-control-panel")]//div[contains(@class, "ui-input small")]')
tileEle = wrapTile[1].children[1].children[0]
print(tileEle.get_text())
tileEle.set_text(2)
doClickOut()
# wrapTile[1].children[1].click()
doEarn(True)

