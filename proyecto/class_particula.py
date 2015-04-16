# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-
#%matplotlib inline

class Particula:
    
    """
    Simula el movimiento de una partícula con atributos:
    -posicion: Es una lista o arreglo de posiciones iniciales [pos_x, pos_y] (números flotantes)
    -velocidad: Es una lista o arrgelo de velocidades iniciales [vel_x, vel_y] (números flotantes)
    -masa: Es una magintud (flotante)
    """
    
    def __init__(self, posicion, velocidad, masa):
        self.masa = masa
        
        self.posicion_0 = posicion
        self.posicion_x_0 = self.posicion_0[0]
        self.posicion_y_0 = self.posicion_0[1]
        
        self.velocidad_0 = velocidad
        self.velocidad_x_0 = self.velocidad_0[0]
        self.velocidad_y_0 = self.velocidad_0[1]
        
        self.G = 6.67384e-11
 
    def mover(self, fuerza, tiempo, pasos):
        
        """
        La simulación per sé. Atributos:
        -fuerza: Una lista o arreglo [fuerza_x, fuerza_y]
        -tiempo: Una magnitud de tiempo
        -pasos: En cuántos intervalos se dividirá el tiempo (se recomiendan 100)
        
        Funcionamiento:
        Se divide el tiempo en pasos subintervalos. Para cada subintervalo se calcula la posición y la velocidad final conforme
        a la aceleración.
        Nota: los pasos definen mejor la trayectoria que dibuja la partícula.
        """
        
        self.pasos = pasos
        self.tiempo = np.array([(i+1)*(tiempo/self.pasos) for i in range(self.pasos)])
        
        self.aceleracion_x = fuerza[0] / self.masa
        self.aceleracion_y = fuerza[1] / self.masa
        
        self.velocidades = np.zeros([pasos,2])
        self.velocidad_x = self.velocidades[:,0]
        self.velocidad_y = self.velocidades[:,1]
        
        self.velocidad_x[0] = self.velocidad_x_0
        self.velocidad_y[0] = self.velocidad_y_0
        
        self.posiciones = np.zeros([pasos,2])
        self.posicion_x = self.posiciones[:,0]
        self.posicion_y = self.posiciones[:,1]
        
        self.posicion_x[0] = self.posicion_x_0
        self.posicion_y[0] = self.posicion_y_0
        
        
        for i in range(self.pasos - 1):
            self.velocidad_x[i+1] = self.velocidad_x[0] + self.tiempo[i] * self.aceleracion_x
            self.posicion_x[i+1] = self.velocidad_x[0] * self.tiempo[i] + (0.5) * self.aceleracion_x * (self.tiempo[i])**2 + self.posicion_x[0]
            
            self.velocidad_y[i+1] = self.velocidad_y[0] + self.tiempo[i] * self.aceleracion_y
            self.posicion_y[i+1] = self.velocidad_y[0] * self.tiempo[i] + (0.5) * self.aceleracion_y * (self.tiempo[i])**2 + self.posicion_y[0]
    
    def dibujar(self):
        
        """
        Dibuja la partícula tras emplear el método mover.
        """
        
        plt.figure(figsize = (10,8), dpi = 80)
        
        scatter_x = []
        scatter_y = []
        for i in range(0, len(self.posicion_x), 100):
            scatter_x.append(self.posicion_x[i])
            scatter_y.append(self.posicion_y[i])
        
        scatter_x.append(self.posicion_x[len(self.posicion_x)-1])
        scatter_y.append(self.posicion_y[len(self.posicion_y)-1])
        
        plt.plot(self.posicion_x, self.posicion_y , label="Movimiento", color="blue", linewidth = 1)
        plt.scatter(scatter_x, scatter_y, 30,  label = "Movimiento puntual", color = 'r')
        plt.ylabel("Posicion Y (m)")
        plt.xlabel("Posicion X (m)")
        plt.legend(loc = 'best')
        
        
    def dibujar_x_tiempo(self): 
        
        """
        Dibuja la posición X contra el tiempo t tras emplear el método mover.
        """
        
        plt.figure(figsize = (10,8), dpi = 80)
        plt.plot(self.tiempo, self.posicion_x , label=u"Posición X vs Tiempo", color="red")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Posicion X (m)")
        plt.legend(loc = 'best')
    
    def dibujar_y_tiempo(self):
        
        """
        Dibuja la posición Y contra el tiempo t tras emplear el método mover.
        """
        
        plt.figure(figsize = (10,8), dpi = 80)
        plt.plot(self.tiempo, self.posicion_y , label=u"Posición Y vs Tiempo", color="red")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Posicion Y (m)")
        plt.legend(loc = 'best')
        
        
    def distancia(self, otra_particula):
        self.norma = np.linalg.norm(self.posicion_0 - otra_particula.posicion_0) # Interesa sólo la posición inicial
        self.vector_unitario = (self.posicion_0 - otra_particula.posicion_0)/self.norma
        
        return (self.norma, self.vector_unitario) # La distancia regresa la norma entre las dos posiciones y su vector unitario
    

    def fuerzaAplicada(self, otra_particula):
        d, vector_u = self.distancia(otra_particula)
        fuerza_gravitacional = (1/d) * vector_u * self.G * self.masa * otra_particula.masa
        return fuerza_gravitacional