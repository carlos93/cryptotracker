import time
import requests

MAX_COINS = 3

def parseFloat(num):
    return "{0:.4f}".format(num)

def getPriceFromGDAX(coin):
    r = requests.get("https://api.gdax.com/products/"+coin+"/book?level=1", headers={"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"})
    #print(r.json())
    json = r.json()
    value = (float(json["bids"][0][0]) + float(json["asks"][0][0])) / 2.0
    return value

min = [99999999, 99999999, 99999999]
max = [0, 0, 0]
while True:
    isMin = False
    isMax = False
    minIdx = 0
    maxIdx = 0
    file = open("data.txt", "a")
    coins = [0, 0, 0]
    coins[0] = float(getPriceFromGDAX("BTC-EUR"))
    coins[1] = float(getPriceFromGDAX("ETH-EUR"))
    coins[2] = float(getPriceFromGDAX("LTC-EUR"))

    for i in range(MAX_COINS):
        if coins[i] < min[i]:
            min[i] = coins[i]
            isMin = True
            minIdx |= 1 << i
            
        if coins[i] > max[i]:
            max[i] = coins[i]
            isMax = True
            maxIdx |= 1 << i

    line = "BTC: " + parseFloat(coins[0]) + ", ETH: " + parseFloat(coins[1]) + ", LTC: " + parseFloat(coins[2])
    extra = ""
    print(line, end="")
    if isMax:
        extra += " MAX " + str(maxIdx)
    if isMin:
        extra += " MIN " + str(minIdx)
    print(extra)
    file.write(str(parseFloat(coins[0]) + " " + parseFloat(coins[1]) + " " + parseFloat(coins[2])) + "\n")
    file.close()
    time.sleep(5)


