from vpython import *
import numpy as np
scene.range = 10 # se define la dimensión de la escena 


#flecha para los vectores que definen el sistema coordenado

X = arrow(pos=vec(-5,0,0), axis=vec(5,0,0), color=color.red) # Eje x
label(pos=vec(0,0,0), text='X') 
Y = arrow(pos=vec(-5,0,0), axis=vec(0,5,0), color=color.green) # Eje y
label(pos=vec(-5,5,0), text='Y') 
Z = arrow(pos=vec(-5,0,0), axis=vec(0,0,5)) # Eje z
label(pos=vec(-5,0,5), text='Z') 

#Creación de objetos (a.k.a proyectiles): se define su posición inicial, dimensiones, color y que se vea su trayectoria

proyectil = sphere(pos = vec(-5,0,0),radius = 0.5, color = color.red, make_trail = True)  # proyectil movimiento ideal
proyectil_arrastre = sphere(pos = vec(-5,0,0),radius = 0.5, color = color.blue, make_trail = True)  # proyectil movimiento con arrastre
proyectil_arrastre_velocidad = sphere(pos = vec(-5,0,0),radius = 0.5, color = color.white, make_trail = True)  # proyectil movimiento con arrastre y viento 
proyectil_magnus = box(pos = vec(-5,0,0),shape = vec(0.01,0.01,0.02), color = color.green, make_trail = True) # proyectil con arrastre, viento y efecto magnus

# A los proyectiles se les pueden asignar métodos ( condiciones iniciales ) (todo en el sistema internacional)

proyectil.rapidez =  22  #rapidez inicial m/s
proyectil.angulo = 45*np.pi/180 #angulo inicial visto desde el eje +x (tiro hacia la derecha)
proyectil.velocidad = vec(proyectil.rapidez*cos(proyectil.angulo),proyectil.rapidez*sin(proyectil.angulo),0) # vector velocidad del proyectil

# copia para cada movimiento--------------------------------------------------------------------

# Proyectil con arrastre

proyectil_arrastre.rapidez =  proyectil.rapidez  #rapidez inicial
proyectil_arrastre.angulo = proyectil.angulo  #angulo inicial visto desde el eje +x (tiro hacia la derecha)
proyectil_arrastre.velocidad = proyectil.velocidad # vector velocidad del proyectil

# Proyectil con arrastre y viento

proyectil_arrastre_velocidad.rapidez =  proyectil.rapidez #rapidez inicial
proyectil_arrastre_velocidad.angulo = proyectil.angulo #angulo inicial visto desde el eje +x (tiro hacia la derecha)
proyectil_arrastre_velocidad.velocidad = proyectil.velocidad # vector velocidad del proyectil
viento_velocidad = vec(0,0,2) # vector velocidad del viento

# Proyectil con arrastre, viento y efecto magnus (rotación)

proyectil_magnus.rapidez =  proyectil.rapidez #rapidez inicial
proyectil_magnus.angulo = proyectil.angulo #angulo inicial visto desde el eje +x (tiro hacia la derecha)
proyectil_magnus.velocidad = proyectil.velocidad # vector velocidad del proyectil
w = vec(0,10,0) #vector velocidad angular para efecto magnus (define el eje de rotación)

# Parámetros (masa, aceleración de la gravedad sobre la superficie terrestre, coeficiente de arrastre, coeficiente "magnus", área transversal, densidad del fluido donde se encuentra):


proyectil.masa = 0.250 # kg
ACELERACION_G = 9.8 # Magnitud del campo gracitacional sobre la corteza terrestre

#parametros de movimiento con arrastre--------------------------------------------------------------
rho_aire = 1.225 # kg/m^3 %densidad del aire
radio = 0.2 # radio del proyectil [m]
area_proyectil = np.pi*(radio)**2 # área transversal del proyectil (esférico) 
drag_coef = 0.002 # coeficiente de arrastre (tener presente si se trabaja en el régimen lineal, cuadrático o mixto)

#parametros efecto magnus---------------------------------------------------------------------------


