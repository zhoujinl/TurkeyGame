#!/usr/bin/python
#coding=utf-8

'''
模拟六合彩游戏
游戏规则：摇号，从 1-49 个号码中，选出特码。
假设当前赔率为X，即本金Y，得X倍数的奖金 Y*X。
为提供中奖的概率，每次压住为Z个Y，本程序计算如何在有限的资金下，尽可能的分配每次的押注成本Y,以提高中奖概率

为模拟真实的游戏，现假设X 为 48，Y为10，每次押注Z为13.
params: python calc.py -h 

三个变量：
1.准确率
2.每期下注策略
3.何时止盈止损

'''
import openpyxl 
import random
import datetime

import customTurkey  
#import luckyTurkey  
import strategy
import player

from datafile import DataFile


class Turkey:
    '这是一只好斗的小火鸡'
    
    def __init__(self, name, options):
        self.name = name
        self.money = 0
        self.lastwinMoney = 0
        self.winCount = 0
        self.playCount = 0
        self.continuousLoss = 0   #投注策略用到
        self.continuousWin = 0    #投注策略用到
        
        self.originBetting = options.betting
        self.currentBetting = options.betting
        self.gameCount = options.gameCount
        self.odds = options.odds
        self.maxBetting = options.maxBetting
        self.totalNumber = options.totalNumber
        self.numberBetting = options.numberBetting
        
        self.probability = self.probabilityOfWinningEachPeriod()                        
        stime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        self.datafile = DataFile(r"E:\Git\turkeyGame\var\sample-" + stime +"-"+ str(name) + ".xlsx") 
     
    #子类继承
    def probabilityOfWinningEachPeriod(self):
        '每次中奖的概率：可由子类重写'
        return self.numberBetting/self.totalNumber
        
    def isWin(self):
        '本期是否中奖,随机获取'
        return random.randint(0, 100) < (self.probability * 100)
        
    #策略接口    
    def setStrategy(self,strategy):
        self.strategy = strategy 
        
    #止盈止损接口    
    def setPlayer(self,player):
        self.player = player           
        
   
        
    def earnMeneyOnePeriod(self):  
        '本期是否赚钱。中则加钱，不中则扣钱'        
        if self.isWin(): 
            self.winCount = self.winCount + 1 
            self.continuousWin = self.continuousWin + 1 
            self.continuousLoss = 0
            makeMoney = self.currentBetting * self.odds - self.currentBetting * self.numberBetting
        else :
            self.continuousLoss = self.continuousLoss + 1 
            self.continuousWin = 0 
            makeMoney = - (self.currentBetting * self.numberBetting)

        self.lastwinMoney = makeMoney
        self.playCount = self.playCount + 1
        self.money = self.money + makeMoney
        
    def saveStateEachPeriod(self):
        '记录每局输赢'
        self.datafile.write2xlsx(numberPeriod=self.playCount,money=self.money,lastwinMoney=self.lastwinMoney,
                                    betting=self.currentBetting,probability=self.probability,cost=self.currentBetting * self.numberBetting)
        
    def startStrategy(self):
        '启用策略，当某几期之后，亏钱时，增大赌注，默认是翻倍;'   
        self.strategy.doStrategy()
        
    def playGameEachPeriod(self):
        self.earnMeneyOnePeriod()
        self.saveStateEachPeriod()
        self.startStrategy()
    
    def cleanGame(self):
        self.datafile.save2xlsx()
        self.datafile.close
     
    def startGame(self):    
        self.player.play()       
        self.cleanGame()
        return self.money


def customThink(options):
    '''总次数14次,游戏规则：
    不中，则+10；
    中，则退出游戏，重新开始
    分别计算中一次...N次的盈利情况
    '''
    for i in range(0,14) :
        tukey = customTurkey.CustomTurkey("xiaolizi-"+str(i),options)
        tukey.setStrategy(strategy.CrazyStrategy(tukey))
        tukey.setPlayer(player.CrazyPlayer(tukey))
        tukey.startGame()
    
        

if __name__ == '__main__':
    from optparse import OptionParser
    import os

    parser = OptionParser()
    usage = "usage: %prog [options] arg1" 
    parser.add_option("-o", "--odds", dest="odds", help="The odds ;default 48", default='48', type="int")
    parser.add_option("-t", "--totalNumber", dest="totalNumber", help="The totalNumber ;default 49", default='49.0', type="float")
    parser.add_option("-n", "--numberBetting", dest="numberBetting", help="The number of betting;default 12", default='13', type="int")
    parser.add_option("-m", "--maxBetting", dest="maxBetting", help="The max Betting;default 100", default='100', type="int")
    parser.add_option("-c", "--count", dest="gameCount", help="The gameCount;default 100", default='14', type="int")
    parser.add_option("-b", "--betting", dest="betting", help="Each bet;init 10", default='10', type="int")

    (options, args) = parser.parse_args()
    
    tukey = customTurkey.CustomTurkey("xiaolizi",options)
    tukey.setStrategy(strategy.CrazyStrategy(tukey))
    tukey.setPlayer(player.CrazyPlayer(tukey))
    tukey.startGame()
    
    print ("最后盈利为：" + str(tukey.money))
    print ("最后一期盈利大小：" + str(tukey.lastwinMoney))
    print ("总中奖次数：" + str(tukey.winCount))
    print ("总游戏次数：" + str(tukey.playCount))

    

