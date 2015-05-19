
# -*- coding: utf-8 -*-
#%pylab inline
from __future__ import division
from JSAnimation import IPython_display
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import mpl_toolkits.mplot3d.axes3d as a3d
# -*- coding: utf-8 -*-

class leer_universo:
    
    def __init__(self, metodo, archivo, tresd):
        """
        Clase para leer archivo del universo
        """
        self.metodo = metodo #El método siempre es Particula
        self.archivo = archivo #Nombre del archivo
        self.tresd = tresd #True o false
        
    def cargar_datos(self):
        configuracion_universo = []
        archivo_universo = open(self.archivo, 'r')
        #Se lee cada línea del archivo y cada dato de guarda como float en una lista
        for linea in archivo_universo.readlines():
            for i in range(len(linea.split())):
                configuracion_universo.append(float(linea.split()[i]))

        archivo_universo.close() #Se cierra el archivo
        
        return configuracion_universo
    
    def obtener_datos(self):
        universo = self.cargar_datos()
        numero_particulas = int(universo[0])
        radio_universo = universo[1]
        lista_particulas = []
        contador = 2
        #Caso 2D...
        if self.tresd == False:
            for particula in range(numero_particulas):
                #Se iniciliza cada partícula y se agrega a una lista
                particula_aux = self.metodo(posicion = universo[contador:contador+2],
                                          velocidad = universo[contador+2:contador+4],
                                          masa = universo[contador+4])
                lista_particulas.append(particula_aux)
                contador += 5
        #Caso 3D..
        else: 
            for particula in range(numero_particulas):
                #Se inicializa en cada partícula y se agrega a una lista
                particula_aux = self.metodo(posicion = universo[contador:contador+3],
                                          velocidad = universo[contador+3:contador+6],
                                          masa = universo[contador+6])
                lista_particulas.append(particula_aux)
                contador += 7
        
        return numero_particulas, radio_universo, lista_particulas
            
        