magnus_coef = 0.5 # coeficiente de sustentacion de rotación 

# Condiciones temporales (tiempo inicial e intervalo)----------------------------------------------------------------------------
t = 0 # tiempo inicial
dt = 0.01 # intervalo de tiempo


#para que el programa se detenga cuando se alcance el suelo (el proyectil ideal), se define que la variable y del método POS,  debe ser mayor o igual que cero(para que pueda iniciar la simulación):

while(proyectil.pos.y >= 0): #con esto se garantiza que se toman los valores de y = 0
    # fuerza actuando sobre el proyectil ideal

    rate(10) # fotogramas por segundo 

    fuerza_gravitacional = vec(0,-proyectil.masa*ACELERACION_G,0) #vector de fuerza gravitacional
    fuerza_total = fuerza_gravitacional # fuerza total movimiento ideal
    
    # fuerzas de arrastre
    
    arrastre_direccion = -proyectil_arrastre.velocidad/mag(proyectil_arrastre.velocidad) #direccion de la fuerza de arrastre
    fuerza_arrastre = (0.5*rho_aire*area_proyectil*mag(proyectil_arrastre.velocidad)**2)*(arrastre_direccion) # fuerza de arrastre
    fuerza_total_a = fuerza_gravitacional + fuerza_arrastre #fuerza total para el movimiento con arrastre

    
    # fuerza de arrastre con viento incluido 

    arrastre_direccion_v = -(proyectil_arrastre_velocidad.velocidad-viento_velocidad)/mag(proyectil_arrastre_velocidad.velocidad-viento_velocidad) #direccion de la fuerza de arrastre
    fuerza_arrastre_v = (0.5*rho_aire*area_proyectil*mag(proyectil_arrastre_velocidad.velocidad-viento_velocidad)**2)*(arrastre_direccion_v)
    fuerza_total_v = fuerza_gravitacional + fuerza_arrastre_v #fuerza total para el arrastre con viento incluido

    # fuerza de arrastre con viento incluido y efecto magnus

    fuerza_magnus = proyectil.masa*magnus_coef*cross(w,proyectil_magnus.velocidad)
    arrastre_direccion_m = -(proyectil_magnus.velocidad-viento_velocidad)/mag(proyectil_magnus.velocidad-viento_velocidad) #direccion de la fuerza de arrastre
    fuerza_arrastre_m = (0.5*rho_aire*area_proyectil*mag(proyectil_magnus.velocidad-viento_velocidad)**2)*(arrastre_direccion_m)
    fuerza_total_m = fuerza_gravitacional + fuerza_arrastre_m + fuerza_magnus #fuerza total para el arrastre, viento y efecto magnus



    # se actualizan las velocidades

    proyectil.velocidad = proyectil.velocidad + (fuerza_total/proyectil.masa)*dt # Se actualizan las velocidades a partir del impulso adquirido para cada uno de los movimientos tomados
    proyectil_arrastre.velocidad +=  (fuerza_total_a/proyectil.masa)*dt
    proyectil_arrastre_velocidad.velocidad += (fuerza_total_v/proyectil.masa)*dt
    proyectil_magnus.velocidad += (fuerza_total_m/proyectil.masa)*dt



    # se actualizan las posiciones de igual forma que se actualizan las fuerzas
    proyectil.pos  = proyectil.pos + proyectil.velocidad*dt
    proyectil_arrastre.pos = proyectil_arrastre.pos  +  proyectil_arrastre.velocidad*dt
    proyectil_arrastre_velocidad.pos = proyectil_arrastre_velocidad.pos  +  proyectil_arrastre_velocidad.velocidad*dt
    proyectil_magnus.pos = proyectil_magnus.pos  +  proyectil_magnus.velocidad*dt
    proyectil_magnus.rotate((mag(w)*t),axis = w) # se rota el objeto sobre el eje del vector w, y angulo |w|*t definido por la magnitud de la velocidad angular que se definió antes
    # se actualiza el tiempo
    t = t + dt
