import simpy
import random
import datetime as dt
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt

tiempos = []

class Recinto():
    def __init__(self,env,mesas):
        self.env = env
        self.mesas = simpy.Resource(env,mesas)

    def calcularFecha(self,minuto):
        return dt.datetime(2021,6,3) + pd.TimedeltaIndex([minuto], unit='m')[0]

    #   - Las personas hacen fila (en caso de ser necesario)
    def hacerFila(self):
        tiempo = random.randint(10,30)
        tiempos.append(tiempo)
        yield self.env.timeout(tiempo)

    #   - Tiempo que tarda la persona en salir del recinto electoral
    def abandonarRecinto(self):
        tiempo = random.randint(2,7)
        yield self.env.timeout(tiempo)

    #   - La segunda dosis se realiza despues de 30 dias
    def esperaSegundaDosis(self):
        yield self.env.timeout(43200) # Equivalencia de 30 dias en minutos

    #   - La persona debe esperar 20 minutos para verificar que no tiene problemas de salud
    def chequeoSalud(self):
        yield self.env.timeout(20)

    #   - La vacunacion dura entre 5 a 10 minutos
    def vacunacion(self):
        tiempo = random.randint(5,10)
        yield self.env.timeout(tiempo)

    #   - La persona recibe su certificado y cita para la proxima vacuna de 2 a 3 minutos
    def certificado(self):
        espera = random.randint(2,3)
        yield self.env.timeout(espera)

    def llega_persona(self,persona):
        
        for i in range (2):
            with self.mesas.request() as mesa:
                print('**********   Persona {}  **********   ||{} dosis||'.format(int(persona),i+1))
                yield mesa

                yield self.env.process(self.hacerFila())
                t = self.calcularFecha(self.env.now)
                print('La persona {} pasa a la mesa a el {}'.format(persona,t))

                yield self.env.process(self.vacunacion())
                t = self.calcularFecha(self.env.now)
                print('La persona {} se termina de vacunar el {}'.format(persona,t))

            yield self.env.process(self.chequeoSalud())
            t = self.calcularFecha(self.env.now)
            print('La persona {} espera 20 minutos para poder realizarse chequeos en su salud, termina estos chequeos el {}'.format(persona,t))

            if i == 0:
                yield self.env.process(self.certificado())
                t = self.calcularFecha(self.env.now)
                print('La persona {} recibe su certificado a los {} minutos'.format(persona,t))

                yield self.env.process(self.abandonarRecinto())
                t = self.calcularFecha(self.env.now)
                print('La persona {} abandona el recinto el {}'.format(persona,t))

                print('La persona {} espera 30 dias para su segunda dosis'.format(persona))
                print('**********   Persona {}  **********   ||FIN {} dosis||'.format(int(persona),i+1))
                yield self.env.process(self.esperaSegundaDosis())
            else:
                yield self.env.process(self.abandonarRecinto())
                t = self.calcularFecha(self.env.now)
                print('La persona {} abandona el recinto el {}'.format(persona,t))
                print('**********   Persona {}  **********   ||FIN {} dosis||'.format(int(persona),i+1))


class Simulacion():
    def __init__(self,electores):
        self.electores = electores * 0.8 #   - 80% de la poblacion se vacunara dentro del pais
        self.electores = self.calcularPersonas(self.electores)
        
    #   - 5% al 10% no podrán vacunarse    
    def calcularPersonas(self,electores):    
        no_vacuna = 1-random.randint(5,10)/100
        self.electores = self.electores * no_vacuna
        print('Se vacunará a ' + str(int(self.electores)) + ' personas de ' + str(int(electores)) + ' personas, en el recinto Técnico Salesiano')
        return self.electores

    def ejecutar(self,env,mesas):
        recinto = Recinto(env,mesas)
        for i in range(int(self.electores)): 
            if i < 7000:
                env.process(recinto.llega_persona(i))
            else:
                yield env.timeout(random.randint(5,30)) # Tiempo de espera aleatorio para q lleguen mas personas
                yield env.process(recinto.llega_persona(i))
        

if __name__ == '__main__':
    electores = 7000
    juntas = 8
    tiempoSimulacion = 864000 #dias en minutos
    
    env = simpy.Environment()
    simulacion = Simulacion(electores)
    print('El recinto Técnico Salesiano cuenta con ' +  str(juntas) + ' mesas')
    env.process(simulacion.ejecutar(env,juntas))
    env.run(until=tiempoSimulacion)

    labels = 'Vacunados', 'No vacunados'
    sizes = [simulacion.electores, electores-simulacion.electores]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    df = DataFrame (tiempos,columns=['Tiempo'])
    df['persona'] = range(1, len(df) + 1)
    p_train = 0.50
    dosis1 = df[:int(len(df)/2)]
    dosis2 = df[int(len(df)/2):]
    dosis2['persona'] = range(1, int(len(df)/2) + 1)

    graf = [dosis1.Tiempo.mean(), dosis2.Tiempo.mean()]
    bars = ('1 Dosis', '2 Dosis')
    x_pos = np.arange(len(bars))

    # Create bars with different colors
    plt.bar(x_pos, graf, color=['red', 'green'])

    # Create names on the x-axis
    plt.xticks(x_pos, bars)

    plt.show()