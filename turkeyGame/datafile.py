#!/usr/bin/python
#coding=utf-8
'''
供 tukeyGame 调用
使用 openpyxl 包保存中间数据到 xlsx ，以便用excel 分析统计
openpyxl参考手册：https://openpyxl.readthedocs.io/en/default/tutorial.html#create-a-workbook

'''

from openpyxl import Workbook

class DataFile:
    '状态数据保存'
    
    def __init__(self,filename):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Tukey"
        self.ws.append(["当前期数", "当前总盈利","本期赚钱","本期成本","本期单注金额","本期中奖概率" ])    
        self.filename = filename
       
    def write2xlsx(self, **other):
        # Rows can also be appended
        self.ws.append([other["numberPeriod"],other["money"],other["lastwinMoney"],other["cost"],other["betting"],other["probability"]])    
        
    def save2xlsx(self):
        self.wb.save(self.filename)
    
    def close(self):
        self.wb.close()

        