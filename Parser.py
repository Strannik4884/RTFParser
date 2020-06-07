# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 19:20:30 2020

@author: twi9g
"""

import os
os.chdir(r".spyder-py3\\rosAtom\\data")
from striprtf.striprtf import rtf_to_text
import re
import numpy as np
import json
from json import JSONEncoder

class Paragraph():
    def __init__(self, name, context, profession, appointed):
        self.name = name
        self.context = context
        self.profession = profession
        self.appointed = appointed
    def set_profession(self, profession):
        self.profession = profession
    def set_appointed(self, appointed):
        self.appointed = appointed

class ParagraphEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Paragraph):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
#загружаем результат в json
def toJSON(result, filename, profession, appointed):
    with open(filename, 'w', encoding='cp1251') as f:
        json.dump({"paragraph":result},f, ensure_ascii=False, cls=ParagraphEncoder)
#получаем болки текста с параграфами
def Get_Block(reg_start, reg_end, text):
    #Поиск начала блоков
    start = re.search(reg_start, text)
    end = re.search(reg_end, text)
    #Определение блоков
    block = text[start.end():end.start()]
    return(block)
#Получаем массивы строк для каждого параграфа
def Get_String(block):
    block_records = []
    stop = 100
    er = 0
    while len(block) > 0:
        result = re.search(r'([0-9-\.]+) ([а-я-А-Я-\ -\,-\.]+)', block)
        stop = stop - 1
        if(stop <= 0):
            break
        try:
            block = block[result.end():]
            if(result.group(0) != ' '):
                block_records.append({"number":result.group(1),
                                      "text":result.group(2)})
        except:
            er = er+1
    return(block_records)

def Algorithm(paragraphs, text, filename):
    result = []
    er = 0
    try:
        for i in range(len(paragraphs)-1):
            block = Get_Block(paragraphs[i], paragraphs[i+1], text)
            paragraph = Paragraph(paragraphs[i],
                        Get_String(block), '', '')
            if(i == 0):
                try:
                    profession = (re.search(r'([а-я-А-Я-\ ]+) относится', 
                                            paragraph.context[0]['text'])).group(1)
                except:
                    profession = ''
                try:    
                    appointed = (re.search(r'производится приказом ([а-я-А-Я-\ ]+)', 
                                            paragraph.context[2]['text'])).group(1)
                except:
                    appointed = ''
            paragraph.set_profession(profession)
            paragraph.set_appointed(appointed)
            result.append(paragraph)
    except:
      er = er+1
    new_filename = (re.search(r'([0-9-а-я-А-Я]+)', filename)).group(0) + '.json'
    
    if(profession != '' and appointed != ''):
        toJSON(result, new_filename, profession, appointed)
    elif(profession == '' and appointed != ''):
        toJSON(result, new_filename, '', appointed)
    elif(profession != '' and appointed == ''):
        toJSON(result, new_filename, profession, '')
    elif(profession == '' and appointed == ''):
        toJSON(result, new_filename, '', '')
    return('Succussed')

#Получаем файлы директории
files = os.listdir(r".")
#Проходим по всем файлам и собираем блоки
for i in files:
    file = open(i,'r')
    text = rtf_to_text(file.read())
    try:
        paragraphs = [r'Общие положения', r'Должностные обязанности',
                      r'Права', r'Ответственность', 'С инструкцией ознакомлен']
        Algorithm(paragraphs, text, i)
    except:
      print('Файл: ' + i + ' нелязя преобразовать')
    file.close()