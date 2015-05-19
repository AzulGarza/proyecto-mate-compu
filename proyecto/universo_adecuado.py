
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

class Universo:
    #OBSERVACION: Muchos de los métodos empleados (sobre todo los gráficos) toman su base en los vistos en clase
    #y en los notebooks.
    def __init__(self, N, radio, particulas, tipo_limites, tipo_colision, rango_colision, masa_perdida):
        """
        Simula el movimiento de N partículas del tipo 'Particula' en un unvierso con:
        -`N` número de partículas
        -Radio `R`
        -`particulas` una lista de particulas
        -`tipo_limites` conforme:
        None Las partículas se mueven sin límites. 
        (0) Las partículas rebotan cuando 'chocan' contra los límites del universo.
        (1) Las partículas se quedan 'congeladas' cuando 'chocan' contra los límites del universo.
        (2) Las partículas desaparecen cuando 'chocan' contra los límites del universo.
        -`tipo_colision` de acuerdo a:
        None Las partículas no chocan.
        (0) Si dos partículas están suficientemente cerca (`rango_colision`), sus masas se suman, 
        se toma la posición de la masamás grande y se suman vectorialmente las velocidades.
        (1) Si dos partículas están suficientemente cerca (`rango_colision`), siguen la misma ruta pero 
        pierden masa proporcionalmente a las masas que chocan.
        -`rango_colision` aceptado para que choquen las partículas.
        -`masa_perdida` la proporción que pierde la partícula con la menor masa cuando choca ( 1 menos la que gana
        la partícula de mayor masa cuando dos partículas chocan). ENTRE 0 Y 1.
        """
        #Se inicializan características del universo
        self.N = N
        self.radio = radio
        self.particulas = particulas
        self.tipo_limites = tipo_limites
        self.tipo_colision = tipo_colision
        self.rango_colision = rango_colision
        self.masa_perdida = masa_perdida
        #Se crea un vector de fuerzas donde se almacenará la fuerza que recibirá cada partícula
        self.fuerzas = np.zeros([self.N, 2])
        #Lleva la cuenta del número de veces que se ha movido el universo
        self.movimientos_universo = 0
        self.tiempo_simulacion = 0 #Lleva el tiempo de la simulación
        #Lista que lleva los números de las partículas
        self.numeros_particulas = [i for i in range(self.N)]
        self.particulas_quitadas = [] #Lista que lleva el número de las partículas quitadas
        #Implementando 3D
        self.tres_D = False
        #Lista donde se guardan los valores 3D de cada partícula
        vector_tres_d = np.array([self.particulas[particula].tres_d for particula in range(self.N)])
        #Si cada partícula está en 3D, el Universo también
        if vector_tres_d.all() == True:
            self.tres_D = True
        #Si el caso es 3D re requerirán de tres fuerzas    
        if self.tres_D == True:
            self.fuerzas = np.zeros([self.N, 3])               
        
    def fuerza_total(self):
        """
        Calcula la fuerza general que ejerce el sistema sobre cada partícula
        """
        #Caso 2D...
        if self.tres_D == False:
            #Para cada partícula, con el principio de superposición, se calcula la fuerza que ejercen
            #las demás partículas sobre ella
            for particula in range(self.N):
                fuerza_aux_x = 0 #Fuerza auxiliar que llevará la suma de las fuerzas
                fuerza_aux_y = 0
                #Se calcula la fuerza que ejercen las otras partículas sobre esta
                for otra_particula in range(self.N):
                    fuerza_aux_x += self.particulas[particula].fuerzaAplicada(self.particulas[otra_particula])[0]
                    fuerza_aux_y += self.particulas[particula].fuerzaAplicada(self.particulas[otra_particula])[1]
                #Se guarda la fuerza
                self.fuerzas[particula][0] = fuerza_aux_x
                self.fuerzas[particula][1] = fuerza_aux_y
        #Caso 3D... Exactamente igual que el anterior, agregando un eje
        else:
            for particula in range(self.N):
                fuerza_aux_x = 0
                fuerza_aux_y = 0
                fuerza_aux_z = 0

                for otra_particula in range(self.N):
                    fuerza_aux_x += self.particulas[particula].fuerzaAplicada(self.particulas[otra_particula])[0]
                    fuerza_aux_y += self.particulas[particula].fuerzaAplicada(self.particulas[otra_particula])[1]
                    fuerza_aux_z += self.particulas[particula].fuerzaAplicada(self.particulas[otra_particula])[2]

                self.fuerzas[particula][0] = fuerza_aux_x
                self.fuerzas[particula][1] = fuerza_aux_y
                self.fuerzas[particula][2] = fuerza_aux_z
    
    def desaparecer_particula(self, numero_particula):
        """
        "Desaparece" una partícula: en realidad la aleja a una distancia de a*self.radio donde a es
        constante
        """
        #Caso 2D...
        if self.tres_D == False:
            #Si la partícula se encuentra en el I o IV cuadrante
            if self.particulas[numero_particula].posicion_actual[0] >= 0:
                #Si la partícula se encuentra en el I cuadrante
                if self.particulas[numero_particula].posicion_actual[1] >= 0:
                    self.particulas[numero_particula].posicion_actual[0] = 1e16*self.radio #La partícula se aleja lo suficiente
                    self.particulas[numero_particula].posicion_actual[1] = 1e16*self.radio #para que ya no influya en la fuerza
                    self.particulas[numero_particula].detener = True
                #Si la partícula se encuentra en el IV cuadrante
                else:
                    self.particulas[numero_particula].posicion_actual[0] = 1e16*self.radio
                    self.particulas[numero_particula].posicion_actual[1] = -1e16*self.radio
                    self.particulas[numero_particula].detener = True
            #Si la partícula se encuentra en el II o III cuadrante
            else:
                #Si la partícula se encuentra en el II cuadrante
                if self.particulas[numero_particula].posicion_actual[1] >= 0:
                    self.particulas[numero_particula].posicion_actual[0] = -1e16*self.radio
                    self.particulas[numero_particula].posicion_actual[1] = 1e16*self.radio
                    self.particulas[numero_particula].detener = True
                #Si la partícula se encuentra en el III cuadrante
                else:
                    self.particulas[numero_particula].posicion_actual[0] = -1e16*self.radio
                    self.particulas[numero_particula].posicion_actual[1] = -1e16*self.radio
                    self.particulas[numero_particula].detener = True
        #Caso 3D...
        else:
            #Si la partícula se encuentra en el I o IV cuadrante
            if self.particulas[numero_particula].posicion_actual[0] >= 0:
                #Si la partícula se encuentra en el I cuadrante
                if self.particulas[numero_particula].posicion_actual[1] >= 0:
                    #Si la partícula se encuentra en la parte positiva del eje z
                    if self.particulas[numero_particula].posicion_actual[2] >=0:
                        self.particulas[numero_particula].posicion_actual[0] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = 1e16*self.radio 
                        self.particulas[numero_particula].detener = True
                    #Si no...
                    else:
                        self.particulas[numero_particula].posicion_actual[0] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = -1e16*self.radio
                        self.particulas[numero_particula].detener = True
        
                #Si la partícula se encuentra en el IV cuadrante
                else:
                    #Si la partícula se encuentra en la parte positiva o negativa del eje z
                    if self.particulas[numero_particula].posicion_actual[2] >=0:
                        self.particulas[numero_particula].posicion_actual[0] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = 1e16*self.radio 
                        self.particulas[numero_particula].detener = True
                    #Si no...
                    else:
                        self.particulas[numero_particula].posicion_actual[0] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = -1e16*self.radio
                        self.particulas[numero_particula].detener = True
        
            #Si la partícula se encuentra en el II o III cuadrante
            else:
                #Si la partícula se encuentra en el II cuadrante
                if self.particulas[numero_particula].posicion_actual[1] >= 0:
                    #Si la partícula se encuentra en la parte positiva del eje z
                    if self.particulas[numero_particula].posicion_actual[2] >=0:
                        self.particulas[numero_particula].posicion_actual[0] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = 1e16*self.radio 
                        self.particulas[numero_particula].detener = True
                    #Si no...
                    else:
                        self.particulas[numero_particula].posicion_actual[0] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = 1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = -1e16*self.radio
                        self.particulas[numero_particula].detener = True
                #Si la partícula se encuentra en el III cuadrante
                else:
                   #Si la partícula se encuentra en la parte positiva del eje z
                    if self.particulas[numero_particula].posicion_actual[2] >=0:
                        self.particulas[numero_particula].posicion_actual[0] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = 1e16*self.radio 
                        self.particulas[numero_particula].detener = True
                    #Si no...
                    else:
                        self.particulas[numero_particula].posicion_actual[0] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[1] = -1e16*self.radio
                        self.particulas[numero_particula].posicion_actual[2] = -1e16*self.radio
                        self.particulas[numero_particula].detener = True
        
    def verificar_limites(self, tipo):
        """
        Verifica que las partículas no se salgan del radio del Universo.
        Se procede de acuerdo a `tipo`. 
        Tipo:
        (0) Las partículas aparecen del otro lado cuando 'chocan' contra los límites del universo.
        (1) Las partículas se quedan 'congeladas' cuando 'chocan' contra los límites del universo.
        (2) Las partículas desaparecen cuando 'chocan' contra los límites del universo.
        """
        if tipo == 0:
            for particula in range(self.N):
                #Si la partícula rebasa el radio en la posición X
                if np.abs(self.particulas[particula].posicion_actual[0]) >= self.radio:
                    #Si la partícula rebasa está en la parte positiva del eje X
                    if self.particulas[particula].posicion_actual[0] > 0:
                        self.particulas[particula].posicion_x[len(self.particulas[particula].posicion_x)-1] -= 2*self.radio
                    else: #Si no...
                        self.particulas[particula].posicion_x[len(self.particulas[particula].posicion_x)-1] += 2*self.radio
                #Si la partícula rebasa el radio en la posición Y
                if np.abs(self.particulas[particula].posicion_actual[1]) >= self.radio:
                    #Si la partícula está en la parte positiva del eje Y
                    if self.particulas[particula].posicion_actual[1] > 0:
                        self.particulas[particula].posicion_y[len(self.particulas[particula].posicion_x)-1] -= 2*self.radio
                    else: #Si no...
                        self.particulas[particula].posicion_y[len(self.particulas[particula].posicion_x)-1] += 2*self.radio
                #Caso 3D... Si la partícula rebasa el radio en la posición Z
                if self.tres_D == True:
                    if np.abs(self.particulas[particula].posicion_actual[2]) >= self.radio:
                        #Si la partícula está en la parte positiva del eje Z
                        if self.particulas[particula].posicion_actual[2] > 0:
                            self.particulas[particula].posicion_y[len(self.particulas[particula].posicion_x)-1] -= 2*self.radio
                        else: #Si no...
                            self.particulas[particula].posicion_y[len(self.particulas[particula].posicion_x)-1] += 2*self.radio
                        
        elif tipo == 1:
            for particula in range(self.N):
                #Para cada partícula calculamos su posición absoluta
                absx = np.abs(self.particulas[particula].posicion_actual[0])
                absy = np.abs(self.particulas[particula].posicion_actual[1])
                if self.tres_D == True: #Caso 3D...
                    absz = np.abs(self.particulas[particula].posicion_actual[2])
                    #Si alguna partícula choca contra algún límite, se detiene
                    if absx >= self.radio or absy >= self.radio or absz >= self.radio:
                        self.particulas[particula].detener = True
                else: #Caso 2D...
                    #Si alguna pariucla choca contra algún límite, se detiene
                    if absx >= self.radio or absy >= self.radio:
                        self.particulas[particula].detener = True
                    
        elif tipo == 2:
            for particula in range(self.N):
                #Para cada partícula calculamos su posición absoluta
                absx = np.abs(self.particulas[particula].posicion_actual[0])
                absy = np.abs(self.particulas[particula].posicion_actual[1])
                if self.tres_D == True: #Caso 3D...
                    absz = np.abs(self.particulas[particula].posicion_actual[2])
                    #Si alguna partícula choca contra algún límite, se desaparece
                    if absx >= self.radio or absy >= self.radio or absz >= self.radio:
                        self.desaparecer_particula(particula)
                else: #Caso 2D...
                    if absx >= self.radio or absy >= self.radio:
                        self.desaparecer_particula(particula)
    
    def verificar_colision(self, tipo, cerca, proporcion_perdida):
        """
        De acuerdo al `tipo` de colisión hace lo siguiente:
        Tipo:
        (0) Si dos partículas están suficientemente cerca, sus masas se suman, se toma la posición de la masa
        más grande y se suman vectorialmente las velocidades.
        (1) Si dos partículas están suficientemente cerca, siguen la misma ruta pero pierden masa proporcionalmente
        a las masas que chocan.
        """
        
        if tipo == 0:
            for particula in range(self.N):
                iterar = [particula_distinta for particula_distinta in range(self.N)]
                iterar.pop(iterar.index(particula)) #Se quita la particula actual pues su distancia a sí misma es 0
                #Para las otras partículas...
                for otra_particula in iterar:
                    #Si la distancia de la partícula actual a otra partícula distinta en menor al rango de colisión...
                    if self.particulas[particula].distancia(self.particulas[otra_particula])[0] <= cerca:
                        #Si la masa de la partícula actual es mayor a la de la partícula distinta,
                        #la partícula actual gana la masa y la velocidad de la otra;
                        #la otra partícula desaparece
                        if self.particulas[particula].masa >= self.particulas[otra_particula].masa:
                            self.particulas[particula].masa += self.particulas[otra_particula].masa
                            tamano = len(self.particulas[particula].velocidad_x) - 1
                            self.particulas[particula].velocidad_x[tamano] += self.particulas[otra_particula].velocidad_x[tamano]
                            self.particulas[particula].velocidad_y[tamano] += self.particulas[otra_particula].velocidad_y[tamano]
                            if self.tres_D == True: #Caso 3D...
                                self.particulas[particula].velocidad_z[tamano]+=self.particulas[otra_particula].velocidad_z[tamano]
                            self.desaparecer_particula(otra_particula)
                        else: #Si no...
                            self.particulas[otra_particula].masa += self.particulas[particula].masa
                            tamano = len(self.particulas[otra_particula].velocidad_x) - 1
                            self.particulas[otra_particula].velocidad_x[tamano] += self.particulas[particula].velocidad_x[tamano]
                            self.particulas[otra_particula].velocidad_y[tamano] += self.particulas[particula].velocidad_y[tamano]
                            if self.tres_D == True: #Caso 3D...
                                self.particulas[otra_particula].velocidad_z[tamano]+=self.particulas[particula].velocidad_z[tamano]
                            self.desaparecer_particula(particula)
               
        elif tipo == 1:
            for particula in range(self.N):
                iterar = [particula_distinta for particula_distinta in range(self.N)]
                iterar.pop(iterar.index(particula)) #Se quita la particula actual pues su distancia a sí misma es 0
                #Para las otras partícula
                for otra_particula in iterar:
                    #Si la distancia de la partícula actual a otra partícula distinta en menor al rango de colisión...
                    if self.particulas[particula].distancia(self.particulas[otra_particula])[0] <= cerca:
                        #Si la masa de la partícula actual es mayor a la de la partícula distinta,
                        #la partícula actual gana la masa de acuerdo a la proporción dada y la otra pierde masa de acuerdo
                        #también a la proporción; las velocidades se conservan
                        if self.particulas[particula].masa > self.particulas[otra_particula].masa:
                            self.particulas[particula].masa += (1 - proporcion_perdida)*self.particulas[otra_particula].masa
                            self.particulas[otra_particula].masa *= 1 - proporcion_perdida
                            #Si la masa de la otra partícula se vuelve no positiva, desaparece
                            if self.particulas[otra_particula].masa <= 0:
                                self.desaparecer_particula(otra_particula)
                        #Si la masa de partícula actual es menor a la de la partícula distinta, igual pero a la inversa
                        elif self.particulas[particula].masa < self.particulas[otra_particula].masa:
                            self.particulas[otra_particula].masa += (1 - proporcion_perdida)*self.particulas[particula].masa
                            self.particulas[particula].masa *= 1 - proporcion_perdida
                            #Si la masa de partícula se vuelve no positiva, desaparece
                            if self.particulas[particula].masa <= 0:
                                self.desaparecer_particula(particula)
                        #Si las masas son iguales, ambas pierden el 50% de sus masas
                        else:
                            self.particulas[particula].masa *= 0.5
                            self.particulas[particula].masa *= 0.5 
                            #SI la masa de la partícula se vuelve no positiva, desaparece
                            if self.particulas[particula].masa <= 0:
                                self.desaparecer_particula(particula)
                            #Si la masa de la otra partícula se vuelve no postiva, desaparece
                            if self.particulas[otra_particula].masa <= 0:
                                self.desaparecer_particula(otra_particula)
                                  
    def step(self, cambio_tiempo, subpasos):
        """
        Calcula el cambio de estado de todas las particulas en un lapso cambio_tiempo = dt
        """
        #Cada partícula se mueve de acuerdo a la fuerza calculada por el método 'fuerzas'
        #durante un tiempo `cambio_tiempo` que se calcula en el método 'simular'
        for particula in range(self.N):
            self.particulas[particula].mover(self.fuerzas[particula], cambio_tiempo, subpasos)
                               
    def simular(self, tiempo, pasos, subpasos):
        """
        Simula el movimiento de los N cuerpos en un tiempo dado
        Usa el método step un número de `pasos` veces
        Funcionamiento:
        Se calcula el lapso de tiempo en el que se estarán actualizando las fuerzas a través de 
        dt = tiempo/pasos
        Para cada paso...
        Se calculan las fuerzas resultantes de las posiciones iniciales
        Hecho esto, se verifica si se quieren checar los límites y las colisiones
        Posteriormente se realiza el movimiento de las partículas durante un tiempo dt; para esto, como el método 'mover'
        de las partículas requiere un número de pasos también, se usa `subpasos`
        """
        self.tiempo_simulacion += tiempo #Actualización del tiempo de simulación
        dt = tiempo/pasos #El lapso de tiempo entre actualización de fuerzas por el método 'fuerzas'
        for i in range(pasos): #Para cada paso...
            self.fuerza_total()#Se calculan las fuerzas
            if self.tipo_limites != None: #Si se quieren verificar los límites
                self.verificar_limites(self.tipo_limites)
            if self.tipo_colision != None: #Si se quieren verificar las colisiones
                self.verificar_colision(self.tipo_colision, self.rango_colision, self.masa_perdida)
            self.step(dt, subpasos) #Se hace el step para mover a las partículas 
        #Se actualiza el número de movimientos
        #Notar que el universo se mueve pasos*subpasos veces
        self.movimientos_universo = self.particulas[0].movimientos
                 
    def dibujar(self):
        #Caso 2D...
        if self.tres_D == False:
            fig = plt.figure(figsize = (6,6), dpi = 80)
            fig.suptitle(u"Universo: Posición Y vs Posición X", fontsize = 14, fontweight = 'bold')
            #Se deja un rango del 10% para visualizar mejor al universo
            ax = plt.axes(xlim=(-1.1 * self.radio, 1.1 * self.radio), ylim=(-1.1 * self.radio, 1.1 * self.radio))
            #Se grafican los límites del universo
            ax.plot([-self.radio, self.radio, self.radio, -self.radio, -self.radio], 
                    [-self.radio, -self.radio, self.radio, self.radio, -self.radio],
                    '--', linewidth = 0.5, c = 'g')
            #Para cada partícula...
            for particula in range(self.N):
                colores = np.random.rand(4) #Se escoge un color al azar
                self.particulas[particula].movimiento_puntual() #Se calcula su movimiento puntual
                #Movimiento continuo
                ax.plot(self.particulas[particula].posicion_x, 
                        self.particulas[particula].posicion_y, 
                        color = colores, linewidth = 1, label = u"Partícula %d" % (particula + 1))
                #Movimiento puntual
                ax.scatter(self.particulas[particula].scatter_x, 
                           self.particulas[particula].scatter_y, 30,  
                           color = colores)
            
            ax.set_xlabel(u'Posición X (m)')
            ax.set_ylabel(u'Posición Y (m)')
            
            ax.legend(loc = "best")
        #Caso 3D...    
        else:
            fig = plt.figure(figsize = (6, 6), dpi = 80)
            fig.suptitle(u"Universo 3D: Posición Z vs Y vs X", fontsize=14, fontweight='bold')
          
            ax = fig.gca(projection='3d')
            #Para cada partícula...
            for particula in range(self.N):
                colores = np.random.rand(4) #Se escoge un color al azar
                self.particulas[particula].movimiento_puntual() #Se calcula el movimiento puntual de cada partícula
                #Movimiento continuo
                ax.plot(self.particulas[particula].posicion_x, 
                        self.particulas[particula].posicion_y,
                        self.particulas[particula].posicion_z,
                        color = colores, linewidth = 1, label = u"Partícula %d" % (particula + 1))
                #Movimiento puntual
                ax.scatter(self.particulas[particula].scatter_x,
                           self.particulas[particula].scatter_y, 
                           self.particulas[particula].scatter_z,
                           color = colores)
                
            ax.set_xlabel(u'Posición X (m)')
            ax.set_ylabel(u'Posición Y (m)')
            ax.set_zlabel(u'Posición Z (m)')
            #Se deja un espacio del 10% para apreciar mejor el universo
            ax.set_xlim(-1.1 * self.radio, 1.1 * self.radio)
            ax.set_ylim(-1.1 * self.radio, 1.1 * self.radio)
            ax.set_zlim=(-1.1 * self.radio, 1.1 * self.radio)
            
            ax.legend(loc = 'best')
        
    def animar(self):
        """
        Se aplica tras el método simular.
        """
        #Caso 2d...
        if self.tres_D == False:
            fig = plt.figure()
            #Se deja un espacio del 10% para apreciar mejor el movimiento de la partícula
            ax = plt.axes(xlim=(-1.1 * self.radio, 1.1 * self.radio), ylim=(-1.1 * self.radio, 1.1 * self.radio))
            #Se grafican los límites del universo
            ax.plot([-self.radio, self.radio, self.radio, -self.radio, -self.radio], 
                    [-self.radio, -self.radio, self.radio, self.radio, -self.radio],
                    '--', linewidth = 0.5, c = 'r')
            ax.set_axis_bgcolor('azure')

            plot_args = {'markersize' : 8, 'alpha' : 0.6}
            line, = ax.plot([], [], 'o', color = np.random.rand(4), **plot_args)

            font = {'color'  : 'black'}
            time_text = ax.text(0.02, 0.95, '', fontdict = font, transform=ax.transAxes)
            #Anima tiempo    
            tiempos = [i*self.tiempo_simulacion/self.movimientos_universo for i in range(self.movimientos_universo+1)] 
            #Función de inicio de la animación
            def init():
                line.set_data([], [])
                time_text.set_text('')
                return line, time_text
            #Función de animación, regresa la posición i de todas partícula y del tiempo
            def animate(i):
                x = []
                y = []
                for particula in range(self.N):
                    if len(self.particulas[particula].posicion_x) >= i:
                        x.append(self.particulas[particula].posicion_x[i])
                        y.append(self.particulas[particula].posicion_y[i])
                line.set_data(x, y)
                time_text.set_text('time = %.1f' % tiempos[i])
                return line, time_text

            ani = animation.FuncAnimation(fig, animate, frames=self.movimientos_universo,
                                          interval=self.tiempo_simulacion/4., blit=False, init_func=init)

            return ani
        
        else:
            fig = plt.figure()
            fig.suptitle(u"Universo 3D: Posición Z vs Y vs X", fontsize=14, fontweight='bold')
            
            ax = fig.gca(projection='3d')
            
            plot_args = {'markersize' : 8, 'alpha' : 0.6}
            line, = ax.plot([], [], [], 'o', **plot_args)
            #En 3D sólo se requiere la función de animación
            #Regresa la posición i de todas partícula
            def update_lines(i) :
                x = []
                y = []
                z = []
                for particula in range(self.N):
                    if len(self.particulas[particula].posicion_x) >= i:
                        x.append(self.particulas[particula].posicion_x[i])
                        y.append(self.particulas[particula].posicion_y[i])
                        z.append(self.particulas[particula].posicion_z[i])
                line.set_data(x, y)
                line.set_3d_properties(z)
                
                return line
            
            ax.set_xlim3d([-1.1*self.radio, 1.1*self.radio])
            ax.set_xlabel(u'Posición X (m)')

            ax.set_ylim3d([-1.1*self.radio, 1.1*self.radio])
            ax.set_ylabel(u'Posición Y (m)')

            ax.set_zlim3d([-1.1*self.radio, 1.1*self.radio])
            ax.set_zlabel(u'Posición Z (m)')
            
            ani = animation.FuncAnimation(fig, update_lines, frames=self.movimientos_universo,
                              interval=self.tiempo_simulacion/4., blit=False) 
            
            return ani

        