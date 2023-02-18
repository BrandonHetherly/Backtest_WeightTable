from re import split
import pandas as pd
import numpy as np
import csv
import datetime as dt
from functools import reduce
from pandas.tseries.offsets import MonthEnd

# x: the data,  na.rm: change "nan" values to 0 (either True or False)
# this will turn your df into an excel and change all nan values to 0 if na_rm is True
def checkData(data, na_rm=True):

    # checking that the type of data is a df
    if type(data) != type(pd.DataFrame()):
        try:
            if data.endswith(".xlsx"):
                data = pd.read_excel(data)
        except:
            print("data is not excel or dataframe")

            # checking for nan values and changing them to "0"
    if (na_rm):
        check_nan = data.isnull().values.any()
        if (check_nan):
            print("nan values detected")
            data = data.fillna(0)
    return data

def return_portfolio(data, weights):
    # df of closing prices
    df = checkData(data)
    df.columns = df.columns.str.strip()

    columnReturn = list(df.columns)
    columnReturn.remove("Date")

    # weight table df
    weight_table = checkData(weights, na_rm=False)
    # getting rid of white space
    weight_table.columns = weight_table.columns.str.strip()
    columnWeight = list(weight_table.columns)
    columnWeight.remove("Date")

    #check that both files have same stocks
    for x in range(len(columnWeight)):
        hasStock = False
        for y in range(len(columnReturn)):
            if(columnReturn[y] == columnWeight[x]):
                hasStock = True
        if hasStock == False:
            print("ERROR: Stocks do not match")
            return
    print("INFO: Stocks match")

    ### first day setup ###
    currentAmount = 100
    stockTempPrices = []

    weightDate = []
    weightStockName = columnWeight
    weightStockWeight = []
    for index, data in weight_table.iterrows():
        tempStockW = []
        for a in range(len(data)):
            if(a == 0):
                dateV = data[0].date()
                weightDate.append(str(dateV))
            else:
                tempStockW.append(data[a])
        weightStockWeight.append(tempStockW)

    returnDate = []
    returnStockName = columnReturn
    returnStockPrice = []
    for index, data in df.iterrows():
        tempStockP = []
        for a in range(len(data)):
            if (a == 0):
                dateV = data[0].date()
                returnDate.append(str(dateV))
            else:
                tempStockP.append(data[a])
        returnStockPrice.append(tempStockP)

    for x in range(len(returnStockName)):
        stockTempPrices.append(weightStockWeight[0][x]*currentAmount)

    #detect input type
    percentChangeTrue = False
    for i in returnStockPrice[0]:
        if(float(i) <= 1):
            percentChangeTrue = True
            break

    if(percentChangeTrue):
        print("INFO: Detected percent change input")
    else:
        print("INFO: Detected dollar amount input")


    lastDate = returnDate[-1]
    print("Starting Date:" + str(returnDate[0]))
    print("Starting Total Money:" + str(currentAmount))
    print("Starting Prices:")
    print(stockTempPrices)
    print("")
    index = -1
    weightRealloc = 1
    for var in returnStockPrice:
        index = index + 1
        curDate = returnDate[index]
        
        if(index >= 1):
            ## get percent change here ##
            for a in range(len(returnStockPrice[index])):
                if not percentChangeTrue:
                    tempVar = ((returnStockPrice[index][a] - returnStockPrice[index-1][a])/returnStockPrice[index-1][a])*100
                else:
                    tempVar = returnStockPrice[index][a]*100
                stockTempPrices[a] = stockTempPrices[a] + (tempVar*stockTempPrices[a]/100)

            foundDay = False
            ##check for reallocation
            for z in weightDate:
                if(z == curDate):
                    foundDay = True
                    currentAmount = 0
                    for a in stockTempPrices:
                        currentAmount = currentAmount + a
                    print("Date:" + curDate)
                    print("Total Money:" + str(currentAmount))
                    print("Current Allocation:")
                    print(stockTempPrices)
                    for a in range(len(stockTempPrices)):
                        stockTempPrices[a] = currentAmount*weightStockWeight[weightRealloc][a]
                    weightRealloc = weightRealloc + 1
                    print("Rellocation:")
                    print(stockTempPrices)
                    print("-----------------------------------")
                    print("")
                    break
            if(lastDate == curDate and foundDay == False):
                currentAmount = 0
                for a in stockTempPrices:
                    currentAmount = currentAmount + a
                print("Date:" + curDate)
                print("Total Money:" + str(currentAmount))
                print("Current Allocation:")
                print(stockTempPrices)


return_portfolio(data="Test_returns.xlsx", weights="weight_table_test.xlsx")
