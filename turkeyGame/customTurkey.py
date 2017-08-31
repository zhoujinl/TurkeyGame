#!/usr/bin/python
#coding=utf-8

import turkeyGame    

class CustomTurkey(turkeyGame.Turkey):       
    g_i = -1
    g_win = [0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1]
    
    def probabilityOfWinningEachPeriod(self):
        '每次中奖的概率'
        print '我是自定义的小火鸡,所以每次中奖的概率:' +str(CustomTurkey.g_win) 
        return 0.5
        
    def isWin(self):
        '本期是否中奖,随机获取'
        CustomTurkey.g_i = CustomTurkey.g_i + 1
        return CustomTurkey.g_win[CustomTurkey.g_i] 
        
if __name__ == '__main__':
    print "I'm a lucky turkey."