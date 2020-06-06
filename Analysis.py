# Выделение ключевых слов
from rutermextract import TermExtractor
term_extractor = TermExtractor()
#  Нормализация слов
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

# Список должностей
empl = ['администратор гостиницы', 'специалист', 'директор гостиницы', 'посетитель']

text = open('analysis_example.txt', 'r', encoding="utf-8").read()
print(text)
#  Разделение текста на предложения
lst = text.split("\n")
list(filter(None, lst))
# Нормализация каждого слова в предложении отдельно
def normalize_sentence(lst):
   norm = list()
   for i in lst:
      tmp = i.split()
      s=''
      for j in tmp:
         s = s + morph.parse(j)[0].normal_form + ' '
      norm.append(s)
   return norm
# Добавляю индексы для каждого предложения
def numbers(lst):
   tmp = list()
   for i in range(0, len(lst)):
      tmp1 = [lst[i], i]
      tmp.append(tmp1)
   return tmp
# Поиск совпадений
def empl_search(lst, empl):
   newLst = list()
   for i in lst:     #  i --> [предложение, индекс]
      flag = False   #  Флаг того что в рпедложении нашлось слово
      for term in term_extractor(i[0]):   #  Перебор ключевых слов предложения
         print(term.normalized)
         for k in empl:
            if term.normalized.find(k) != -1:   #  Проверка: нашлось ли слово?
               print('++++++++', term, '---', k)
               flag = True
               break
         if flag:
            newLst.append(i)
            break
   return newLst
# Первый проход идет без нормализации слов
newLst1_1 = numbers(lst)
newLst1 = empl_search(newLst1_1, empl)

print()
print()
print()

# Второй проход с нормализацией строк
q = normalize_sentence(lst)
newLst2_1 = numbers(q)
newLst2 = empl_search(newLst2_1, empl)

print()
print()
print()

print(newLst1)

print()
print()
print()

print(newLst2)
# Собираем оба варианта вместе (если каким-то образом какой-то из вариантов не нашел что-то)
final = set()
for i in newLst1:
   final.add(lst[i[1]])
for i in newLst2:
   final.add(lst[i[1]])

for i in final:
   print(i)