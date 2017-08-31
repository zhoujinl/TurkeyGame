#!/usr/bin/python
#coding=utf-8

'''
ģ�����ϲ���Ϸ
��Ϸ����ҡ�ţ��� 1-49 �������У�ѡ�����롣
���赱ǰ����ΪX��������Y����X�����Ľ��� Y*X��
Ϊ�ṩ�н��ĸ��ʣ�ÿ��ѹסΪZ��Y�������������������޵��ʽ��£������ܵķ���ÿ�ε�Ѻע�ɱ�Y,������н�����

Ϊģ����ʵ����Ϸ���ּ���X Ϊ 48��YΪ10��ÿ��ѺעZΪ13.
params: python calc.py -h 

����������
1.׼ȷ��
2.ÿ����ע����
3.��ʱֹӯֹ��

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
    '����һֻ�ö���С��'
    
    def __init__(self, name, options):
        self.name = name
        self.money = 0
        self.lastwinMoney = 0
        self.winCount = 0
        self.playCount = 0
        self.continuousLoss = 0   #Ͷע�����õ�
        self.continuousWin = 0    #Ͷע�����õ�
        
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
     
    #����̳�
    def probabilityOfWinningEachPeriod(self):
        'ÿ���н��ĸ��ʣ�����������д'
        return self.numberBetting/self.totalNumber
        
    def isWin(self):
        '�����Ƿ��н�,�����ȡ'
        return random.randint(0, 100) < (self.probability * 100)
        
    #���Խӿ�    
    def setStrategy(self,strategy):
        self.strategy = strategy 
        
    #ֹӯֹ��ӿ�    
    def setPlayer(self,player):
        self.player = player           
        
   
        
    def earnMeneyOnePeriod(self):  
        '�����Ƿ�׬Ǯ�������Ǯ���������Ǯ'        
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
        '��¼ÿ����Ӯ'
        self.datafile.write2xlsx(numberPeriod=self.playCount,money=self.money,lastwinMoney=self.lastwinMoney,
                                    betting=self.currentBetting,probability=self.probability,cost=self.currentBetting * self.numberBetting)
        
    def startStrategy(self):
        '���ò��ԣ���ĳ����֮�󣬿�Ǯʱ�������ע��Ĭ���Ƿ���;'   
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
    '''�ܴ���14��,��Ϸ����
    ���У���+10��
    �У����˳���Ϸ�����¿�ʼ
    �ֱ������һ��...N�ε�ӯ�����
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
    
    print ("���ӯ��Ϊ��" + str(tukey.money))
    print ("���һ��ӯ����С��" + str(tukey.lastwinMoney))
    print ("���н�������" + str(tukey.winCount))
    print ("����Ϸ������" + str(tukey.playCount))

    

