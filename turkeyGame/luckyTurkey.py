#!/usr/bin/python
#coding=utf-8

import turkeyGame  

class LuckyTurkey(turkeyGame.Turkey):

    def probabilityOfWinningEachPeriod(self):
        '每次中奖的概率'
        print '我是幸运的小火鸡,所以每次中奖的概率:0.5' 
        return 0.5

if __name__ == '__main__':
    print "I'm a lucky turkey."