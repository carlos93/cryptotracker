import time
import requests
import sys
from multiprocessing import Pool, TimeoutError

MAX_COINS = 4

def parseFloat(num):
    return "{0:.4f}".format(num)

def getPriceFromGDAX(coin):
    r = requests.get("https://api.gdax.com/products/"+coin+"/book?level=1", headers={"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"})
    #print(r.json())
    json = r.json()
    value = (float(json["bids"][0][0]) + float(json["asks"][0][0])) / 2.0
    return value

if __name__ == '__main__':
    min = [99999999, 99999999, 99999999, 99999999]
    max = [0, 0, 0, 0]
    with Pool(processes=4) as pool:
        while True:
            try:
                isMin = False
                isMax = False
                minIdx = 0
                maxIdx = 0
                file = open("data.txt", "a")
                coins = [0, 0, 0, 0]

                coins[0] = pool.apply_async(getPriceFromGDAX, ("BTC-EUR",)).get()
                coins[1] = pool.apply_async(getPriceFromGDAX, ("ETH-EUR",)).get()
                coins[2] = pool.apply_async(getPriceFromGDAX, ("LTC-EUR",)).get()
                coins[3] = pool.apply_async(getPriceFromGDAX, ("BCH-EUR",)).get()

                for i in range(MAX_COINS):
                    if coins[i] < min[i]:
                        min[i] = coins[i]
                        isMin = True
                        minIdx |= 1 << i
                        
                    if coins[i] > max[i]:
                        max[i] = coins[i]
                        isMax = True
                        maxIdx |= 1 << i

                line = "BTC: " + parseFloat(coins[0]) + ", ETH: " + parseFloat(coins[1]) + ", LTC: " + parseFloat(coins[2]) + ", BCH: " + parseFloat(coins[3])
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
            except:
                file = open("logs.txt", "a")
                file.write("Unexpected error: " + sys.exc_info()[0])
                file.close()
                raise


