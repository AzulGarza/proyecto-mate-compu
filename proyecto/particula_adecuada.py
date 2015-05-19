
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


class Particula:
    #OBSERVACION: Muchos de los métodos empleados (sobre todo los gráficos) toman su base en los vistos en clase
    #y en los notebooks.
    def __init__(self, posicion, velocidad, masa):
        """
        Atributos:
        -posicion: Es una lista o arreglo de posiciones iniciales [pos_x, pos_y] (números flotantes)
        -velocidad: Es una lista o arrgelo de velocidades iniciales [vel_x, vel_y] (números flotantes)
        -masa: Es una magintud (flotante)
        """
        #Inicialización de la partícula
        self.posicion_0 = posicion
        self.velocidad_0 = velocidad
        self.masa = masa
        #Se define la posición  y la velocidad actual de la partícula
        self.posicion_actual = self.posicion_0
        self.velocidad_actual = self.velocidad_0
        #Lista de posiciones que acumulará las posiciones de la paricula según se mueva
        #Se inicializan las listas de posiciones con la posición inicial
        self.posicion_x = [self.posicion_0[0]]
        self.posicion_y = [self.posicion_0[1]]
        #Lista de velocidades que acumulará las velocidades de la partícula según se mueva
        #Se inicializan las listas de velocidades con la velocidad inicial 
        self.velocidad_x = [self.velocidad_0[0]]
        self.velocidad_y = [self.velocidad_0[0]]
        #Lista de tiempos que nos ayudará a llevar el conteo del tiempo
        #Se inicializa en 0
        self.tiempo = [0]
        #Lleva la cuenta del número de veces que se ha movido la partícula
        self.movimientos = 0
        #Listas de posiciones y tiempo que nos ayudarán a visualizar el movimiento de la partícula en un rango de tiempo
        self.scatter_x = []
        self.scatter_y = []
        self.scatter_tiempo = []
        #Implementando 3D
        #Switch 3D
        self.tres_d = False
        if len(posicion) == 3: #Si se da un vector de 3 posiciones, se asume que se trabajará en 3D
            self.tres_d = True
            #Se crea el eje z
            self.posicion_z = [self.posicion_0[2]]
            self.velocidad_z = [self.velocidad_0[2]]
            self.scatter_z = []
        #Switch para detener la partícula en cualquier punto
        self.detener = False
        #Constante de gravitación universal
        self.G = 6.67384e-11
         
    def distancia(self, otra_particula):
        """
        Devuelve un vector de dos entradas: a) la distancia entre dos partículas, b) el vector unitario entre dos partículas
        """
        #Cálculo de la distancia o norma entre dos partículas (es fácil con numpy) a partir de su `posicion_actual`
        self.norma = np.linalg.norm(np.array(otra_particula.posicion_actual) - np.array(self.posicion_actual))
        #Cálculo del vector unitario entre dos partículas (dividimos la resta de sus posiciones entre la norma de la resta)
        self.vector_unitario = (np.array(otra_particula.posicion_actual) - np.array(self.posicion_actual))/self.norma
        
        return (self.norma, self.vector_unitario) # La distancia regresa la norma entre las dos posiciones y su vector unitario
    

    def fuerzaAplicada(self, otra_particula):
        """
        Calcula la fuerza que ejerce otra partícula sobre esta partícula.
        """
        #Se toma la distancia y el vector unitario calculados en el método 'distancia'
        d, vector_u = self.distancia(otra_particula)
        #Si la distancia se anula, la fuerza es cero
        if d == 0:
            #Se considera el caso cuando se trabaja en tercera dimensión
            if self.tres_d == False:
                return np.array([0., 0.])
            else:
                return np.array([0., 0., 0.])
        #Si la distancia no se anula, calculamos la fuerza ejercia a partir de la Ley de Gravitación Universal newtoniana
        else:
            #No se considera el caso donde se trabaja en tercera dimensión pues `vector_u` reconoce la dimensión
            fuerza_gravitacional = (1./d) * vector_u * self.G * self.masa * otra_particula.masa
            return fuerza_gravitacional    
 
    def mover(self, fuerza, tiempo, pasos):
        """
        La simulación per sé. Atributos:
        -fuerza: Una lista o arreglo [fuerza_x, fuerza_y]
        -tiempo: Una magnitud de tiempo
        -pasos: En cuántos intervalos se dividirá el tiempo (se recomiendan al menos 100)
        
        Funcionamiento:
        Se divide el tiempo en `pasos` subintervalos. 
        Para cada subintervalo se calcula la posición y la velocidad final conforme
        a la aceleración.
        Nota: los pasos definen mejor la trayectoria que dibuja la partícula.
        """
        self.pasos = pasos
        #Lista auxiliar de tiempos que nos ayudará a calcular las posiciones en cada subintervalo
        tiempo_aux = [0]
        #Llenamos la lista de tiempos auxiliar con el `tiempo` dividio en `pasos`
        for i in range(self.pasos):
            tiempo_aux.append((i+1)*(tiempo/self.pasos))
            #La lista "oficial"  de tiempos se rellena también y se le añade el tiempo transcurrido tras el último empleo
            #del método 'mover'
            self.tiempo.append((i+1)*(tiempo/self.pasos) + self.tiempo[self.movimientos]) 
        #A partir de las ecuaciones de movimiento calculamos las aceleraciones a lo largo de los ejes
        self.aceleracion_x = fuerza[0] / self.masa
        self.aceleracion_y = fuerza[1] / self.masa
        #Se considera el caso tercerdimensional
        if self.tres_d == True:
            self.aceleracion_z = fuerza[2] / self.masa
        #Si la partícula no se ha detenido...
        if self.detener == False:
            #A partir de las ecuaciones de movimiento se determinan las velocidades y las posiciones para cada paso
            for i in range(self.pasos):
                #Se considera como velocidad inicial la última que lleva la partícula
                self.velocidad_x.append(self.velocidad_actual[0] + tiempo_aux[i+1] * self.aceleracion_x)
                self.velocidad_y.append(self.velocidad_actual[1] + tiempo_aux[i+1] * self.aceleracion_y)
                #Se considera como posicion inicial la última que lleva la partícula
                self.posicion_x.append(self.velocidad_actual[0] * tiempo_aux[i+1] 
                                       + (0.5) * self.aceleracion_x * (tiempo_aux[i+1])**2
                                       + self.posicion_actual[0])
                self.posicion_y.append(self.velocidad_actual[1] * tiempo_aux[i+1] 
                                       + (0.5) * self.aceleracion_y * (tiempo_aux[i+1])**2
                                       + self.posicion_actual[1])
                #Caso 3D
                if self.tres_d == True:
                    self.velocidad_z.append(self.velocidad_actual[2] + tiempo_aux[i+1] * self.aceleracion_z)
                    self.posicion_z.append(self.velocidad_actual[2] * tiempo_aux[i+1] 
                                       + (0.5) * self.aceleracion_z * (tiempo_aux[i+1])**2
                                       + self.posicion_actual[2])
        #Si la partícula se detiene, para cada paso, la particula se queda en la misma posición
        #y la velocidad se anula
        else:
            for i in range(self.pasos):
                self.velocidad_actual[0] = 0
                self.velocidad_actual[1] = 0
                self.velocidad_x.append(self.velocidad_actual[0])
                self.velocidad_y.append(self.velocidad_actual[1])
                self.posicion_x.append(self.posicion_actual[0])
                self.posicion_y.append(self.posicion_actual[1])
                #Caso 3D...
                if self.tres_d == True:
                    self.velocidad_actual[2]
                    self.velocidad_z.append(self.velocidad_actual[2])
                    self.posicion_z.append(self.posicion_actual[2])         
        #El número de movimientos aumenta en `pasos` veces
        self.movimientos += self.pasos
        #Se actualizan las velocidades y las posiciones actuales
        self.velocidad_actual[0] = self.velocidad_x[self.movimientos]
        self.velocidad_actual[1] = self.velocidad_y[self.movimientos]
        self.posicion_actual[0] = self.posicion_x[self.movimientos]
        self.posicion_actual[1] = self.posicion_y[self.movimientos]
        #Caso  3D...
        if self.tres_d == True:
            self.velocidad_actual[2] = self.velocidad_z[self.movimientos]
            self.posicion_actual[2] = self.posicion_z[self.movimientos]
        
    def movimiento_puntual(self): 
        """
        Divide el movimiento de la partícula en 10 intervalos para apreciar mejor cómo acelera.
        Útil para graficar.
        """
        #Se reinician las siguientes listas para no tener problemas de reasignación
        self.scatter_x = []
        self.scatter_y = []
        self.scatter_tiempo = []
        #Caso 3D...
        if self.tres_d ==True:
            self.scatter_z = []
        #Dividimos la longitud de la lista de las posiciones (puede ser cualquiera, tienen la misma longitud)
        #entre 10
        #Si el entero más cercano a esta razón es positivo (no cero), las listas `scatter` se llenan 
        #tomando las listas del movimiento continuo en lapsos de esta relación
        if int(np.ceil(len(self.posicion_x)/10)) > 0:
            for i in range(0, len(self.posicion_x), int(np.ceil(len(self.posicion_x)/10))):
                self.scatter_x.append(self.posicion_x[i])
                self.scatter_y.append(self.posicion_y[i])
                self.scatter_tiempo.append(self.tiempo[i])
                #Caso 3D...
                if self.tres_d == True:
                    self.scatter_z.append(self.posicion_z[i])
        #Si no, se toma 1 como lapso
        else:
            for i in range(len(self.posicion_x)):
                self.scatter_x.append(self.posicion_x[i])
                self.scatter_y.append(self.posicion_y[i])
                self.scatter_tiempo.append(self.tiempo[i])
                #Caso 3D...
                if self.tres_d == True:
                    self.scatter_z.append(self.posicion_z[i])
        #Se añaden además las posiciones actuales finales 
        self.scatter_x.append(self.posicion_actual[0])
        self.scatter_y.append(self.posicion_actual[1])
        self.scatter_tiempo.append(self.tiempo[len(self.tiempo)-1])
        if self.tres_d == True:
            self.scatter_z.append(self.posicion_actual[2])
        
    def dibujar(self):
        """
        Dibuja la partícula tras emplear el método mover.
        """
        #Primero aplicamos el método 'movimiento puntual' para obtener el movimiento puntual de la partícula
        self.movimiento_puntual()
        #Caso 2D...
        if self.tres_d == False:
            fig = plt.figure(figsize = (6,6), dpi = 80)
            fig.suptitle(u"Posición Y vs Posición X", fontsize = 14, fontweight = 'bold')
            ax = fig.gca()
            #Graficamos el "movimiento continuo", variables `posicion_x` y `posicion_y`
            ax.plot(self.posicion_x,
                    self.posicion_y,
                    label="Movimiento", color="blue", linewidth = 1)
            #Graficamos el "movimiento puntual"
            ax.scatter(self.scatter_x,
                       self.scatter_y,
                       30,  label = "Movimiento puntual", color = 'r')
            #Marcamos la posición inicial
            ax.plot(self.scatter_x[0],
                    self.scatter_y[0],
                    'ko', label = "Pos inicial" )
            #Marcamos la posición final
            ax.plot(self.scatter_x[len(self.scatter_x)-1],
                    self.scatter_y[len(self.scatter_y)-1],
                    'co', label = "Pos final" )
            
            ax.set_ylabel(u"Posición Y (m)")
            ax.set_xlabel(u"Posición X (m)")
            
            ax.legend(loc = 'best')
        #Caso 3D...    
        else:
            fig = plt.figure(figsize = (6, 6), dpi = 80)
            fig.suptitle(u"Posición Z vs Y vs X", fontsize=14, fontweight='bold')
            ax = fig.gca(projection='3d')
            #Graficamos el "movimiento continuo"
            ax.plot(self.posicion_x, 
                    self.posicion_y,
                    self.posicion_z,
                    label='Movimiento', color = 'b', linewidth = 1)
            #Graficamos el "movimiento puntual"
            ax.scatter(self.scatter_x, 
                       self.scatter_y,
                       self.scatter_z, 
                       label = "Movimiento puntual", color = 'r')
            #Graficamos la posición inicial
            ax.scatter(self.scatter_x[0],
                       self.scatter_y[0],
                       self.scatter_z[0],
                       marker = '^', label = "Pos inicial", color = 'black')
            #Graficamos la posición final
            ax.scatter(self.scatter_x[len(self.scatter_x)-1],
                       self.scatter_y[len(self.scatter_y)-1], 
                       self.scatter_z[len(self.scatter_z)-1],
                       marker = '^', label = "Pos final", color = 'm')
            
            ax.set_xlabel(u'Posición X (m)')
            ax.set_ylabel(u'Posición Y (m)')
            ax.set_zlabel(u'Posición Z (m)')
            
            ax.legend(loc = 'best')

    def dibujar_contra_tiempo(self):
        """
        Para 2D dibuja:
        1) Posición Y vs Posición X
        2) Posición X vs Tiempo
        3) Posición Y vs Tiempo
        
        Para 3D dibuja
        1) Posición X vs Tiempo
        2) Posición Y vs Tiempo
        3) Posición Z vs Tiempo
        """
        #Primero aplicamos el método 'movimiento puntual' para obtener el movimiento puntual de la partícula
        self.movimiento_puntual()
        #Caso 2D...
        if self.tres_d == False:
            fig, ax = plt.subplots(1,3, figsize = (19,5), dpi = 80)
            #Posición Y vs Posición X
            ax[0].set_title(u"Posición Y vs Posición X", fontsize = 20) 
            ax[0].plot(self.posicion_x, #Movimiento continuo
                       self.posicion_y,
                       label="Movimiento", color="blue", linewidth = 1) 
            ax[0].scatter(self.scatter_x, #Movimiento puntual
                          self.scatter_y,
                          30,  label = "Movimiento puntual", color = 'r')
            ax[0].plot(self.scatter_x[0], #Posición inicial
                       self.scatter_y[0],
                       'ko', label = "Pos inicial" )
            ax[0].plot(self.scatter_x[len(self.scatter_x)-1], #Posición final
                       self.scatter_y[len(self.scatter_y)-1],
                       'co', label = "Pos final" )
            ax[0].set_ylabel("Posicion Y (m)")
            ax[0].set_xlabel("Posicion X (m)")
            ax[0].legend(loc = 'best')
            #Posición X vs Tiempo
            ax[1].set_title(u"Posición X vs Tiempo", fontsize = 20)
            ax[1].plot(self.tiempo, #Movimiento continuo
                       self.posicion_x,
                       label=u"Movimiento uniforme", color='c')
            ax[1].scatter(self.scatter_tiempo, #Movimiento puntual
                          self.scatter_x,
                          30,  label = "Movimiento puntual", color = 'm')
            ax[1].plot(self.scatter_tiempo[0], #Posición inicial
                       self.scatter_x[0],
                       'ko', label = "Pos inicial")
            ax[1].plot(self.scatter_tiempo[len(self.scatter_tiempo)-1], #Posición final
                       self.scatter_x[len(self.scatter_x)-1], 
                       'yo', label = "Pos final")
            ax[1].set_xlabel("Tiempo (s)")
            ax[1].set_ylabel("Posicion X (m)")
            ax[1].legend(loc = 'best')
            #Posición Y vs Tiempo
            ax[2].set_title(u"Posición Y vs Tiempo", fontsize = 20)
            ax[2].plot(self.tiempo, #Movimiento continuo
                       self.posicion_y,
                       label=u"Movimiento uniforme", color='g')
            ax[2].scatter(self.scatter_tiempo, #Movimiento puntual
                          self.scatter_y,
                          30,  label = "Movimiento puntual", color = 'k')
            ax[2].plot(self.scatter_tiempo[0], #Posición inicial
                       self.scatter_y[0],
                       'ro', label = "Pos inicial" )
            ax[2].plot(self.scatter_tiempo[len(self.scatter_tiempo)-1], #Posición final
                       self.scatter_y[len(self.scatter_y)-1],
                       'bo', label = "Pos final" )
            ax[2].set_xlabel("Tiempo (s)")
            ax[2].set_ylabel("Posicion Y (m)")
            ax[2].legend(loc = 'best')
        
        else:
            fig, ax = plt.subplots(1,3, figsize = (19,5), dpi = 80)
            #Posición X vs Tiempo
            ax[0].set_title(u"Posición X vs Tiempo", fontsize = 20)
            ax[0].plot(self.tiempo, #Movimiento continuo
                       self.posicion_x,
                       label=u"Movimiento uniforme", color='c')
            ax[0].scatter(self.scatter_tiempo, #Movimiento puntual
                          self.scatter_x,
                          30,  label = "Movimiento puntual", color = 'm')
            ax[0].plot(self.scatter_tiempo[0], #Posición inicial
                       self.scatter_x[0],
                       'ko', label = "Pos inicial" )
            ax[0].plot(self.scatter_tiempo[len(self.scatter_tiempo)-1], #Posición final
                       self.scatter_x[len(self.scatter_x)-1], 
                       'yo', label = "Pos final" )
            ax[0].set_xlabel("Tiempo (s)")
            ax[0].set_ylabel("Posicion X (m)")
            ax[0].legend(loc = 'best')
            #Posición Y vs Tiempo
            ax[1].set_title(u"Posición Y vs Tiempo", fontsize = 20)
            ax[1].plot(self.tiempo, #Movimiento continuo
                       self.posicion_y,
                       label=u"Movimiento uniforme", color='g')
            ax[1].scatter(self.scatter_tiempo, #Movimiento puntual
                          self.scatter_y,
                          30,  label = "Movimiento puntual", color = 'k')
            ax[1].plot(self.scatter_tiempo[0], #Posición inicial
                       self.scatter_y[0],
                       'ro', label = "Pos inicial" )
            ax[1].plot(self.scatter_tiempo[len(self.scatter_tiempo)-1], #Posición final
                       self.scatter_y[len(self.scatter_y)-1],
                       'bo', label = "Pos final" )
            ax[1].set_xlabel("Tiempo (s)")
            ax[1].set_ylabel("Posicion Y (m)")
            ax[1].legend(loc = 'best')
            #Posición Z vs Tiempo
            ax[2].set_title(u"Posición Z vs Tiempo", fontsize = 20)
            ax[2].plot(self.tiempo, #Movimiento continuo
                       self.posicion_z,
                       label=u"Movimiento uniforme", color='darkred')
            ax[2].scatter(self.scatter_tiempo, #Movimiento puntual
                          self.scatter_z,
                          30,  label = "Movimiento puntual", color = 'darkviolet')
            ax[2].plot(self.scatter_tiempo[0], #Posición inicial
                       self.scatter_z[0],
                       'ro', label = "Pos inicial", color = 'greenyellow' )
            ax[2].plot(self.scatter_tiempo[len(self.scatter_tiempo)-1], #Posición final
                       self.scatter_z[len(self.scatter_z)-1], 
                       'bo', color = 'darkseagreen', label = "Pos final")
            ax[2].set_xlabel("Tiempo (s)")
            ax[2].set_ylabel("Posicion Z (m)")
            ax[2].legend(loc = 'best')
        
    def animar(self):
        """
        Se aplica tras el método mover. Anima la trayectoria de la partícula.
        """
        #Caso 2D...
        if self.tres_d == False:
            #Para apreciar mejor la animación, se limitará el espacio de animación sólo al rango 
            #dentro del cual se mueva la partícula
            #Se deja un margen del 10% (1.1*...)
            radio_sup_x = 1.1*max(self.posicion_x[i] for i in range(len(self.posicion_x)))  
            radio_sup_y = 1.1*max(self.posicion_y[i] for i in range(len(self.posicion_y)))
            radio_inf_x = 1.1*min(self.posicion_x[i] for i in range(len(self.posicion_x)))
            radio_inf_y = 1.1*min(self.posicion_y[i] for i in range(len(self.posicion_y)))
            
            fig = plt.figure()

            ax = plt.axes(xlim=(radio_inf_x, radio_sup_x), ylim=(radio_inf_y, radio_sup_y))
            ax.set_axis_bgcolor('black')

            plot_args = {'markersize' : 8, 'alpha' : 0.6}
            line, = ax.plot([], [], 'o', c = 'w', **plot_args)

            font = {'color'  : 'white'}
            time_text = ax.text(0.02, 0.95, '', fontdict = font, transform=ax.transAxes) #Anima el tiempo
            #Función de incio de la animación
            def init():
                line.set_data([], [])
                time_text.set_text('')
                return line, time_text
            #Función de animación, regresa la posición i de la partícula y del tiempo
            def animate(i):
                line.set_data(self.posicion_x[i], self.posicion_y[i])
                time_text.set_text('time = %.1f' % self.tiempo[i])
                return line, time_text

            ani = animation.FuncAnimation(fig, animate, frames=self.movimientos,
                                          interval=self.tiempo[len(self.tiempo)-1]/4., blit=True, init_func=init)

            return ani
        #Caso 3D...
        else:
            #Para apreciar mejor la animación, se limitará el espacio de animación sólo al rango 
            #dentro del cual se mueva la partícula
            #Se deja un margen del 10% (1.1*...)
            radio_sup_x = 1.1*max(self.posicion_x[i] for i in range(len(self.posicion_x))) 
            radio_sup_y = 1.1*max(self.posicion_y[i] for i in range(len(self.posicion_y)))
            radio_sup_z = 1.1*max(self.posicion_z[i] for i in range(len(self.posicion_z)))
            radio_inf_x = 1.1*min(self.posicion_x[i] for i in range(len(self.posicion_x)))
            radio_inf_y = 1.1*min(self.posicion_y[i] for i in range(len(self.posicion_y)))
            radio_inf_z = 1.1*min(self.posicion_z[i] for i in range(len(self.posicion_z)))
            
            fig = plt.figure()
            fig.suptitle(u"Universo 3D: Posición Z vs Y vs X", fontsize=14, fontweight='bold')
            
            ax = fig.gca(projection='3d')
            
            plot_args = {'markersize' : 8, 'alpha' : 0.6}
            line, = ax.plot([], [], [], 'o', c = 'b', **plot_args)
            
            font = {'color'  : 'white'}
            time_text = ax.text(0.02, 0.95, 0.95, '', fontdict = font, transform=ax.transAxes)
            #En 3D sólo se requiere la función de animación
            #Regresa la posición i de la partícula y del tiempo
            def update_line(i):
                line.set_data(self.posicion_x[i], self.posicion_y[i])
                line.set_3d_properties(self.posicion_z[i]) #Eje Z
                time_text.set_text('time = %.1f' % self.tiempo[i])
                
                return line, time_text
            
            ax.set_xlim3d([radio_inf_x, radio_sup_x])
            ax.set_xlabel(u'Posición X (m)')

            ax.set_ylim3d([radio_inf_y, radio_sup_y])
            ax.set_ylabel(u'Posición Y (m)')

            ax.set_zlim3d([radio_inf_z, radio_sup_z])
            ax.set_zlabel(u'Posición Z (m)')
            
            ani = animation.FuncAnimation(fig, update_lines, frames=self.movimientos,
                              interval=self.tiempo[len(self.tiempo)-1]/4., blit=False) 
            
            return ani   
    #Los métodos siguientes fueron construídos para de resolver el problema de cómo mover una partícula 
    #empleando diferentes fuerzas en diferentes tiempos
    #Podemos considerarlos "obsoletos" pues tal problema se resolvió posteriormente utilizando sólo los 
    #métodos anteriores
    #Aún así, se compara su funcionamiento con lo hecho arriba    
    def mover_muchas_fuerzas(self, vector_tiempos, vector_fuerzas, vector_pasos): 
        """
        Mueve la partícula a partir de distintas fuerzas aplicadas en distintos tiempos
        -vector_tiempos es un vector de tiempos [[tiempo inicial, tiempo final], [tiempo final, tiempo final 2], ...]
        -vector_fuerzas es un vector de fuerzas (debe ser de la misma longitud que `Tiempos`)
        -vector_pasos es un vector de pasos (debe ser de la misma longitud que `Tiempos`)
        En el lapso de tiempo i se aplicará la fuerza i con un número de p = paso
        con el método mover definido arriba.
        """
        self.vector_tiempos = vector_tiempos
        self.vector_fuerzas = vector_fuerzas
        self.vector_pasos = vector_pasos
        #Activando 3D en caso de ser necesario...
        if len(vector_fuerzas[0]) == 3:
            self.tres_d == True
        #Para cada fuerza se emplea el método mover durante su tiempo respectivo
        for i in range(len(vector_fuerzas)):
            dt = vector_tiempos[i][1] - vector_tiempos[i][0] #Tiempo de aplicación
            self.mover(vector_fuerzas[i], dt, vector_pasos[i])
    
    def dibujar_muchas_fuerzas(self):
        """
        Dibuja lo hecho por el 'método muchas_fuerzas'
        Grafica:
        (1) La trayectoria de la partícula señalando el cambio de fuerza
        (2) La trayectoria de la partícula continua
        """
        #NO GRAFICA EN 3D
        fig, ax = plt.subplots(1,2, figsize = (12,6), dpi = 80)
        
        ax[0].set_title("%d Fuerzas" % len(self.vector_fuerzas), fontsize = 20) #Señala el número de fuerzas que interactúan
        ax[0].set_ylabel("Posicion Y (m)")
        ax[0].set_xlabel("Posicion X (m)")
        
        data_aux = 0
        for i in range(len(self.vector_fuerzas)):
            ax[0].plot(self.posicion_x[data_aux : data_aux + self.vector_pasos[i]], #Dibuja el movimiento de cada fuerza
                       self.posicion_y[data_aux : data_aux + self.vector_pasos[i]], 
                       label = "Fuerza %d" % (i+1), color = np.random.rand(4), linewidth = 2)
            ax[0].scatter(self.posicion_x[data_aux + self.vector_pasos[i]], 
                          self.posicion_y[data_aux + self.vector_pasos[i]],
                          30, color =  'y')
            data_aux += self.vector_pasos[i]
            
        ax[0].scatter(self.posicion_x[0], self.posicion_y[0], 40, label = "Pos inicial", c = 'b')
        ax[0].scatter(self.posicion_x[len(self.posicion_x)-1], 
                      self.posicion_y[len(self.posicion_y)-1],
                      40,  label = "Pos final", c = 'k')
        ax[0].legend(loc="best")
        
        ax[1].set_title("Movimiento continuo", fontsize = 20)
        ax[1].set_ylabel("Posicion Y (m)")
        ax[1].set_xlabel("Posicion X (m)")
        ax[1].plot(self.posicion_x,
                   self.posicion_y,
                   color = 'g', linewidth = 1.5)
        ax[1].scatter(self.posicion_x[0],
                      self.posicion_y[0],
                      40, label = "Pos inicial", c = 'b')
        ax[1].scatter(self.posicion_x[len(self.posicion_x)-1], 
                      self.posicion_y[len(self.posicion_y)-1], 40,  label = "Pos final", c = 'k')
        ax[1].legend(loc="best")