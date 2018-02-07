from random import uniform, choice, expovariate, lognormvariate
import os
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import requests

os.system('cls')


def updatePrice(prices, lastPrice, k, tendency):
    if tendency == "UP":
        minK = lastPrice
        maxK = lastPrice * (1 + k)
    elif tendency == "DOWN":
        minK = lastPrice * (1 - k)
        maxK = lastPrice
    else:
        minK = lastPrice * (1 - (k / 2))
        maxK = lastPrice * (1 + (k / 2))
    newPrice = uniform(minK, maxK)
    prices.append(newPrice)
    #print(newPrice, tendency, minK, maxK)
    return newPrice

def soldCoins(newPrice, lastExchangePrice, money, k, queueAv):
    relation = lastExchangePrice / newPrice - 1
    if relation > (k + queueAv):
        #print("SELL: " + parseFloat(newPrice))
        lastExchangePrice = newPrice
    elif relation < ((k + queueAv) - 1):
        #print("SELL: " + parseFloat(newPrice))
        lastExchangePrice = newPrice

    return lastExchangePrice

def buyedCoins(newPrice, lastExchangePrice, money, k, queueAv):
    relation = lastExchangePrice / newPrice - 1
    if relation > (k + queueAv):
        #print("BUY: " + parseFloat(newPrice))
        lastExchangePrice = newPrice
    elif relation < ((k + queueAv) - 1):
        #print("SELL: " + parseFloat(newPrice))
        lastExchangePrice = newPrice

    return lastExchangePrice

def optimizedMoney(prices, initialCoins):
    money = initialMoney
    coins = initialCoins
    lastPrice = prices[0]
    for i in prices:
        if i < (lastPrice * 1.04):
            coins = money / lastPrice
        elif i > (lastPrice * 1.04):
            money = coins * i

        lastPrice = i

        #print(money, coins)

    return money
            

def parseFloat(num):
    return "{0:.2f}".format(num)

for j in range(1):
    initialPrice = 650.0
    maxVal = initialPrice 
    minVal = initialPrice
    initialMoney = 100.0
    money = initialMoney
    initialCoins = money / initialPrice
    coins = initialCoins
    prices = [initialPrice]
    lastExchangePrice = initialPrice
    moneyInside = True
    timesSameChoice = 3
    lastTendency = tendency = choice(["UP", "DOWN", "INESTABLE"])
    l = deque()
    """for i in range(1000):
        k = 0.20
        lastPrice = prices[i]
        if timesSameChoice > 0:
            tendency = lastTendency
            timesSameChoice -= 1
        else:
            tendency = choice(["UP", "DOWN", "INESTABLE"])
            while tendency == lastTendency:
                tendency = choice(["UP", "DOWN", "INESTABLE"])

            if tendency == "UP":
                timesSameChoice = 2
            elif tendency == "DOWN":
                timesSameChoice = 2
            else:
                timesSameChoice = 0

        if tendency == "UP":
            l.append(1)
        elif tendency == "INESTABLE":
            l.append(0)
        else:
            l.append(-1)

        if i >= 10: 
            l.popleft()

        queueAv = sum(l) / len(l)

        average = float(sum(prices) / len(prices))

        newPrice = updatePrice(prices, lastPrice, 0.01, tendency)

        lastTendency = tendency

        tempLastExchangePrice = lastExchangePrice

        if moneyInside:
            money = coins * newPrice
            lastExchangePrice = soldCoins(newPrice, lastExchangePrice, money, k, queueAv)
        else:
            lastExchangePrice = buyedCoins(newPrice, lastExchangePrice, money, k, queueAv)

        if tempLastExchangePrice != lastExchangePrice:
            moneyInside = not moneyInside
            if moneyInside:
                coins = money / newPrice

        isMaxVal = newPrice > maxVal
        if isMaxVal:
            maxVal = newPrice

        isMinVal = newPrice < minVal
        if isMinVal:
            minVal = newPrice
            
        print(parseFloat(newPrice) + "    =>    " + parseFloat(money) + "   =>   " + parseFloat(coins) + "        " + ("+ " if lastPrice < newPrice else "- ") + ("MAX" if isMaxVal else "") + ("MIN" if isMinVal else ""))"""

    file = open("data.txt", "r")
    btcPrices = []
    ethPrices = []
    ltcPrices = []
    for line in file:
        btc, eth, ltc = line.split(" ")
        btcPrices.append(float(btc))
        ethPrices.append(float(eth))
        ltcPrices.append(float(ltc))

    print("")
    print("##########")
    print("Starting: " + parseFloat(initialMoney) + ", Starting Price: " + parseFloat(initialPrice))
    print("Money: " + parseFloat(money) + ", " + parseFloat(money*100/initialMoney-100) + "%")
    print("Coins: " + parseFloat(coins) + ", " + parseFloat(coins*100/initialCoins-100) + "%")

    #average = float(sum(prices) / len(prices))
    #print("Average coin value: " + parseFloat(average))

    #optimized = optimizedMoney(prices, initialCoins)
    #print(optimized)
    #print("Optimized money " + parseFloat(optimized))
    #print("Min val: " + parseFloat(minVal) + ", Max val: " + parseFloat(maxVal))
    #print("Efficience: " + parseFloat(money - initialMoney) + ", " + parseFloat(optimized - initialMoney) + ", " + parseFloat((money - initialMoney) * 100 / (optimized - initialMoney+0.1)) + "%")

    plt.subplot(3,1,1)
    plt.plot(np.array(btcPrices), "y")

    plt.subplot(3,1,2)
    plt.plot(np.array(ethPrices), "b")

    plt.subplot(3,1,3)
    plt.plot(np.array(ltcPrices), "m")
    plt.show()