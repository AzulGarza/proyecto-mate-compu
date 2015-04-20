class Universo:
    
    def __init__(self, radio, N, particulas):
        self.radio = radio
        self.N = N
        self.particulas = particulas
        self.posiciones = []
        self.velocidades = []
        self.fuerzas = np.zeros([self.N,2]) 
        
    def fuerza_total(self):
        """
        Calcula la fuerza general que ejerce el sistema sobre cada partícula
        """
        
        for i in range(self.N):
            fuerza_aux = 0
            
            for j in range(self.N):
                fuerza_aux += self.particulas[i].fuerzaAplicada(self.particulas[j])
            
            self.fuerzas[i][0] = fuerza_aux[0]
            self.fuerzas[i][1] = fuerza_aux[1]

    
    def step(self, cambio_tiempo, subpasos):
        
        """
        Calcula el cambio de estado de todas las particulas en un lapso cambio_tiempo = dt
        """
        
        for i in range(self.N):
            self.particulas[i].mover(self.fuerzas[i], cambio_tiempo, subpasos)    
        
    
    def dibujar_universo_circular(self):
        plt.figure(figsize = (10, 10), dpi = 80)
        
        X = np.linspace(-self.radio, self.radio, 1000)
        Y = np.sqrt((self.radio)**2 - X**2)
        # Dibujando el universo
        plt.scatter(0,0, 10, color = "black")  # Centro del Universo
        plt.plot(X, Y, label = u"Límites del universo", color = 'r',  linewidth = 2.5, linestyle = "--") # Límites del Universo
        plt.plot(X, -Y, color = 'r',  linewidth = 2.5, linestyle = "--")
        # Posición inicial de las partículas
        for i in range(0, int(self.N)):
            plt.scatter(self.particulas[i].posicion_0[0], self.particulas[i].posicion_0[1], 30, label = u"Partícula %d" % i)
        plt.legend(loc = "upper right")
        # Dibujar el movimiento en cualquier tiempo
        for i in range(self.N):
            plt.plot(self.particulas[i].posx, self.particulas[i].posy, '-')
            
    def dibujar_universo_cuadrado(self):
        plt.figure(figsize = (10,10), dpi = 80)
        plt.xlim(-self.radio, self.radio)
        plt.ylim(-self.radio, self.radio)
        plt.scatter(0,0, 10, label = "Centro del universo", color = "black")
        for i in range(0, int(self.N)):
            plt.scatter(self.particulas[i].posicion_0[0], self.particulas[i].posicion_0[1], 30, label = u"Partícula %d" % i)
        plt.legend(loc = "best")
        
                
                   
    def simular(self, tiempo, pasos, subpasos):
        """
        Simula los N cuerpos en un tiempo dado
        Usa el método step pasos veces
        """
        self.tiempo = np.array([(i+1)*(tiempo/self.pasos) for i in range(self.pasos)])
        for i in range(pasos):
            self.step(self.tiempo[i], subpasos) 
            self.fuerza_total() # Hecho el step de dt segundos se vuelven a reasignar las fuerzas
        
        