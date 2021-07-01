import simpy
import random
import datetime as dt
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt

contagiadosCursos = []
contagiadosNum = []

class Colegio():
    def __init__(self,env,docentes,estudiantes):
        self.env = env
        self.docentes = simpy.Resource(env,docentes)
        self.numAlumnos = int(estudiantes/docentes)
        self.totalContagiados = 0

    #   - 6 horas diaras de clase durante un mes
    def aula(self):
        yield self.env.timeout(1800)

    #   - Recreos de 30 minutos (600 minutos durante el mes), foco de contagio de hasta el 2%
    def recreo(self):
        self.contagiados = random.randint(0,2)
        contagiadosNum.append(self.contagiados)
        yield self.env.timeout(600)

    def clases(self,i):
        
        with self.docentes.request() as docente:
            print('**********     Curso ' + str(i+1) + '     **********' + str(self.numAlumnos))
            yield docente

            yield self.env.process(self.aula())

            yield self.env.process(self.recreo())

            print('Contagiados en los recreos: ' + str(self.contagiados))

            if (self.contagiados!=0):
                contagiadosCursos.append(i+1)
                print('Curso: ' + str(i+1) + ' cerrado')


class Simulacion():
    def __init__(self,docentes,estudiantes):
        self.docentes = int(docentes - (docentes * 10)/100)
        print('Se vacunó a ' + str(self.docentes) + ' de ' + str(docentes) + ' docentes')
        self.estudiantes = self.calcularEstudiantes(estudiantes)

    #   - 5% al 10% de estudiantes no podrán asistir    
    def calcularEstudiantes(self,estudiantes):    
        no_asiste = 1-random.randint(5,10)/100
        self.estudiantes = estudiantes * no_asiste
        print('Asistiran ' + str(int(self.estudiantes)) + ' estudiantes de ' + str(int(estudiantes)))
        return self.estudiantes

    def ejecutar(self,env):
        colegio = Colegio(env,self.docentes,self.estudiantes)
        i = 0
        while i<self.docentes:
            #yield env.timeout(random.expovariate(1 / 0.5))
            yield env.process(colegio.clases(i))
            i=i+1
        

if __name__ == '__main__':
    NUM_DOCENTES = 22
    NUM_ESTUDIANTES = 359
    SIM_TIME = 46080  # Simulate until 32 dias en minutos

    print('Colegio CEBCI')
    env = simpy.Environment()
    simulacion = Simulacion(NUM_DOCENTES, NUM_ESTUDIANTES)
    env.process(simulacion.ejecutar(env))
    env.run(until=SIM_TIME)

    print('------------------     RESULTADOS     ------------------')
    print('Se deben cerrar los cursos:')
    print(contagiadosCursos)

    labels = 'Estudiantes sanos', 'Estudiantes contagiados'
    sizes = [simulacion.estudiantes, simulacion.estudiantes-int(sum(contagiadosNum))]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()