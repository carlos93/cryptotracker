import time
import requests
import sys
import json

coinNames = ["BTC-EUR", "ETH-EUR", "LTC-EUR", "BCH-EUR"]

MAX_COINS = 4

def parseFloat(num):
    return "{0:.4f}".format(num)

def parsePct(num):
    return "{0:.3f}".format(((num-1)*100))

def getPriceFromGDAX(coin):
    r = requests.get("https://api.gdax.com/products/"+coin+"/book?level=1", headers={"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"})
    json = r.json()
    value = (float(json["bids"][0][0]) + float(json["asks"][0][0])) / 2.0
    return value

def getStatsFromGDAX(coin):
    r = requests.get("https://api.gdax.com/products/"+coin+"/stats", headers={"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"})
    json = r.json()
    return json

def fillCoins(coins):
    for i in range(MAX_COINS):
        coins.append(float(getPriceFromGDAX(coinNames[i])))

def fillStats(stats):
    for i in range(MAX_COINS):
        stats.append(getStatsFromGDAX(coinNames[i]))

def fillPcts(coins, stats, pct):
    for i in range(MAX_COINS):
        pct.append(coins[i] / float(stats[i]["open"]))

min = [99999999, 99999999, 99999999, 99999999]
max = [0, 0, 0, 0]
while True:
    try:
        isMin = False
        isMax = False
        minIdx = 0
        maxIdx = 0
        file = open("data.txt", "a")
        coins = []
        fillCoins(coins)

        stats = []
        fillStats(stats)

        pct = []
        fillPcts(coins, stats, pct)

        for i in range(MAX_COINS):
            if coins[i] < min[i]:
                min[i] = coins[i]
                isMin = True
                minIdx |= 1 << i
                
            if coins[i] > max[i]:
                max[i] = coins[i]
                isMax = True
                maxIdx |= 1 << i

        line = "BTC: " + parseFloat(coins[0]) + " (" + parsePct(pct[0])  + "%), ETH: " + parseFloat(coins[1]) + " (" + parsePct(pct[1])  + "%), LTC: " + parseFloat(coins[2]) + " (" + parsePct(pct[2])  + "%), BCH: " + parseFloat(coins[3]) + "(" + parsePct(pct[3])  + "%)"
        extra = ""
        print(line, end="")
        if isMax:
            extra += " MAX " + str(maxIdx)
        if isMin:
            extra += " MIN " + str(minIdx)
        print(extra)
        file.write(str(parseFloat(coins[0]) + " " + parseFloat(coins[1]) + " " + parseFloat(coins[2]) + " " + parseFloat(coins[3])) + "\n")
        file.close()
        time.sleep(5)
    except json.JSONDecodeError as error:
        file = open("logs.txt", "a")
        file.write("JSONDecodeError error: " + error.msg + "\n" + error.doc + " AT POS: " + error.pos + ":" + ":" + "\n")
        file.close()
    except:
        file = open("logs.txt", "a")
        file.write("Unexpected error: " + str(sys.exc_info()[0]) + "\n")
        file.close()
        raise


