import time
import requests

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
    btc = float(getPriceFromGDAX("BTC-EUR"))
    eth = float(getPriceFromGDAX("ETH-EUR"))
    ltc = float(getPriceFromGDAX("LTC-EUR"))

    if btc < min[0]:
        min[0] = btc
        isMin = True
        minIdx |= 1
        
    if eth < min[1]:
        min[1] = eth
        isMin = True
        minIdx |= 2
        
    if ltc < min[2]:
        min[2] = ltc
        isMin = True
        minIdx |= 4

    if btc > max[0]:
        max[0] = btc
        isMax = True
        maxIdx |= 1
        
    if eth > max[1]:
        max[1] = eth
        isMax = True
        maxIdx |= 2
        
    if ltc > max[2]:
        max[2] = ltc
        isMax = True
        maxIdx |= 4

    line = parseFloat(btc) + " " + parseFloat(eth) + " " + parseFloat(ltc)
    extra = ""
    print(line, end="")
    if isMax:
        extra += " MAX " + str(maxIdx)
    if isMin:
        extra += " MIN " + str(minIdx)
    print(extra)
    file.write(line + "\n")
    file.close()
    time.sleep(5)


