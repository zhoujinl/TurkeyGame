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

totalNumber = 49.0
randomNumber = 100

class Turkey:
    '����һֻ�ö���С��'
    
    def __init__(self, name, options):
        self.name = name
        self.money = 0
        self.lastIswinMoney = 0
        self.winCount = 0
        self.options = options
        self.originBetting = options.betting
        self.probabilityOfWinningEachPeriod()
        self.probability = self.options.numberBetting/totalNumber
        #self.probability = 0.5

    def probabilityOfWinningEachPeriod(self):
        'ÿ���н��ĸ���'
        self.probability = self.options.numberBetting/totalNumber 
        print 'ÿ���н��ĸ���: ' + str(self.probability)

    def isWin(self):
        '�����Ƿ��н�'
        #return random.randint(0, 100) < (self.probability * 100)
        print (random.randint(0, 100) < (self.probability * 100))
        return "False"
        
    def makeMoney(self):  
        '�����Ƿ�׬Ǯ�������Ǯ���������Ǯ'
        print ("����Ѻע��С��" + str(tukey.options.betting))
        if self.isWin():
            makeMoney = self.options.betting * self.options.odds - self.options.betting * self.options.numberBetting
            self.winCount = self.winCount + 1 
        else :
            makeMoney = - (self.options.betting * self.options.numberBetting)
        self.lastIswinMoney = makeMoney
        self.money = self.money + makeMoney

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
        if self.money < 0 :
            if self.options.betting < self.options.maxBetting  :
                self.options.betting = self.options.betting +  self.originBetting             
        elif self.options.betting > self.originBetting  :
            self.options.betting = self.options.betting - self.originBetting    
            
    def startGame(self):
        if self.options.autoIncreaseBetting == "true" :
            for i in range(0,self.options.gameCount) :
                self.makeMoneyByStrategy()
        else :        
            for i in range(0,self.options.gameCount) :
                self.makeMoney() 
        return self.money
     
if __name__ == '__main__':
    from optparse import OptionParser
    import os

    parser = OptionParser()
    usage = "usage: %prog [options] arg1" 
    parser.add_option("-o", "--odds", dest="odds", help="The odds ;default 48", default='48', type="int")
    parser.add_option("-n", "--numberBetting", dest="numberBetting", help="The number of betting;default 12", default='12', type="int")
    parser.add_option("-b", "--betting", dest="betting", help="Each bet;init 10", default='10', type="int")
    parser.add_option("-a", "--auto", dest="autoIncreaseBetting", help="IS atuo Increase Each bet;default true", default='true', type="string")
    parser.add_option("-m", "--maxBetting", dest="maxBetting", help="The max Betting;default 100", default='100', type="int")
    parser.add_option("-c", "--count", dest="gameCount", help="The gameCount;default 100", default='10', type="int")

    (options, args) = parser.parse_args()
    tukey=Turkey("xiaolizi",options)

    tukey.startGame()
    print ("���ӯ��Ϊ��" + str(tukey.money))
    print ("���һ��ӯ����С��" + str(tukey.lastIswinMoney))
    print ("���н�������" + str(tukey.winCount))

