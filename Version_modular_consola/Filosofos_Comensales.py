import threading
import time
import random
import threading
import time
import random

num_filo = 5 # Se define el número de filósofos
tenedores = [threading.Semaphore(1) for _ in range(num_filo)] # Crea una lista de semáforos, uno por cada tenedor, inicializados en 1
cantidad_comidas = 5
intervalo_ini = 0
intervalo_fin = 4

def menu():
    print("")
    print("Parametros: ")
    print("1- Cantidad de filosofos")
    print("2- Simulacion con tiempo random entre intervalos")
    print("3- Cantidad de veces que va a comer cada filosofo")
    print("4- Ejecutar")
    print("5- Ayuda parametros")
    print("6- Salir")

###### parte visual
print("")
print("Problema filosofos-comensales:")
print("Cinco filósofos se sientan alrededor de una mesa y pasan su vida cenando y pensando. Cada filósofo tiene un plato de fideos y un tenedor a la izquierda de su plato. Para comer los fideos son necesarios dos tenedores y cada filósofo sólo puede tomar los que están a su izquierda y derecha. Si cualquier filósofo toma un tenedor y el otro está ocupado, se quedará esperando, con el tenedor en la mano, hasta que pueda tomar el otro tenedor, para luego empezar a comer.")
print("")

print("La aplicacion primeramente esta planteada con parametros de 5 filosofos, un tiempo que demora un valor random comprendido en el intervalo de 0 a 4 para comer y pensar, y cada filosofo va a comer 5 veces")
print("Pero se pueden modificar estos parametros a traves del menu de paramtros")

input("Presiona una tecla para continuar...")

menu()

opcion = int(input("Seleccione una opcion: "))

while opcion != 4 and opcion != 6:
    if opcion == 1:
        print("")
        for _ in range(num_filo):
            tenedores.pop()
        num_filo = int(input("Ingrese el nuevo numero de filosofos: "))
        tenedores = [threading.Semaphore(1) for _ in range(num_filo)]

        menu()
        opcion = int(input("Seleccione una opcion: "))

    elif opcion == 2:
        print("")
        intervalo_ini = float(input("Ingrese el valor inicio del intervalo: "))
        intervalo_fin = float(input("Ingrese el valor fin del intervalo: "))

        menu()
        opcion = int(input("Seleccione una opcion: "))
    elif opcion == 3:
        print("")
        cantidad_comidas = int(input("Ingrese la cantidad de veces que va a comer cada filosofo: "))
        menu()
        opcion = int(input("Seleccione una opcion: "))
    elif opcion == 5:
        print("")
        print("1- Cantidad de filosofos: Cantidad de filosofos que van a estar en la mesa (Tener consideraciones que no esta validado, por lo tanto elegir cuidadosamente acorde a logica si se va a modificar el valor original de 5 filosofos)")
        print("2- Simulacion con tiempo random entre intervalos: Asigna el intervalo y el tiempo de ejecucion del proceso es un valor random compredido en ese intervalo")
        print("3- Cantidad de veces que va a comer cada filosofo: De aqui se saca tambien la estadistica de cuanto tiempo demoró global")
        menu()
        opcion = int(input("Seleccione una opcion: "))

def filosofo(id):
    comidas = 0  # Contador de comidas para cada filósofo
    while comidas < cantidad_comidas:  # Cada filósofo comerá 5 veces en el caso base de ejemplo
        piensa(id)
        levanta_tenedores(id)
        come(id)
        suelta_tenedores(id)
        comidas += 1  # incrementamos el contador de comidas

def piensa(id):
    delay = round(random.uniform(intervalo_ini, intervalo_fin), 2) # simulacion tiempo pensando
    print(f"{id} - Tengo hambre... {delay} segundos")
    time.sleep(delay)

def levanta_tenedores(id):
    if (id % 2 == 0):  # Si el filósofo es zurdo
        tenedor1 = tenedores[id] # tenedor zurdo
        tenedor2 = tenedores[(id + 1) % num_filo] # tenedor a su derecha
    else:  # Si el filósofo es diestro
        tenedor1 = tenedores[(id + 1) % num_filo] # tenedor a su derecha
        tenedor2 = tenedores[id] # tenedor zurdo
    tenedor1.acquire() # Intenta tomar el primer tenedor
    print(f"{id} - Tengo el primer tenedor")
    tenedor2.acquire() # Intenta tomar el segundo tenedor
    print(f"{id} - Tengo ambos tenedores")

def suelta_tenedores(id):
    tenedores[(id + 1) % num_filo].release() # Suelta el segundo tenedor
    tenedores[id].release() # Suelta el primer tenedor
    print(f"{id} - Sigamos pensando...")  # Imprime un mensaje indicando que el filósofo va a seguir pensando

def come(id):
    delay = round(random.uniform(intervalo_ini, intervalo_fin), 2) # simulacion tiempo comiendo
    print(f"{id} - ¡A comer! {delay} segundos")
    time.sleep(delay)  # Simular tiempo de comida

def main():
    start_time = time.time()  # Inicio del cronómetro de tiempo

    filosofos = []
    for i in range(num_filo):  # Crea una lista de hilos, uno por cada filósofo
        fil = threading.Thread(target=filosofo, args=[i])
        filosofos.append(fil)
        fil.start()  # Se inicia cada hilo de ejecución

    for fil in filosofos:
        fil.join()

    end_time = time.time()  # Fin del cronómetro
    total_time = end_time - start_time

    print(f"¡Todos los filósofos han comido {cantidad_comidas} veces! Tardó {total_time:.2f} segundos en total.")
    input("Presione una tecla para terminar ")

if opcion == 4:
    main()