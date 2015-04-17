
# -*- coding: utf-8 -*-
#%matplotlib inline

import numpy as np
import matplotlib.pyplot as plt

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
        
        self.velocidad_0 = velocidad

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
        
        lis_aux = [0]
        for i in range(self.pasos):
            lis_aux.append((i+1)*(tiempo/self.pasos))
            
        self.tiempo = np.array(lis_aux)
        
        self.aceleracion_x = fuerza[0] / self.masa
        self.aceleracion_y = fuerza[1] / self.masa
        
        self.velocidades = np.zeros([self.pasos + 1,2])
        self.velocidad_x = self.velocidades[:,0]
        self.velocidad_y = self.velocidades[:,1]
        
        self.velocidad_x[0] = self.velocidad_0[0]
        self.velocidad_y[0] = self.velocidad_0[1]
        
        self.posiciones = np.zeros([self.pasos + 1,2])
        self.posicion_x = self.posiciones[:,0]
        self.posicion_y = self.posiciones[:,1]
        
        self.posicion_x[0] = self.posicion_0[0]
        self.posicion_y[0] = self.posicion_0[1]
        
        
        for i in range(self.pasos):
            self.velocidad_x[i+1] = self.velocidad_x[0] + self.tiempo[i+1] * self.aceleracion_x
            self.posicion_x[i+1] = self.velocidad_x[0] * self.tiempo[i+1] + (0.5) * self.aceleracion_x * (self.tiempo[i+1])**2 + self.posicion_x[0]
              
            self.velocidad_y[i+1] = self.velocidad_y[0] + self.tiempo[i+1] * self.aceleracion_y
            self.posicion_y[i+1] = self.velocidad_y[0] * self.tiempo[i+1] + (0.5) * self.aceleracion_y * (self.tiempo[i+1])**2 + self.posicion_y[0]
            
    
    def dibujar(self):
        
        """
        Dibuja la partícula tras emplear el método mover.
        """
        
        plt.figure(figsize = (10,8), dpi = 80)
        
        scatter_x = []
        scatter_y = []
        if int(np.ceil(len(self.posicion_x)/10)) > 0:
            for i in range(0, len(self.posicion_x), int(np.ceil(len(self.posicion_x)/10))):
                scatter_x.append(self.posicion_x[i])
                scatter_y.append(self.posicion_y[i])
        else:
            for i in range(0, len(self.posicion_x)):
                scatter_x.append(self.posicion_x[i])
                scatter_y.append(self.posicion_y[i])
            
        
        scatter_x.append(self.posicion_x[len(self.posicion_x)-1])
        scatter_y.append(self.posicion_y[len(self.posicion_y)-1])
        
        plt.title(u"Posición Y vs Posición X", fontsize = 20)
        plt.plot(self.posicion_x, self.posicion_y , label="Movimiento", color="blue", linewidth = 1)
        plt.scatter(scatter_x, scatter_y, 30,  label = "Movimiento puntual", color = 'r')
        plt.plot(scatter_x[0], scatter_y[0], 'ko', label = "Pos inicial" )
        plt.plot(scatter_x[len(scatter_x)-1], scatter_y[len(scatter_y)-1], 'co', label = "Pos final" )
        plt.ylabel("Posicion Y (m)")
        plt.xlabel("Posicion X (m)")
        plt.legend(loc = 'best')

    def dibujar_xt_yt(self):
        
        """
        Dibuja:
        1) Posición Y vs Posición X
        2) Posición X vs Tiempo
        3) Posición Y vs tiempo
        """
        
        fig, ax = plt.subplots(1,3, figsize = (19,5), dpi = 80)
        
        scatter_x = []
        scatter_y = []
        scatter_tiempo = []
        
        if int(np.ceil(len(self.posicion_x)/10)) > 0:
            for i in range(0, len(self.posicion_x), int(np.ceil(len(self.posicion_x)/10))):
                scatter_x.append(self.posicion_x[i])
                scatter_y.append(self.posicion_y[i])
                scatter_tiempo.append(self.tiempo[i])
        else:
            for i in range(0, len(self.posicion_x)):
                scatter_x.append(self.posicion_x[i])
                scatter_y.append(self.posicion_y[i])
                scatter_tiempo.append(self.tiempo[i])
        
        scatter_x.append(self.posicion_x[len(self.posicion_x)-1])
        scatter_y.append(self.posicion_y[len(self.posicion_y)-1])
        scatter_tiempo.append(self.tiempo[len(self.tiempo)-1])
        
        ax[0].set_title(u"Posición Y vs Posición X", fontsize = 20)
        ax[0].plot(self.posicion_x, self.posicion_y , label="Movimiento", color="blue", linewidth = 1)
        ax[0].scatter(scatter_x, scatter_y, 30,  label = "Movimiento puntual", color = 'r')
        ax[0].plot(scatter_x[0], scatter_y[0], 'ko', label = "Pos inicial" )
        ax[0].plot(scatter_x[len(scatter_x)-1], scatter_y[len(scatter_y)-1], 'co', label = "Pos final" )
        ax[0].set_ylabel("Posicion Y (m)")
        ax[0].set_xlabel("Posicion X (m)")
        ax[0].legend(loc = 'best')
        
        ax[1].set_title(u"Posición X vs Tiempo", fontsize = 20)
        ax[1].plot(self.tiempo, self.posicion_x , label=u"Movimiento uniforme", color='c')
        ax[1].scatter(scatter_tiempo, scatter_x, 30,  label = "Movimiento puntual", color = 'm')
        ax[1].plot(scatter_tiempo[0], scatter_x[0], 'ko', label = "Pos inicial" )
        ax[1].plot(scatter_tiempo[len(scatter_tiempo)-1], scatter_x[len(scatter_x)-1], 'yo', label = "Pos final" )
        ax[1].set_xlabel("Tiempo (s)")
        ax[1].set_ylabel("Posicion X (m)")
        ax[1].legend(loc = 'best')
        
        ax[2].set_title(u"Posición Y vs Tiempo", fontsize = 20)
        ax[2].plot(self.tiempo, self.posicion_y , label=u"Movimiento uniforme", color='g')
        ax[2].scatter(scatter_tiempo, scatter_y, 30,  label = "Movimiento puntual", color = 'k')
        ax[2].plot(scatter_tiempo[0], scatter_y[0], 'ro', label = "Pos inicial" )
        ax[2].plot(scatter_tiempo[len(scatter_tiempo)-1], scatter_y[len(scatter_y)-1], 'bo', label = "Pos final" )
        ax[2].set_xlabel("Tiempo (s)")
        ax[2].set_ylabel("Posicion Y (m)")
        ax[2].legend(loc = 'best')
    
    def mover_muchas_fuerzas(self, tiempos, fuerzas, paso):
        
        """
        -Tiempos es un vector de tiempos [[tiempo inicial, tiempo final], []]
        -Fuerzas es un vector de fuerzas
        -Paso es un vector de pasos
        En el lapso de tiempo i se aplicará la fuerza i con un número de p = paso
        con el método mover definido arriba.
        """
        
        self.pos_x = []
        self.pos_y = []
        self.fuerzas = fuerzas
        self.paso = paso
    
        
        for i in range(len(fuerzas)):
            dt = tiempos[i][1] - tiempos[i][0]
            self.mover(fuerzas[i], dt, paso[i])
            self.posicion_0 = [self.posicion_x[self.pasos], self.posicion_y[self.pasos]]
            self.velocidad_0 = [self.velocidad_x[self.pasos], self.velocidad_y[self.pasos]]
            self.pos_x.append(self.posicion_x)
            self.pos_y.append(self.posicion_y)
    
    
    def dibujar_muchas_fuerzas(self):
        
        """
        Dibuja lo hecho por el método muchas_fuerzas()
        """
        
        fig, ax = plt.subplots(1,2, figsize = (15,7), dpi = 80)
        
        ax[0].set_title("%d Fuerzas" % len(self.fuerzas), fontsize = 20)
        ax[0].set_ylabel("Posicion Y (m)")
        ax[0].set_xlabel("Posicion X (m)")
        
        for i in range(len(self.fuerzas)):
            ax[0].plot(self.pos_x[i], self.pos_y[i], label = "Fuerza %d" % (i+1), color = np.random.rand(4), linewidth = 2)
            ax[0].scatter(self.pos_x[i][0], self.pos_y[i][0], 30, color =  'r')
            
        ax[0].scatter(self.pos_x[0][0], self.pos_y[0][0], 40, label = "Pos inicial", c = 'b')
        ax[0].scatter(self.pos_x[len(self.fuerzas)-1][self.paso[len(self.fuerzas)-1]-1], 
                    self.pos_y[len(self.fuerzas)-1][self.paso[len(self.fuerzas)-1]-1], 
                    40,  label = "Pos final", c = 'k')
        
        ax[0].legend(loc="best")
        
        
        ax[1].set_title("Movimiento continuo", fontsize = 20)
        ax[1].set_ylabel("Posicion Y (m)")
        ax[1].set_xlabel("Posicion X (m)")
        
        for i in range(len(self.fuerzas)):
            ax[1].plot(self.pos_x[i], self.pos_y[i], color = 'g', linewidth = 1.5)
            
        ax[1].scatter(self.pos_x[0][0], self.pos_y[0][0], 40, label = "Pos inicial", c = 'b')
        ax[1].scatter(self.pos_x[len(self.fuerzas)-1][self.paso[len(self.fuerzas)-1]-1], 
                    self.pos_y[len(self.fuerzas)-1][self.paso[len(self.fuerzas)-1]-1], 
                    40,  label = "Pos final", c = 'r')
        
        ax[1].legend(loc="best")
               
    def distancia(self, otra_particula):
        self.norma = np.linalg.norm(self.posicion_0 - otra_particula.posicion_0) # Interesa sólo la posición inicial
        self.vector_unitario = (self.posicion_0 - otra_particula.posicion_0)/self.norma
        
        return (self.norma, self.vector_unitario) # La distancia regresa la norma entre las dos posiciones y su vector unitario
    

    def fuerzaAplicada(self, otra_particula):
        d, vector_u = self.distancia(otra_particula)
        if d == 0:
            return np.array([0.0, 0.0])
        else:
            fuerza_gravitacional = (1/d) * vector_u * self.G * self.masa * otra_particula.masa
            return fuerza_gravitacional