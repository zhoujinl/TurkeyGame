#!/usr/bin/python
#coding=utf-8

'''
模拟六合彩游戏
游戏规则：摇号，从 1-49 个号码中，选出特码。
假设当前赔率为X，即本金Y，得X倍数的奖金 Y*X。
为提供中奖的概率，每次压住为Z个Y，本程序计算如何在有限的资金下，尽可能的分配每次的押注成本Y,以提高中奖概率

为模拟真实的游戏，现假设X 为 48，Y为10，每次押注Z为13.
params: python calc.py -h 

三类：好运、一半、厄运

'''
import openpyxl 
import random
import datetime
from datafile import DataFile
totalNumber = 49.0
randomNumber = 100

class Turkey:
    '这是一只好斗的小火鸡'
    
    def __init__(self, name, options):
        self.name = name
        self.money = 0
        self.lastIswinMoney = 0
        self.winCount = 0
        self.playCount = 0
        self.options = options
        stime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        self.datafile = DataFile(r"E:\Git\turkeyGame\var\sample-" +stime +"-"+ str(name) + ".xlsx") 
        self.originBetting = options.betting
        self.probabilityOfWinningEachPeriod()
        #self.probability = self.options.numberBetting/totalNumber
        #self.probability = 0.5

    def probabilityOfWinningEachPeriod(self):
        '每次中奖的概率'
        #self.probability = self.options.numberBetting/totalNumber 
        self.probability = 0.3
        print '每次中奖的概率' + str(self.probability)

    def isWin(self):
        '本期是否中奖'
        #return random.randint(0, 100) < (self.probability * 100)
        return random.randint(0, 100) < (self.probability * 100)
        
    def makeMoney(self):  
        '本期是否赚钱。中则加钱，不中则扣钱'
        
        if self.isWin(): 
            makeMoney = self.options.betting * self.options.odds - self.options.betting * self.options.numberBetting
            self.winCount = self.winCount + 1 
        else :
            makeMoney = - (self.options.betting * self.options.numberBetting)
        self.lastIswinMoney = makeMoney
        self.playCount = self.playCount + 1
        self.money = self.money + makeMoney
        
        #记录每局输赢
        self.datafile.write2xlsx(numberPeriod=self.playCount,money=self.money,lastIswinMoney=self.lastIswinMoney,
                                    betting=self.options.betting,probability=self.probability,cost=self.options.betting * self.options.numberBetting)
        
    def makeMoneyByStrategy(self):
        '启用策略，当某几期之后，亏钱时，增大赌注，默认是翻倍;'   
        self.makeMoney()
        #todo 保存当前状态
        '''
        # 赌注开方
        if self.money < 0 :
            if self.options.betting < self.options.maxBetting/2 :
                self.options.betting = self.options.betting * 2              
        elif self.options.betting > self.originBetting  :
            self.options.betting = self.options.betting/2
        '''
        
        # 赌注每次增加一倍
        if self.money < 0 :  #亏钱的情况下加大筹码
            if self.options.betting < self.options.maxBetting  :
                self.options.betting = self.options.betting +  self.originBetting             
        else  :              #赚钱的情况下怎么处理    
            if self.options.betting <= self.options.maxBetting  :
                if self.lastIswinMoney > 0 : #如果上一期中了,加大筹码
                    self.options.betting = self.options.betting + self.originBetting  
                else : # 反之
                    self.options.betting = self.options.betting + self.originBetting  
                    
    def startGame(self):
        if self.options.autoIncreaseBetting == "true" :
            ''' ##有限游戏次数下的游戏
            for i in range(0,self.options.gameCount) :
                self.makeMoneyByStrategy()
            '''
            
            '''##赌徒模式 假如要赚到10000 才收手
            self.makeMoneyByStrategy()
            while self.money < 10000  :
                self.makeMoneyByStrategy()
                if self.money < -10000:
                    break
            '''
            '''## 有赚就跑模式 
            ## 看来一定要止损10000 ，止盈可以多一点
            self.makeMoneyByStrategy()
            while self.money < 100000  :
                self.makeMoneyByStrategy()
                if self.money < -10000:
                    break                   
            '''
            
            ##然而时间有限
            self.makeMoneyByStrategy()
            while self.money < 10000  :
                self.makeMoneyByStrategy()
                if self.money < -3000 :
                    break  
                if self.playCount > 30 :
                    break
        else :        
            for i in range(0,self.options.gameCount) :
                self.makeMoney() 
        return self.money
     
    def __del__(self):
        self.datafile.save2xlsx()
        
if __name__ == '__main__':
    from optparse import OptionParser
    import os

    parser = OptionParser()
    usage = "usage: %prog [options] arg1" 
    parser.add_option("-o", "--odds", dest="odds", help="The odds ;default 48", default='48', type="int")
    parser.add_option("-n", "--numberBetting", dest="numberBetting", help="The number of betting;default 12", default='13', type="int")
    parser.add_option("-b", "--betting", dest="betting", help="Each bet;init 10", default='20', type="int")
    parser.add_option("-a", "--auto", dest="autoIncreaseBetting", help="IS atuo Increase Each bet;default true", default='true', type="string")
    parser.add_option("-m", "--maxBetting", dest="maxBetting", help="The max Betting;default 100", default='100', type="int")
    parser.add_option("-c", "--count", dest="gameCount", help="The gameCount;default 100", default='10', type="int")

    (options, args) = parser.parse_args()
    #只开一局
    '''
    tukey=Turkey("xiaolizi",options)
    tukey.startGame()
    print ("最后盈利为：" + str(tukey.money))
    print ("最后一期盈利大小：" + str(tukey.lastIswinMoney))
    print ("总中奖次数：" + str(tukey.winCount))
    print ("总游戏次数：" + str(tukey.playCount))
    '''
    
    #以赌徒模式来计算，上下止盈、封顶均为10000 ,那么总次数为
    winCount = 0
    winMoney = 0
    gameCount = 0
    for i in range(0,10) :
        (options, args) = parser.parse_args()
        tukey=Turkey(i,options)
        thisWin=tukey.startGame()
        if thisWin > 0 :
            print "winCount:"+str(winCount)
            winCount = winCount + 1
        winMoney = winMoney + tukey.money
        gameCount = gameCount + tukey.playCount
        print ("第 %d 次总游戏次数："  %(i)  + str(tukey.playCount))
        print ("第 %d 次盈利为："  %(i)  + str(tukey.money))
        
    print ("大轮游戏赢次：" + str(winCount))
    print ("小轮游戏总次数：" + str(gameCount))
    print ("最后盈利为：" + str(winMoney))
  
    

