#!/usr/bin/python
#coding=utf-8

import turkeyGame
'''
玩家：何时止盈止损
'''
class Player():
    
    def __init__(self, turkey):
        self.turkey = turkey
        
    def play(self):
        '普通玩家'
        for i in range(0,self.turkey.gameCount) :
            self.turkey.playGameEachPeriod()

class WisePlayer(Player):

    def play(self):
        '每次中奖的概率'
        #todo nothing
        self.turkey.currentBetting = self.turkey.currentBetting
        '''
        ##有限游戏次数下的游戏
        for i in range(0,self.gameCount) :
            self.playGameEachPeriod()
        '''
        
        '''##赌徒模式 假如要赚到10000 才收手
        self.playGameEachPeriod()
        while self.money < 10000  :
            self.playGameEachPeriod()
            if self.money < -10000:
                break
        '''
        '''## 有赚就跑模式 
        ## 看来一定要止损10000 ，止盈可以多一点
        self.playGameEachPeriod()
        while self.money < 100000  :
            self.playGameEachPeriod()
            if self.money < -10000:
                break                   
        '''
        
        '''
        ##然而时间有限
        self.playGameEachPeriod()
        while self.money < 10000  :
            self.playGameEachPeriod()
            if self.money < -3000 :
                break  
            if self.playCount > 30 :
                break
        '''
            
class CrazyPlayer(Player):

    def play(self):
        ## 有赚就跑模式 
        for i in range(0,self.turkey.gameCount) :
            self.turkey.playGameEachPeriod()  
            if self.turkey.money > 0 :
                break;
        
                
        
if __name__ == '__main__':
    print "I'm the Strategy."