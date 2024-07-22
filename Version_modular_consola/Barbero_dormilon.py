import threading
import time
import random

cant_sillas = 5
intervalo_ini = 0 # barbero
intervalo_fin = 4 # barbero
intervalo_ini_llega = 0 # llega cliente
intervalo_fin_llega = 2 # llega cliente
cantClientes = 15

sem_sillasAccesibles = threading.Semaphore(cant_sillas) # Controla el acceso a las sillas disponibles en la barbería
sem_clientes = threading.Semaphore(0) # Indica cuando hay un cliente esperando para ser atendido
sem_barberoListo = threading.Semaphore(0) # Indica cuando el barbero ha terminado de atender a un cliente
sillasLibres = cant_sillas # Inicializar con 5 sillas
sillasOcupadas = [False] * cant_sillas # Lista para rastrear las sillas ocupadas
clientesAtendidos = 0
clientesSeFueron = 0


print("")


def menu():
    print("")
    print("Parametros: ")
    print("1- Cantidad de sillas en la barberia")
    print("2- Simulacion de tiempo de llegada de clientes, valor random entre intervalo")
    print("3- Simulacion de tiempo barbero atiende a cliente, valor random entre intervalo")
    print("4- Cantidad de clientes que van a llegar")
    print("5- Ejecutar")
    print("6- Ayuda parametros")
    print("7- Salir")


###### parte visual

print("")
print("Problema barbero-dormilón:")
print("El problema consiste en una barbería en la que trabaja un barbero que tiene un único sillón de barbero y varias sillas para esperar. Cuando no hay clientes, el barbero se sienta en una silla y se duerme. Cuando llega un nuevo cliente, éste o bien despierta al barbero o —si el barbero está afeitando a otro cliente— se sienta en una silla (o se va si todas las sillas están ocupadas por clientes esperando).")
print("")

print("La aplicacion primeramente esta planteada con parametros: ")
print("5 sillas de espera para los clientes")
print("Un tiempo que demora un valor random comprendido en el intervalo de 0 a 4 para que el barbero atienda al cliente")
print("Un tiempo que demora un valor random comprendido en el intervalo de 0 a 2 para la llegada de clientes")
print("15 clientes a llegar")
print(" ** Pero se pueden modificar estos parametros a traves del menu de paramtros ** ")

input("Presiona una tecla para continuar...")

menu()

opcion = int(input("Seleccione una opcion: "))

while opcion != 5 and opcion != 7:

    if opcion == 1:
        print("")
        for _ in range(cant_sillas):
            sillasOcupadas.pop()

        cant_sillas = int(input("Ingrese la nueva cantidad de sillas: "))
        sillasLibres = cant_sillas

        sillasOcupadas = [False] * cant_sillas

        menu()
        opcion = int(input("Seleccione una opcion: "))

    elif opcion == 2:
        print("")
        intervalo_ini_llega = float(input("Ingrese el valor inicio del intervalo: "))
        intervalo_fin_llega = float(input("Ingrese el valor fin del intervalo: "))
        menu()
        opcion = int(input("Seleccione una opcion: "))

    elif opcion == 3:
        print("")
        intervalo_ini = float(input("Ingrese el valor inicio del intervalo: "))
        intervalo_fin = float(input("Ingrese el valor fin del intervalo: "))
        menu()
        opcion = int(input("Seleccione una opcion: "))

    elif opcion == 4:
        print("")
        cantClientes = int(input("Diga la cantidad de clientes que va a entrar a la barberia: "))
        menu()
        opcion = int(input("Seleccione una opcion: "))
    elif opcion == 6:
        print("")
        print("1- Cantidad de sillas: Cantidad de sillas que van a haber en la barberia para los clientes sentar a esperar")
        print("2- Simulacion de tiempo de llegada de clientes: Asigna el intervalo y el tiempo en que llega un nuevo cliente a la barberia es un valor random compredido en ese intervalo") 
        print("3- Simulacion de tiempo barbero atiende a cliente: Asigna el intervalo y el tiempo en que el barbero atiende a un cliente es un valor random compredido en ese intervalo")
        print("4- Cantidad de clientes que van a llegar: De aqui se saca tambien la estadistica de cuantos clientes fueron atendidos y cuantos se fueron")
        menu()
        opcion = int(input("Seleccione una opcion: "))


def barbero():
    global sillasLibres, sillasOcupadas, clientesAtendidos
    while True:
        sem_clientes.acquire() # Espera a que haya un cliente
        sem_sillasAccesibles.acquire() # Adquiere el acceso a las sillas
        for i in range(len(sillasOcupadas)):
            if sillasOcupadas[i]:
                sillasLibres += 1
                sillasOcupadas[i] = False
                print(f"Atendiendo a un cliente en la silla {i+1}.")
                clientesAtendidos += 1
                break

        sem_sillasAccesibles.release() # Libera el acceso a las sillas

        delay = random.uniform(intervalo_ini, intervalo_fin) # Genera un tiempo de corte aleatorio entre el intervalo
        time.sleep(delay)

        sem_barberoListo.release() # Libera la señal de que el barbero está listo

def cliente():
    global sillasLibres, sillasOcupadas, clientesSeFueron
    for i in range(len(sillasOcupadas)):
        if not sillasOcupadas[i]:
            sem_sillasAccesibles.acquire() # Adquiere el acceso a las sillas
            sillasLibres -= 1
            sillasOcupadas[i] = True
            print(f"Cliente se ha sentado en la silla {i+1}.")
            sem_clientes.release() # Libera la señal de que hay un cliente
            sem_sillasAccesibles.release() # Libera el acceso a las sillas
            sem_barberoListo.acquire() # Espera a que el barbero esté listo
            print(f"Cliente en la silla {i+1} está siendo atendido.")
            break
    else:
        print("No hay sillas disponibles, el cliente se va.")
        clientesSeFueron += 1

def main():
    # Crear el hilo del barbero
    t_barbero = threading.Thread(target=barbero)
    t_barbero.start()

    # Lista de hilos de clientes
    cliente_threads = []

    # Crear los hilos de los clientes
    for _ in range(cantClientes):
        delay = random.uniform(intervalo_ini_llega, intervalo_fin_llega) # Genera un tiempo de llegada aleatorio entre los valores
        time.sleep(delay)
        t_cliente = threading.Thread(target=cliente)
        cliente_threads.append(t_cliente)
        t_cliente.start()

    # Esperar a que todos los hilos de los clientes hayan terminado
    for t in cliente_threads:
        t.join()

    print(f"Clientes atendidos: {clientesAtendidos}")
    print(f"Clientes que se fueron: {clientesSeFueron}")

if opcion == 5:
    main()