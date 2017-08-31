#!/usr/bin/python
#coding=utf-8

import turkeyGame
'''
押注策略
'''
class Strategy():
    
    def __init__(self, turkey):
        self.turkey = turkey
        
    def doStrategy(self):
        '默认押注策略，保持不变'
        #todo nothing
        self.turkey.currentBetting = self.turkey.currentBetting


class WiseStrategy(Strategy):
    '明智的玩法,追求风险与收益成正比'
    
    def doStrategy(self):
        #todo nothing
        '''
        # 赌注开方
        if self.money < 0 :
            if self.currentBetting < self.maxBetting/2 :
                self.currentBetting = self.currentBetting * 2              
        elif self.currentBetting > self.originBetting  :
            self.currentBetting = self.currentBetting/2
        '''                
        if self.turkey.money < 0 :  #亏钱的情况下如何处理  
            if self.turkey.continuousLoss > 2 :
                if self.turkey.currentBetting < self.turkey.maxBetting  :
                    self.turkey.currentBetting = self.turkey.currentBetting +  self.turkey.originBetting             
        else : #赚钱的情况下怎么处理    
            if self.turkey.continuousWin > 1 :
                if self.turkey.currentBetting < self.turkey.maxBetting  :
                    self.turkey.currentBetting = self.turkey.currentBetting + self.turkey.originBetting  
            #有收益的时候，以保本为旨
            elif self.turkey.currentBetting > self.turkey.originBetting : 
                self.turkey.currentBetting = self.turkey.currentBetting - self.turkey.originBetting 

class CrazyStrategy(Strategy):
    '从10开始，每输一次就就筹码+10'
    
    def doStrategy(self):
        #todo nothing
        '''
        # 赌注开方
        if self.money < 0 :
            if self.currentBetting < self.maxBetting/2 :
                self.currentBetting = self.currentBetting * 2              
        elif self.currentBetting > self.originBetting  :
            self.currentBetting = self.currentBetting/2
        ''' 
        if self.turkey.lastwinMoney > 0 :        
            self.turkey.currentBetting =  self.turkey.originBetting             
        else :     
            self.turkey.currentBetting = self.turkey.currentBetting + self.turkey.originBetting   
            
        self.turkey.makeMoney = self.turkey.currentBetting * self.turkey.odds - self.turkey.currentBetting * self.turkey.numberBetting
        #如果发现该赌注在赢的情况下，无法一次性翻本，则继续+self.turkey.originBetting
        while self.turkey.money + self.turkey.makeMoney < 0 :
            self.turkey.currentBetting = self.turkey.currentBetting + self.turkey.originBetting             
            self.turkey.makeMoney = self.turkey.currentBetting * self.turkey.odds - self.turkey.currentBetting * self.turkey.numberBetting

        
if __name__ == '__main__':
    print "I'm the Strategy."