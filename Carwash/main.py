# Consideraciones
#   - Numero de vehiculos
#   - Numero de maquinas de lavado
#   - Tiempo que se demora en lavar (aleatorio)

# Calcular el tiempo a la llegada a la maquina (aleatorio)
# Calcular el tiempo que toma el vehiculo para salir del local (aleatorio)
# Intervalo de llegada de cada vehiculo
# Tiempo de simulacion

import simpy
import random
import numpy

class CarWash():
    def __init__(self,env,maquinas):
        self.env = env
        self.maquinas = simpy.Resource(env,maquinas)

    def llegadaMaquina(self, tiempo):
        yield self.env.timeout(tiempo)

    def lavadoVehiculo(self,tiempo):
        yield self.env.timeout(tiempo)

    def salidaVehiculo(self,tiempo):
        yield self.env.timeout(tiempo)

    def llegadaVehiculo(self,vehiculo):
        
        with self.maquinas.request() as maquina:
            print('El {} llega al minuto {:,.2f}'.format(vehiculo,self.env.now))
            yield maquina

            # Calcular el tiempo a la llegada a la maquina (aleatorio)
            tiempo_llegada = random.randint(1,5)
            #print('El {} llega al minuto {:,.2f}'.format(vehiculo,self.env.now))
            yield self.env.process(self.llegadaMaquina(tiempo_llegada))
            print('El {} llego a la maquina al minuto {:,.2f}'.format(vehiculo,self.env.now))

            # Tiempo que se demora en lavar (aleatorio)
            tiempo_lavado = random.randint(5,11)
            yield self.env.process(self.lavadoVehiculo(tiempo_lavado))
            print('El {} termino de lavarse al minuto {}'.format(vehiculo,self.env.now))

            # Calcular el tiempo que toma el vehiculo para salir del local (aleatorio)
            tiempo_salida = random.randint(2,5)
            yield self.env.process(self.salidaVehiculo(tiempo_salida))
            print('El {} salio del local al minuto {}'.format(vehiculo,self.env.now))


class Simulacion():
    def __init__(self,inicio):
        self.inicio = inicio
        self.nombreVehiculo = 'Vehiculo {}'

    def ejecutar(self,env,maquinas,intervalo):
        carwash = CarWash(env,maquinas)
        self.iniciar_vehiculos(env,carwash)

        while True:
            yield env.timeout(random.randint(intervalo-2,intervalo+2)) # Tiempo de espera aleatorio para q llegue otro vehiculo
            self.inicio+=1
            yield env.process(carwash.llegadaVehiculo(self.nombreVehiculo.format(self.inicio)))

    def iniciar_vehiculos(self,env,carwash):
        for i in range(self.inicio):
            env.process(carwash.llegadaVehiculo(self.nombreVehiculo.format(i)))


if __name__ == '__main__':
    inicio = 5
    maquinas = 3
    intervalo = 15
    tiempoSimulacion = 60

    env = simpy.Environment()
    simulacion = Simulacion(inicio)
    env.process(simulacion.ejecutar(env,maquinas,intervalo))
    env.run(until=tiempoSimulacion)