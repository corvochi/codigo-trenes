#!/usr/bin/env python
# coding: utf-8

# In[80]:


import matplotlib.pyplot as plt
import numpy as np
import random as rn
import math
import pandas as pd
import time


# In[81]:


#-------------------------------Tasa------------------------
path = 'Tasa.xlsx'
df = pd.read_excel(path, 
            sheet_name='Tasa 0,5', 
            header = None, 
            names = ['Hora Salida', 'Salida SA', 'E.Salida', 'ID', 'Servicio', 'F.LIM', 'F.SA', 'LIM','PEN','SGA','VAM','CON','AME','BTO','SOL','QUI','SLT','CHO','HOS','VIN','MIR','REC','POR','BAR','FRA','BEL','PUE', 'CAPACIDAD'])

Tasas = df.values.tolist()

#-------------------------------Sistema------------------------
ID = [fila[2] for fila in Tasas]
Sistema = []

for i in range(len(ID)):
    Sistema.append([0]*27)

for z in range(len(ID)):
    for y in range (7):
        Sistema[z][y] = Tasas[z][y]
        
for z in range(2):
    for y in range(0,27):
        Sistema[z][y] = Tasas[z][y]

for z in range(1,len(ID)):
    Sistema[z][6] = round(Tasas[z][6]*Tasas[z][4],1)
        
def impresion ():      
    b="" 
    for z in range(len(ID)-85):
        for y in range (0,15):
            b+=str(Tasas[z][y])+'\t'
        print (b)
        b=""
print ('')

#-------------------------------Alertas y excesos------------------------
Alertas = []
Excesos = []
n_estaciones = 20 
for i in range(len(ID)):
    Alertas.append([0]*n_estaciones)
    Excesos.append([0]*n_estaciones)
    
for z in range(len(ID)):
    for y in range (n_estaciones):
        if z==0:
            Alertas[z][y] = Sistema[z][y+6]
            Excesos[z][y] = Sistema[z][y+6]
        else:
            Alertas[z][y] = 0
            Excesos[z][y] = 0
    
def impresionA (Alertas):      
    b="" 
    for z in range(len(ID)-85):
        for y in range (0,n_estaciones):
            b+=str(Alertas[z][y])+'\t'
        print (b)
        b=""


def impresionE ():
    c="" 
    for z in range(len(ID)-85):
        for y in range (0,14):
            c+=str(Excesos[z][y])+'\t'
        print (c)
        c=""


#---------------------------Otros parámetros---------------------------
maquinistas = 50
trenes = 35
Tdetencion = 20
Ckwhkm = 328
Cmantencion = 580
alerta = []
#frecuencia: mayor o igual a 6 y menor o igual a 12
frecuencia = 0
#Servicio: simple o múltiple
Servicio = []


# In[82]:


def diagnóstico (n_estaciones, Sistema, Alertas, Tasas, ID, Excesos):

    #Usar el timmer para ir activando los trenes
    #con la frecuencia puedo estimar la gente que habrá en la estación (check)
    #calculo si me da o no con la capacidad que tengo (check)
    #genero alerta (check)
    #se genera planificación
    contador = 0
    Qpasajeros = 0
    demanda = 0
    Alertas2 = Alertas.copy()
    for z in range(2,len(ID)):
        for y in range(6,26):
            E = 0
            exceso = 0
            sistema = 0
            capacidad = Tasas [z][3]
            
            if (y == 6 or y == 7): #Si está en Limache o en peñablanca, significa que la demanda será sin tasa en LIM y con tasa 5
                if(y==6):
                    demanda = Sistema[z][y]
                    #sistema = 0
                    E = 0
                else:
                    demanda = Tasas[z][y]*Tasas[z][4]
                    #sistema = Sistema[z][y-1]
                    E = Excesos[z-1][y-6]
            else:
                demanda = Tasas[z][y]*Tasas[z][5] + E
                E = Excesos[z-1][y-6]
            
            
            exceso = (demanda + E)/capacidad

            Excesos[z][y-6] = round((sistema + demanda + E) - capacidad,1)
            if Excesos[z][y-6] < 0:
                Excesos[z][y-6] = 0
            
            
            if exceso > 1.1:
                #print (z,'\tAlerta en estación\t',Tasas[0][y], '\tID Servicio:\t', Tasas [z][2], ' \tExceso en  :\t',demanda-capacidad, '\tpasajeros',' Exceso anterior: ',E)
                Alertas[z][y-6] = 1
                contador += 1
                Qpasajeros += demanda-capacidad - E
    
    impresionE()
    print ('alertas: ',contador)
    #print ('Qpasajeros: ',Qpasajeros, 'pasaje promedio: 500', 'total: $',Qpasajeros*500)
    return Alertas, contador
#diagnóstico (n_estaciones, Sistema, Alertas, Tasas, ID, Excesos)


# In[83]:


def sumaalertas (Alertas, ID, ser, est):

    suma = 0
    print ("Alertas")
    for z in range(ser+2,len(ID)):
        for y in range(est,n_estaciones-1):
            #print (Alertas[z][y])
            suma = suma + Alertas[z][y] 
    return suma
    
    
def vecindario (n_estaciones, Sistema, Alertas, Tasas, ID, Excesos, contador):
    frecuencias = [6, 9]
    frecuencias2 = [3, 6, 9]
    capacidades = [370, 740]
    ser  = 1
    est  = 0
              
    print (ser, est)
    suma = 0
    for z in range(ser+2,len(ID)):
        for y in range(est,n_estaciones-1):
            suma = suma + Alertas[z][y] 
    print ('1: ',suma)
    f=0
    f2=0
    c2 = 0
    while contador > 10:
        c2+=1
        print ("c2: ",c2)
        f = rn.choice(frecuencias)
        f2 = rn.choice(frecuencias2)
        for z in range(ser+2,len(ID)):
            for y in range(0,n_estaciones-1):
                if y==2:
                    Tasas[z][4] = f
                    Tasas[z][5] = f2
                else:
                    Tasas[z][5] = f2

                Tasas[z][3] = rn.choice(capacidades)
        
        Alertas, contador = diagnóstico (n_estaciones, Sistema, Alertas, Tasas, ID, Excesos)
    print ('f: ',f, ' f2: ',f2)  
    return contador, Alertas, Tasas
    


# In[84]:


#Función objetivo
#CT = len(ID) * (mantencion + kilometraje)


# In[85]:


def MAIN (n_estaciones, Sistema, Alertas, Tasas, ID, Excesos):

    Alertas2, contador = diagnóstico (n_estaciones, Sistema, Alertas, Tasas, ID, Excesos)
    contador, Alertas, Tasas = vecindario (n_estaciones, Sistema, Alertas2, Tasas, ID, Excesos, contador)
    impresionE ()
    impresion()


# In[86]:


MAIN (n_estaciones, Sistema, Alertas, Tasas, ID, Excesos)


# In[ ]:





# In[ ]:




