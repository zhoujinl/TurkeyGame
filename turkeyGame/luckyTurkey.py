#!/usr/bin/python
#coding=utf-8

import turkeyGame  

class LuckyTurkey(turkeyGame.Turkey):

    def probabilityOfWinningEachPeriod(self):
        'ÿ���н��ĸ���'
        print '�������˵�С��,����ÿ���н��ĸ���:0.5' 
        return 0.5

if __name__ == '__main__':
    print "I'm a lucky turkey."