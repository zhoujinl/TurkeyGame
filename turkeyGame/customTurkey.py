#!/usr/bin/python
#coding=utf-8

import turkeyGame    

class CustomTurkey(turkeyGame.Turkey):       
    g_i = -1
    g_win = [0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1]
    
    def probabilityOfWinningEachPeriod(self):
        'ÿ���н��ĸ���'
        print '�����Զ����С��,����ÿ���н��ĸ���:' +str(CustomTurkey.g_win) 
        return 0.5
        
    def isWin(self):
        '�����Ƿ��н�,�����ȡ'
        CustomTurkey.g_i = CustomTurkey.g_i + 1
        return CustomTurkey.g_win[CustomTurkey.g_i] 
        
if __name__ == '__main__':
    print "I'm a lucky turkey."