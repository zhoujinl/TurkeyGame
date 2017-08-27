#!/usr/bin/python
#coding=utf-8

'''
ģ�����ϲ���Ϸ
��Ϸ����ҡ�ţ��� 1-49 �������У�ѡ�����롣
���赱ǰ����ΪX��������Y����X�����Ľ��� Y*X��
Ϊ�ṩ�н��ĸ��ʣ�ÿ��ѹסΪZ��Y�������������������޵��ʽ��£������ܵķ���ÿ�ε�Ѻע�ɱ�Y,������н�����

Ϊģ����ʵ����Ϸ���ּ���X Ϊ 48��YΪ10��ÿ��ѺעZΪ13.
params: python calc.py -h 

���ࣺ���ˡ�һ�롢����

'''
import openpyxl 
import random
import datetime
from datafile import DataFile
totalNumber = 49.0
randomNumber = 100

class Turkey:
    '����һֻ�ö���С��'
    
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
        'ÿ���н��ĸ���'
        #self.probability = self.options.numberBetting/totalNumber 
        self.probability = 0.3
        print 'ÿ���н��ĸ���' + str(self.probability)

    def isWin(self):
        '�����Ƿ��н�'
        #return random.randint(0, 100) < (self.probability * 100)
        return random.randint(0, 100) < (self.probability * 100)
        
    def makeMoney(self):  
        '�����Ƿ�׬Ǯ�������Ǯ���������Ǯ'
        
        if self.isWin(): 
            makeMoney = self.options.betting * self.options.odds - self.options.betting * self.options.numberBetting
            self.winCount = self.winCount + 1 
        else :
            makeMoney = - (self.options.betting * self.options.numberBetting)
        self.lastIswinMoney = makeMoney
        self.playCount = self.playCount + 1
        self.money = self.money + makeMoney
        
        #��¼ÿ����Ӯ
        self.datafile.write2xlsx(numberPeriod=self.playCount,money=self.money,lastIswinMoney=self.lastIswinMoney,
                                    betting=self.options.betting,probability=self.probability,cost=self.options.betting * self.options.numberBetting)
        
    def makeMoneyByStrategy(self):
        '���ò��ԣ���ĳ����֮�󣬿�Ǯʱ�������ע��Ĭ���Ƿ���;'   
        self.makeMoney()
        #todo ���浱ǰ״̬
        '''
        # ��ע����
        if self.money < 0 :
            if self.options.betting < self.options.maxBetting/2 :
                self.options.betting = self.options.betting * 2              
        elif self.options.betting > self.originBetting  :
            self.options.betting = self.options.betting/2
        '''
        
        # ��עÿ������һ��
        if self.money < 0 :  #��Ǯ������¼Ӵ����
            if self.options.betting < self.options.maxBetting  :
                self.options.betting = self.options.betting +  self.originBetting             
        else  :              #׬Ǯ���������ô����    
            if self.options.betting <= self.options.maxBetting  :
                if self.lastIswinMoney > 0 : #�����һ������,�Ӵ����
                    self.options.betting = self.options.betting + self.originBetting  
                else : # ��֮
                    self.options.betting = self.options.betting + self.originBetting  
                    
    def startGame(self):
        if self.options.autoIncreaseBetting == "true" :
            ''' ##������Ϸ�����µ���Ϸ
            for i in range(0,self.options.gameCount) :
                self.makeMoneyByStrategy()
            '''
            
            '''##��ͽģʽ ����Ҫ׬��10000 ������
            self.makeMoneyByStrategy()
            while self.money < 10000  :
                self.makeMoneyByStrategy()
                if self.money < -10000:
                    break
            '''
            '''## ��׬����ģʽ 
            ## ����һ��Ҫֹ��10000 ��ֹӯ���Զ�һ��
            self.makeMoneyByStrategy()
            while self.money < 100000  :
                self.makeMoneyByStrategy()
                if self.money < -10000:
                    break                   
            '''
            
            ##Ȼ��ʱ������
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
    #ֻ��һ��
    '''
    tukey=Turkey("xiaolizi",options)
    tukey.startGame()
    print ("���ӯ��Ϊ��" + str(tukey.money))
    print ("���һ��ӯ����С��" + str(tukey.lastIswinMoney))
    print ("���н�������" + str(tukey.winCount))
    print ("����Ϸ������" + str(tukey.playCount))
    '''
    
    #�Զ�ͽģʽ�����㣬����ֹӯ���ⶥ��Ϊ10000 ,��ô�ܴ���Ϊ
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
        print ("�� %d ������Ϸ������"  %(i)  + str(tukey.playCount))
        print ("�� %d ��ӯ��Ϊ��"  %(i)  + str(tukey.money))
        
    print ("������ϷӮ�Σ�" + str(winCount))
    print ("С����Ϸ�ܴ�����" + str(gameCount))
    print ("���ӯ��Ϊ��" + str(winMoney))
  
    

