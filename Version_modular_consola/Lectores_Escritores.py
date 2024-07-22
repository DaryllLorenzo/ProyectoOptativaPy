import threading
import time
import random
from queue import Queue
import time

##### LECTOR = 0 ; ESCRITOR = 1
## (cantidad de procesos , tipo)

cola_creacion = Queue()
cola_creacion.put( (3, 1) ) # 3 procesos escritores
cola_creacion.put( (2, 0) ) # 2 procesos lectores
cola_creacion.put( (1, 1) ) # 1 proceso escritor
cola_creacion.put( (2, 0) ) # 2 procesos lectores

###

p1 = None
p2 = None

tiempoEstaticoL = None
tiempoEstaticoE = None
intervalo_iniL = 0
intervalo_finL = 4
intervalo_iniE = 0
intervalo_finE = 4
Estatico = False

#
mutex = threading.Semaphore(1)  # Semáforo para controlar el acceso mutuo a la sección crítica
cuarto_vacio = threading.Semaphore(1)  # Semáforo para controlar el acceso al cuarto cuando no hay escritores
mecanismo_control = threading.Semaphore(1)  # Semáforo para controlar el acceso al cuarto cuando hay lectores y escritores
lectores = 0  # Contador de lectores, inicialmente en 0
#

def menu():
    print("")
    print("Parametros: ")
    print("1- Simulacion con tiempo estatico")
    print("2- Simulacion con tiempo random entre intervalos")
    print("3- Reiniciar cantidad de procesos (ver la ayuda de parametros para entender mejor)")
    print("4- Ejecutar")
    print("5- Ayuda parametros")
    print("6- Salir")


def menuInsertar():
    print("")
    print("1- Agregar mas elementos")
    print("2- No agregar más")

def CrearElemento(cantidad , tipo): # tupla de elementos a crear
    tupla = (cantidad, tipo )    
    return tupla

def VaciarCola():
    tam = cola_creacion.qsize()
    for _ in range(tam):
        cola_creacion.get()


print("")
menu()
opcion = int(input("Seleccione una opcion: "))

while opcion != 4 and opcion != 6:
    
    if opcion == 1:
        print("")
        tiempoEstaticoL = int(input("Ingrese el valor estatico para el proceso de lector: "))
        tiempoEstaticoE = int(input("Ingrese el valor estatico para el proceso de escritor: "))
        Estatico = True
        menu()
        opcion = int(input("Seleccione una opcion: "))

    elif opcion == 2:
        print("")
        intervalo_iniL = int(input("Ingrese el valor inicio del intervalo para lectores: "))
        intervalo_finL = int(input("Ingrese el valor fin del intervalo para lectores: "))
        intervalo_iniE = int(input("Ingrese el valor inicio del intervalo para escritores: "))
        intervalo_finE = int(input("Ingrese el valor fin del intervalo para escritores: "))
        Estatico = False
        menu()
        opcion = int(input("Seleccione una opcion: "))

    elif opcion == 3:
        VaciarCola()
        print("")
        p1 = int(input("Ingrese cantidad de procesos a crear: "))
        p2 = int(input("Ingrese tipo de proceso(0 = lectores, 1 = escritores): "))
        elemento = CrearElemento(p1 , p2)
        cola_creacion.put(elemento)
        menuInsertar()
        opcionInsertar = int(input("Seleccione una opcion: "))
        
        while opcionInsertar != 2:
            p1 = int(input("Ingrese cantidad de procesos a crear: "))
            p2 = int(input("Ingrese tipo de proceso(0 = lectores, 1 = escritores): "))
            elemento = CrearElemento(p1 , p2)
            cola_creacion.put(elemento)
            menuInsertar()
            opcionInsertar = int(input("Seleccione una opcion: "))
        
        menu()
        opcion = int(input("Seleccione una opcion: "))

    elif opcion == 5:
        print("")
        print("1- Simulacion con tiempo estatico: Asignar a los procesos lectores y escritores un tiempo fijo que no varia") 
        print("2- Simulacion con tiempo random entre intervalos: Asigna el intervalo y el tiempo de ejecucion del proceso es un valor random compredido en ese intervalo")
        print("3- Reiniciar cantidad de procesos: Elimina los datos que tenemos, y comienza a crear los nuevos datos desde 0, estos datos se crean al final en el orden en que se van creando")
        menu()
        opcion = int(input("Seleccione una opcion: "))


def escritor():
    mecanismo_control.acquire()  # Adquirir el mecanismo_control para acceder al cuarto
    cuarto_vacio.acquire()  # Adquirir el cuarto para escritura
    # Simular la escritura
    #delay = random.uniform(0, 4)

    if Estatico is True:
        delay = tiempoEstaticoE
    else:
        delay = random.uniform(intervalo_iniE, intervalo_finE)

    print(f"Escritor escribiendo {delay:.2f} segundos para terminar")
    time.sleep(delay)

    cuarto_vacio.release() # Liberar el cuarto después de la escritura
    mecanismo_control.release() # Liberar el mecanismo_control para permitir el acceso de otros

def lector():
    global lectores
    mecanismo_control.acquire()  # Adquirir el mecanismo_control para acceder al cuarto
    mecanismo_control.release()  # Liberar el mecanismo_control inmediatamente

    mutex.acquire()  # Adquirir el mutex para acceder a la sección crítica
    lectores = lectores + 1  # Incrementar el contador de lectores
    if lectores == 1:  # Si es el primer lector
        cuarto_vacio.acquire()  # Adquirir el cuarto para la lectura
    mutex.release()  # Liberar el mutex

    # Simular la lectura
    #delay = random.uniform(0, 4)
    if Estatico is True:
        delay = tiempoEstaticoL
    else:
        delay = random.uniform(intervalo_iniL, intervalo_finL)
    
    print(f"Lector leyendo {delay:.2f} segundos para terminar")
    time.sleep(delay)

    mutex.acquire()  # Adquirir el mutex para acceder a la sección crítica
    lectores = lectores - 1  # Decrementar el contador de lectores
    if lectores == 0:  # Si no hay más lectores
        cuarto_vacio.release()  # Liberar el cuarto para permitir la escritura
    mutex.release()  # Liberar el mutex


# Crear hilos de lectores y escritores
def main():
    start_time = time.time()
    size = cola_creacion.qsize()
    threads = []
    for _ in range(size):
        tupla_temp = cola_creacion.get()
        if tupla_temp[1] == 0: # tupla de lectores
            for _ in range(tupla_temp[0]):
                t = threading.Thread(target=lector)
                t.start()
                threads.append(t)
        else: # tupla de escritores
            for _ in range(tupla_temp[0]):
                t = threading.Thread(target=escritor)
                t.start()
                threads.append(t)

    # Esperar a que todos los hilos terminen
    for t in threads:
        t.join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"El tiempo total de ejecución de todos los procesos fue de {total_time:.2f} segundos.")
    input("Presione una tecla para salir")
if opcion == 4:   
    main()
    

