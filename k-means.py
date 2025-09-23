import math
import numpy as np
import matplotlib.pyplot as plt

rg=int(input('\nВыберите метод вычисления расстояния:\n1. Ближайшего соседа \n2. Дальнего соседа\n'))

k=int(input('Введите количество кластеров='))

obj=int(input('\nКоличество объектов='))

t=int(input('\nКоличество переменных='))

r=int(input('\nВыберите режим заполнения данных:\n1. Ввести с клавиатуры \n2. Заполнить случайными числами\n'))

clasters=[]
X=[]

if r==1:    # ввод точек
    for i in range (0,obj):
        X.append([])
        for j in range(0,t):
            print('\nТочка ',i,'. Переменная Х',j,'=')
            X[i].append(float(input()))
            
if r==2:    # создание случайных точек
    min_d=int(input('\nВведите минимум диапазона='))
    max_d=int(input('\nМаксимум диапазона='))
    X=np.asarray(X)
    X=np.random.randint (min_d, max_d, (obj, t))

X=np.asarray(X)
print('Исходные данные:\n',X)

for i in range (0,obj):
    clasters.append(['№'+str(i+1),X[i]])

sum_rasst=0
m_rasst=[]
for i in range (0,obj):     # создаём матрицу расстояний
    m_rasst.append([])
    print(m_rasst)
    for j in range(0,obj):
        for l in range (0,t):
            sum_rasst+=(X[j,l]-X[i,l])**2
        m_rasst[i].append(math.sqrt(sum_rasst))
        sum_rasst=0
m_rasst=np.asarray(m_rasst)
print('\nМатрица расстояний:\n',m_rasst)

num=0
while len(clasters)!=k:
    num += 1
    
    if (rg==1):
        mr=np.where(m_rasst>0, m_rasst, np.inf).min(axis=1)     # поиск близких кластеров
        mr=np.where(mr==mr.min())
        mr1=int(mr[0][0])
        mr2=int(mr[0][1])
        print('\n',num,'. Номера кластеров с минимальным расстоянием:',mr1+1,mr2+1)
        
        for i in range (0,obj):      # изменение матрицы расстояний
            if ((m_rasst[mr1,i]!=0) and (m_rasst[mr2,i]!=0)):
                m_rasst[mr1,i]=np.minimum(m_rasst[mr1,i],m_rasst[mr2,i])
            if ((m_rasst[i,mr1]!=0) and (m_rasst[i,mr2]!=0)):
                m_rasst[i,mr1]=np.minimum(m_rasst[mr1,i],m_rasst[mr2,i])
                
    if (rg==2):
        mr=np.where(m_rasst>0, m_rasst, -np.inf).max(axis=1)
        mr=np.where(mr==mr.max())
        mr1=int(mr[0][0])
        mr2=int(mr[0][1])
        print('\n',num,'. Номера кластеров с максимальным расстоянием:',mr1+1,mr2+1)
        
        for i in range (0,obj):
            if ((m_rasst[mr1,i]!=0) and (m_rasst[mr2,i]!=0)):
                m_rasst[mr1,i]=np.maximum(m_rasst[mr1,i],m_rasst[mr2,i])
            if ((m_rasst[i,mr1]!=0) and (m_rasst[i,mr2]!=0)):
                m_rasst[i,mr1]=np.maximum(m_rasst[mr1,i],m_rasst[mr2,i])
                
    clasters[mr1].append(clasters[mr2])
    del clasters[mr2]
    
    m_rasst=np.delete(m_rasst,mr2,0)
    m_rasst=np.delete(m_rasst,mr2,1)
    obj=obj-1
    
    print('\nМатрица расстояний:\n',m_rasst,'\n\n')
    
    for i in range (0,len(clasters)):
        print('Кластер',i+1,clasters[i])
print('\nКластеры найдены')
