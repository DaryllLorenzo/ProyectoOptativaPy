import threading
import random
import time
from queue import Queue

print("")
print("Daryll Lorenzo Alfonso, programa sistema operativo")
print("VERSION CLI")
print("")
print("MENU: ")
print("1- Problema Productor-consumidor")
print("2- Problema Barbero-dormilón")
print("3- Problema Lectores-escritores")
print("4- Problema Filosofos-comensales")
print("5- Salir")

# Detectar el sistema operativo
#sistema_operativo = platform.system()

#ruta_actual = os.path.abspath(__file__)
#directorio_actual = os.path.dirname(ruta_actual)

op = int(input("Seleccione una opción: "))

if op == 1: # YA OK

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
        input("Pulse una tecla para terminar ")

    if opcion == 5:
        main2Solo()

elif op == 2:
    cant_sillas = 5
    intervalo_ini = 0 # barbero
    intervalo_fin = 4 # barbero
    intervalo_ini_llega = 0 # llega cliente
    intervalo_fin_llega = 2 # llega cliente
    cantClientes = 15

    sem_sillasAccesibles = threading.Semaphore(cant_sillas) # Controla el acceso a las sillas disponibles en la barbería
    sem_clientes = threading.Semaphore(0) # para indicar cuando hay un cliente esperando para ser atendido
    sem_barberoListo = threading.Semaphore(0) # para indicar cuando el barbero ha terminado de atender a un cliente
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
            sem_clientes.acquire() # esperar a que haya un cliente
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
            time.sleep(delay) # simula el tiempo

            sem_barberoListo.release() # Da la señal de que el barbero está listo

    def cliente():
        global sillasLibres, sillasOcupadas, clientesSeFueron
        for i in range(len(sillasOcupadas)):
            if not sillasOcupadas[i]:
                sem_sillasAccesibles.acquire() # Adquiere el acceso a las sillas
                sillasLibres -= 1
                sillasOcupadas[i] = True
                print(f"Cliente se ha sentado en la silla {i+1}.")
                sem_clientes.release() # Da la señal de que hay un cliente
                sem_sillasAccesibles.release() # Da el acceso a las sillas
                sem_barberoListo.acquire() # espera a que el barbero esté listo
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
        input("Presione una tecla para terminar ")

    if opcion == 5:
        main()

elif op == 3:


    ##### LECTOR = 0 ; ESCRITOR = 1
    ## (cantidad de procesos , tipo)
    ### El acquire seria como un down() y el release como un up
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
    print("Problema lectores-escritores:")
    print("Algunos subprocesos pueden leer y otros pueden escribir, con la restricción de que ningún subproceso puede acceder al recurso compartido para leer o escribir mientras otro subproceso está escribiendo en él.(WIKIPEDIA)")
    print("")

    print("La aplicacion primeramente esta planteada con parametros: ")
    print("3 procesos escritores, 2 procesos lectores , 1 proceso escritor, 2 procesos lectores ")
    print("Tiempo dinamico con valor random en el intervalo de 0 a 4 para lo que demora proceso lector")
    print("Tiempo dinamico con valor random en el intervalo de 0 a 4 para lo que demora proceso escritor")


    print("Pero se pueden modificar estos parametros a traves del menu de paramtros")
    input("Presiona una tecla para continuar...")

    menu()
    opcion = int(input("Seleccione una opcion: "))

    while opcion != 4 and opcion != 6:

        if opcion == 1:
            print("")
            tiempoEstaticoL = float(input("Ingrese el valor estatico para el proceso de lector: "))
            tiempoEstaticoE = float(input("Ingrese el valor estatico para el proceso de escritor: "))
            Estatico = True
            menu()
            opcion = int(input("Seleccione una opcion: "))

        elif opcion == 2:
            print("")
            intervalo_iniL = float(input("Ingrese el valor inicio del intervalo para lectores: "))
            intervalo_finL = float(input("Ingrese el valor fin del intervalo para lectores: "))
            intervalo_iniE = float(input("Ingrese el valor inicio del intervalo para escritores: "))
            intervalo_finE = float(input("Ingrese el valor fin del intervalo para escritores: "))
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
        input("Pulse una tecla para terminar ")
    if opcion == 4:   
        main()


elif op == 4: # YA OK
    num_filo = 5 # Define el número de filósofos
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