# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 10:30:39 2019

@author: HP
"""

from cal_sim import simcal




while True:
    question0 = input("口语化描述")
    question = question0.replace('（','(')
    question = question.replace('）',')')
    question = question.replace('、',')')
    question = question.replace('“','')
    question = question.replace('”','')
    question = question.replace(' ','')
    if question == 'q':
        print("你好！")
        break    

    else:
        simcal(question.encode("utf-8"))



   

    


    
    
    