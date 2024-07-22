import threading
import time
import random

# Variables globales para configuración
tiempoEstaticoP = None
tiempoEstaticoC = None
intervalo_iniP = 0
intervalo_finP = 4
intervalo_iniC = 0
intervalo_finC = 4
Estatico = False

# Tamaño del buffer y cantidad de productos a producir/consumir
tamanoBuffer = 10
productos = 10

# Semáforos
s1 = threading.Semaphore(tamanoBuffer)  # Espacios disponibles en el buffer
s2 = threading.Semaphore(0)  # Productos disponibles para consumir

# Buffer lógico para manejo de datos
bufferLogico = []

def menu():
    print("")
    print("Parametros: ")
    print("1- Tamaño del buffer")
    print("2- Simulacion con tiempo estatico")
    print("3- Simulacion con tiempo random entre intervalos")
    print("4- Cantidad de productos a producir y consumir")
    print("5- Ejecutar")
    print("6- Ayuda parametros")
    print("7- Salir")

print("")
print("Problema productor-consumidor:")
print("El programa describe dos procesos, productor y consumidor, ambos comparten un búfer de tamaño finito. La tarea del productor es generar un producto, almacenarlo y comenzar nuevamente; mientras que el consumidor toma (simultáneamente) productos uno a uno. El problema consiste en que el productor no añada más productos que la capacidad del buffer y que el consumidor no intente tomar un producto si el buffer está vacío.")
print("")
print("La aplicacion primeramente esta planteada con parametros de 10 tamaño de buffer, un tiempo que demora un valor random comprendido en el intervalo de 0 a 4, 10 productos a producir y 10 a consumir")
print("Pero se pueden modificar estos parametros a traves del menu de paramtros")
input("Presiona una tecla para continuar...")
menu()

opcion = int(input("Seleccione una opcion: "))

while opcion != 5 and opcion != 7:
    if opcion == 1:
        print("")
        tamanoBuffer = int(input("Ingrese el valor que le quiere dar al buffer: "))
        # Actualizar el semáforo del buffer
        s1 = threading.Semaphore(tamanoBuffer)
        s2 = threading.Semaphore(0)
        menu()
        opcion = int(input("Seleccione una opcion: "))
    elif opcion == 2:
        print("")
        tiempoEstaticoP = float(input("Ingrese el valor estatico para el proceso de productor: "))
        tiempoEstaticoC = float(input("Ingrese el valor estatico para el proceso de consumidor: "))
        Estatico = True
        menu()
        opcion = int(input("Seleccione una opcion: "))
    elif opcion == 3:
        print("")
        intervalo_iniP = float(input("Ingrese el valor inicio del intervalo para productor: "))
        intervalo_finP = float(input("Ingrese el valor fin del intervalo para productor: "))
        intervalo_iniC = float(input("Ingrese el valor inicio del intervalo para consumidor: "))
        intervalo_finC = float(input("Ingrese el valor fin del intervalo para consumidor: "))
        Estatico = False
        menu()
        opcion = int(input("Seleccione una opcion: "))
    elif opcion == 4:
        print("")
        productos = int(input("Ingrese la cantidad de productos a producir y consumir: "))
        menu()
        opcion = int(input("Seleccione una opcion: "))
    elif opcion == 6:
        print("")
        print("1- Tamaño del buffer: Cantidad de productos maximos que pueden estar sin ser consumidos")
        print("2- Simulacion con tiempo estatico: Asignar al proceso de productor y consumidor un tiempo fijo que no varia") 
        print("3- Simulacion con tiempo random entre intervalos: Asigna el intervalo y el tiempo de ejecucion del proceso es un valor random compredido en ese intervalo")
        print("4- Cantidad de productos a producir y consumir: De aqui se saca tambien la estadistica de cuanto tiempo demoró global")
        menu()
        opcion = int(input("Seleccione una opcion: "))

def productor2():
    contador_produccion = 0
    inicio_produccion = time.time()

    while contador_produccion < productos:
        dato = "a"
        s1.acquire()  # Disminuyo el semáforo s1 (espacios disponibles en el buffer)
        
        # Para tiempo de espera
        if Estatico:
            delay = tiempoEstaticoP
        else:
            delay = random.uniform(intervalo_iniP, intervalo_finP)
        
        print(f"Productor esperando {delay:.2f} segundos para producir el elemento")
        time.sleep(delay) # simular el tiempo

        bufferLogico.append(dato)
        print(f"Productor produjo: {dato}, buffer: {bufferLogico}")

        s2.release()  # Incremento el semáforo s2 (productos disponibles para consumir)
        contador_produccion += 1

    fin_produccion = time.time()
    tiempo_total_produccion = fin_produccion - inicio_produccion
    print(f"!!!!!!! Tiempo total de producción: {tiempo_total_produccion:.2f} segundos !!!!!!!")

def consumidor2():
    contador_consumo = 0
    inicio_consumo = time.time()

    while contador_consumo < productos:
        s2.acquire()  # Disminuyo el semáforo s2 (hasta que haya productos disponibles)

        # Para tiempo de espera
        if Estatico:
            delay = tiempoEstaticoC
        else:
            delay = random.uniform(intervalo_iniC, intervalo_finC)
        
        print(f"Esperando {delay:.2f} segundos para consumir")
        time.sleep(delay) # Simular tiempo

        producto = bufferLogico.pop()
        print(f"Consumidor consumió: {producto}, buffer: {bufferLogico}")

        s1.release()  # Incrementar el semáforo s1 (espacios disponibles en el buffer)
        contador_consumo += 1

    fin_consumo = time.time()
    tiempo_total_consumo = fin_consumo - inicio_consumo
    print(f"!!!!!!! Tiempo total de consumo: {tiempo_total_consumo:.2f} segundos !!!!!!!")

# Función para ejecutar el proceso productor-consumidor
def main2Solo():
    hilo1 = threading.Thread(target=productor2)
    hilo2 = threading.Thread(target=consumidor2)
    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

if opcion == 5:
    main2Solo()
