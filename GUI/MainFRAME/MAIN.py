import threading
import time
import random
import tkinter as tk
from tkinter import ttk
from queue import Queue
import os

# Clase principal de la aplicación
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Problemas de Sincronización")
        self.root.geometry("400x200")

        # Título principal de la aplicación
        tk.Label(root, text="Problemas de Sincronización", font=("Helvetica", 16)).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        # Botones para seleccionar los diferentes problemas de sincronización
        tk.Button(frame, text="Productor-Consumidor", command=self.show_productor_consumidor).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(frame, text="Barbero Dormilón", command=self.show_barbero_dormilon).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(frame, text="Lectores y Escritores", command=self.show_lectores_escritores).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(frame, text="Filósofos Comensales", command=self.show_filosofos_comensales).grid(row=1, column=1, padx=10, pady=10)

    # Funciones para abrir nuevas ventanas con los distintos problemas de sincronización	
    def show_productor_consumidor(self):
        self.new_window(ProductorConsumidorApp, "Productor-Consumidor")

    def show_barbero_dormilon(self):
        self.new_window(BarberoDormilonApp, "Barbero Dormilón")

    def show_lectores_escritores(self):
        self.new_window(LectoresEscritoresApp, "Lectores y Escritores")

    def show_filosofos_comensales(self):
        self.new_window(FilosofosComensalesApp, "Filósofos Comensales")

    def new_window(self, app_class, title):
        new_root = tk.Toplevel(self.root)
        new_root.title(title)
        app_class(new_root)

##########################################################################################################

# Clase para el problema Productor-Consumidor
class ProductorConsumidorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Productor-Consumidor")
        self.master.geometry("720x480")  # modificar para otro tam

        # Crear estilos personalizados para los widget
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 16))
        style.configure("TButton", font=("Helvetica", 16))

        # Inicialización de variables
        self.tamanoBuffer = 10
        self.productos = 10
        self.intervalo_iniP = 0
        self.intervalo_finP = 4
        self.intervalo_iniC = 0
        self.intervalo_finC = 4
        self.Estatico = False
        self.tiempoEstaticoP = None
        self.tiempoEstaticoC = None
        self.checkButtonVar = tk.BooleanVar()

        self.buffer = ["-"] * self.tamanoBuffer
        self.bufferLogico = []

        # Inicialización de semáforos
        self.s1 = threading.Semaphore(self.tamanoBuffer)
        self.s2 = threading.Semaphore(0)
        self.s3 = threading.Semaphore(1)

        self.productor_msg = ""
        self.consumidor_msg = ""

        # Crear widgets de la interfaz
        self.create_widgets()
        self.load_gif()
        self.load_gif2()

    def create_widgets(self):
        self.buffer_label = ttk.Label(self.master, text="Buffer:")
        self.buffer_label.pack(pady=10)

        self.buffer_display = ttk.Label(self.master, text=" ".join(self.buffer))
        self.buffer_display.pack(pady=10)

        self.start_button = ttk.Button(self.master, text="Start", command=self.start)
        self.start_button.pack(pady=10)

        self.edit_button = ttk.Button(self.master, text="Editar Parámetros", command=self.editar_parametros)
        self.edit_button.pack(pady=10)

        # Etiqueta para el mensaje del productor
        self.productor_message_label = ttk.Label(self.master, text="", font=("Helvetica", 13))
        self.productor_message_label.pack(anchor=tk.SW)

        # Etiqueta consumidor
        self.consumidor_message_label = ttk.Label(self.master, text="", font=("Helvetica", 13))
        self.consumidor_message_label.pack(anchor=tk.SE)
        

################
    def load_gif(self):
        # Cargar el GIF
        ruta_actual = os.path.abspath(__file__)
        directorio_actual = os.path.dirname(ruta_actual)
        ruta_Prod_GIF = os.path.join(directorio_actual, "seed-seeding.gif")

		
        # Cargar el GIF
        self.gif_image = tk.PhotoImage(file=ruta_Prod_GIF)

        # Redimensionar los frames del GIF 
        self.gif_frames = []
        for i in range(6):
            frame = self.gif_image.subsample(2, 2)  # Cambiar este valor para ajustar el tamaño de los frames(4,4) mas peque
            self.gif_frames.append(frame)
            self.gif_image.configure(file=ruta_Prod_GIF, format=f"gif - {i}")

        self.gif_index = 0
        self.gif_label = tk.Label(self.master, image=self.gif_frames[self.gif_index])
        self.gif_label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)
        self.update_gif()

    # Funcion para actualizar el gif
    def update_gif(self):
        self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
        self.gif_label.config(image=self.gif_frames[self.gif_index])
        self.master.after(100, self.update_gif)  # Actualiza cada 100 ms.


    def load_gif2(self):
        # Cargar el GIF
        ruta_actual2 = os.path.abspath(__file__)
        directorio_actual2 = os.path.dirname(ruta_actual2)
        ruta_Prod_GIF2 = os.path.join(directorio_actual2, "farming-farm.gif")

        # Cargar el GIF
        self.gif_image2 = tk.PhotoImage(file=ruta_Prod_GIF2)

        # Redimensionar los frames del GIF 
        self.gif_frames2 = []
        for i2 in range(6):
            frame2 = self.gif_image2.subsample(3, 3)  # Cambiar este valor para ajustar el tamaño de los frames(4,4) mas peque
            self.gif_frames2.append(frame2)
            self.gif_image2.configure(file=ruta_Prod_GIF2, format=f"gif - {i2}")

        self.gif_index2 = 0
        self.gif_label2 = tk.Label(self.master, image=self.gif_frames2[self.gif_index2])
        self.gif_label2.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SW)
        self.update_gif2()

    # Funcion para actualizar el gif 2
    def update_gif2(self):
        self.gif_index2 = (self.gif_index2 + 1) % len(self.gif_frames2)
        self.gif_label2.config(image=self.gif_frames2[self.gif_index2])
        self.master.after(100, self.update_gif2)  # Actualiza cada 100 ms.

    # Función para actualizar la visualización del buffer
    def update_buffer_display(self):
        self.buffer_display.config(text=" ".join(self.buffer))
        self.master.update_idletasks()

    # Función del hilo productor
    def productor(self):
        contador_produccion = 0
        inicio_produccion = time.time()

        while contador_produccion < self.productos:
            dato = "a"
            self.s1.acquire() # Adquirir semáforo para el buffer, (lo que es un down() en C )

            # Comprobar si es tiempo estatico
            if self.Estatico:
                delay = self.tiempoEstaticoP
            else:
                delay = random.uniform(self.intervalo_iniP, self.intervalo_finP)
            
            mensaje = f" {delay:.2f} segundos para producir "
            self.productor_message_label.config(text=mensaje)  # Actualiza el mensaje del productor

            print(mensaje)

            # Simula la produccion
            time.sleep(delay)

            # Agregar dato al buffer lógico
            self.bufferLogico.append(dato)

            # Para actualizar el buffer visual
            for i in range(self.tamanoBuffer):
                if self.buffer[i] == "-":
                    self.buffer[i] = "x"
                    self.update_buffer_display()
                    break

            self.s2.release() # Liberar semáforo para el consumidor (release lo que seria un up() en C )
            contador_produccion += 1

        fin_produccion = time.time()
        tiempo_total_produccion = fin_produccion - inicio_produccion
        self.productor_msg = f"Tiempo total de producción: {tiempo_total_produccion:.2f} segundos "
        self.productor_message_label.config(text=self.productor_msg)  # Actualiza el mensaje del productor al terminar

    # Función del hilo consumidor
    def consumidor(self):
        contador_consumo = 0
        inicio_consumo = time.time()

        while contador_consumo < self.productos:
            self.s2.acquire() # Adquirir semáforo del productor

            if self.Estatico:
                delay = self.tiempoEstaticoC
            else:
                delay = random.uniform(self.intervalo_iniC, self.intervalo_finC)
            
            mensaje2 = f" {delay:.2f} segundos para consumir  "
            self.consumidor_message_label.config(text=mensaje2)  # Actualiza el mensaje del productor

            print(f"Esperando {delay:.2f} segundos para consumir  ")
            
            # Simular consumo
            time.sleep(delay)

            self.bufferLogico.pop() # Consume el dato del buffer lógico

            # Actualizar el buffer visual
            for i in reversed(range(self.tamanoBuffer)):
                if self.buffer[i] == "x":
                    self.buffer[i] = "-"
                    self.update_buffer_display()
                    break

            self.s1.release() # Liberar semáforo para el productor
            contador_consumo += 1

        fin_consumo = time.time()
        tiempo_total_consumo = fin_consumo - inicio_consumo
        self.consumidor_msg = f"Tiempo total de consumo: {tiempo_total_consumo:.2f} segundos"
        self.consumidor_message_label.config(text=self.consumidor_msg)  # Actualiza el mensaje del consumidor al finalizar

    # Función para iniciar la simulación
    def start(self):
        self.hilo1 = threading.Thread(target=self.productor)
        self.hilo2 = threading.Thread(target=self.consumidor)
        self.hilo1.start()
        self.hilo2.start()

    def editar_parametros(self):
        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.title("Editar Parámetros")
        self.edit_window.geometry("600x480")

        ttk.Label(self.edit_window, text="Tamaño del Buffer:", font=("Helvetica", 14)).pack(pady=10)
        self.tamano_buffer_entry = tk.Entry(self.edit_window, font=("Helvetica", 14))
        self.tamano_buffer_entry.insert(0, str(self.tamanoBuffer))
        self.tamano_buffer_entry.pack(pady=10)

        ttk.Label(self.edit_window, text="Productos:", font=("Helvetica", 14)).pack(pady=10)
        self.productos_entry = tk.Entry(self.edit_window, font=("Helvetica", 14))
        self.productos_entry.insert(0, str(self.productos))
        self.productos_entry.pack(pady=10)

        # Frame para agrupar param3 y param4 en una fila
        self.param_frame = tk.Frame(self.edit_window)
        self.param_frame.pack(pady=10)

        # Etiqueta y entrada para param3
        self.param3_label = ttk.Label(self.param_frame, text="TEP:", font=("Helvetica", 14))
        self.param3_label.pack(side=tk.LEFT, padx=(0, 10))  # Alineado a la izquierda con espacio a la derecha

        self.checkEstatico = ttk.Checkbutton(self.param_frame, text="Estatico", variable=self.checkButtonVar)
        self.checkEstatico.pack(side=tk.LEFT, padx=(0,20))

        # tiempo estatico del productor
        self.TEP_entry = tk.Entry(self.param_frame, font=("Helvetica", 14), width=10)  # Ajustar el ancho del campo
        self.TEP_entry.insert(0, str(self.tiempoEstaticoP))
        self.TEP_entry.pack(side=tk.LEFT, padx=(0, 20))  # Alineado a la izquierda con espacio a la derecha

        # Etiqueta y entrada para param4
        self.param4_label = ttk.Label(self.param_frame, text="TEC:", font=("Helvetica", 14))
        self.param4_label.pack(side=tk.LEFT, padx=(0, 10))  # Alineado a la izquierda con espacio a la derecha

        self.TEC_entry = tk.Entry(self.param_frame, font=("Helvetica", 14), width=10)  # Ajustar el ancho del campo
        self.TEC_entry.insert(0, str(self.tiempoEstaticoC))
        self.TEC_entry.pack(side=tk.LEFT, padx=(0, 20))  # Alineado a la izquierda con espacio a la derecha

        # Frame para agrupar param5 y param6 en una nueva fila
        self.param_frame2 = tk.Frame(self.edit_window)
        self.param_frame2.pack(pady=10)

        # Etiqueta y entrada para param5
        self.param5_label = ttk.Label(self.param_frame2, text="InicioP:", font=("Helvetica", 14))
        self.param5_label.pack(side=tk.LEFT, padx=(0, 10))  # Alineado a la izquierda con espacio a la derecha

        self.TDIP_entry = tk.Entry(self.param_frame2, font=("Helvetica", 14), width=10)  # Ajustar el ancho del campo
        self.TDIP_entry.insert(0, str(self.intervalo_iniP))
        self.TDIP_entry.pack(side=tk.LEFT, padx=(0, 20))  # Alineado a la izquierda con espacio a la derecha

        # Etiqueta y entrada para param6
        self.param6_label = ttk.Label(self.param_frame2, text="FinP:", font=("Helvetica", 14))
        self.param6_label.pack(side=tk.LEFT, padx=(0, 10))  # Alineado a la izquierda con espacio a la derecha

        self.TDFP_entry = tk.Entry(self.param_frame2, font=("Helvetica", 14), width=10)  # Ajustar el ancho del campo
        self.TDFP_entry.insert(0, str(self.intervalo_finP))
        self.TDFP_entry.pack(side=tk.LEFT, padx=(0, 20))  # Alineado a la izquierda con espacio a la derecha


        # Frame para agrupar param7 y param8 en una nueva fila
        self.param_frame3 = tk.Frame(self.edit_window)
        self.param_frame3.pack(pady=10)

        # Etiqueta y entrada para param7
        self.param7_label = ttk.Label(self.param_frame3, text="InicioC:", font=("Helvetica", 14))
        self.param7_label.pack(side=tk.LEFT, padx=(0, 10))  # Alineado a la izquierda con espacio a la derecha

        self.TDIC_entry = tk.Entry(self.param_frame3, font=("Helvetica", 14), width=10)  # Ajustar el ancho del campo
        self.TDIC_entry.insert(0, str(self.intervalo_iniC))
        self.TDIC_entry.pack(side=tk.LEFT, padx=(0, 20))  # Alineado a la izquierda con espacio a la derecha

        # Etiqueta y entrada para param8
        self.param8_label = ttk.Label(self.param_frame3, text="FinC:", font=("Helvetica", 14))
        self.param8_label.pack(side=tk.LEFT, padx=(0, 10))  # Alineado a la izquierda con espacio a la derecha

        self.TDFC_entry = tk.Entry(self.param_frame3, font=("Helvetica", 14), width=10)  # Ajustar el ancho del campo
        self.TDFC_entry.insert(0, str(self.intervalo_finC))
        self.TDFC_entry.pack(side=tk.LEFT, padx=(0, 20))  # Alineado a la izquierda con espacio a la derecha


        ttk.Button(self.edit_window, text="Guardar", command=self.guardar_parametros, style="TButton").pack(pady=10)
        ttk.Button(self.edit_window, text="Cerrar", command=self.edit_window.destroy, style="TButton").pack(pady=10)
        
    def guardar_parametros(self):
        self.tamanoBuffer = int(self.tamano_buffer_entry.get())
        self.productos = int(self.productos_entry.get())
        self.buffer = ["-"] * self.tamanoBuffer
        self.bufferLogico = []
        self.s1 = threading.Semaphore(self.tamanoBuffer)
        self.s2 = threading.Semaphore(0)

        self.tiempoEstaticoP = None
        self.tiempoEstaticoC = None

        self.Estatico = self.checkButtonVar.get()


        if self.Estatico is True:
            self.tiempoEstaticoP = float(self.TEP_entry.get())
            self.tiempoEstaticoC = float(self.TEC_entry.get())
        
        self.intervalo_iniP = float(self.TDIP_entry.get())
        self.intervalo_finP = float(self.TDFP_entry.get())
        self.intervalo_iniC = float(self.TDIC_entry.get())
        self.intervalo_finC = float(self.TDFC_entry.get())

        self.update_buffer_display()
        self.edit_window.destroy()

        # Refrescar la ventana principal
        self.update_buffer_display()

############################################################################################################

# Clase para el problema del Barbero-dormilon
class BarberoDormilonApp:
    def __init__(self, root):

        # Inicialización de variables
        self.sillasLibres = 5 # Número de sillas disponibles en la barbería
        self.sillasOcupadas = [False] * self.sillasLibres # Estado de las sillas (False: libre, True: ocupada)
        self.clientesAtendidos = 0 # Contador de clientes atendidos
        self.clientesSeFueron = 0 # Contador de clientes que se fueron sin ser atendidos
        self.intervalo_ini = 1 # Tiempo mínimo de corte de pelo
        self.intervalo_fin = 4 # Tiempo máximo de corte de pelo
        self.intervalo_ini_llega = 0.5 # Tiempo mínimo entre llegadas de clientes
        self.intervalo_fin_llega = 1 # Tiempo máximo entre llegadas de clientes
        self.cantClientes = 10 # Cantidad de clientes en total

        # Inicializacion Semáforos
        self.sem_clientes = threading.Semaphore(0) # Semáforo para contar clientes esperando
        self.sem_sillasAccesibles = threading.Semaphore(1) # Semáforo para controlar acceso a sillas
        self.sem_barberoListo = threading.Semaphore(0) # Semáforo para indicar que el barbero está listo

        self.simulation_running = False # Estado de la simulación

        # Crear la interfaz gráfica
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Creacion de etiquetas de sillas (Eliminamos las etiquetas anteriores)
        for widget in self.root.pack_slaves():
            if isinstance(widget, tk.Label) and widget not in [self.atendidos_label, self.se_fueron_label, self.barbero_status_label]:
                widget.pack_forget()

        # Etiqueta para mostrar clientes atendidos
        self.atendidos_label = tk.Label(self.root, text=f"Clientes atendidos: {self.clientesAtendidos}")
        self.atendidos_label.pack()

        # Etiqueta para mostrar clientes que se fueron
        self.se_fueron_label = tk.Label(self.root, text=f"Clientes que se fueron: {self.clientesSeFueron}")
        self.se_fueron_label.pack()

        # Etiqueta para mostrar el estado del barbero
        self.barbero_status_label = tk.Label(self.root, text="Barbero: Durmiendo")
        self.barbero_status_label.pack()

        # Crear frame para el log de eventos
        log_frame = tk.Frame(self.root)
        log_frame.pack(padx=10, pady=10)

        # Área de texto para el log
        self.log_text = tk.Text(log_frame, state='disabled', height=15, width=60)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar para el log
        log_scroll = tk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el área de texto con el scroll
        self.log_text.config(yscrollcommand=log_scroll.set)

        # Botón para iniciar la simulación
        start_button = tk.Button(self.root, text="Start", command=self.start_simulation)
        start_button.pack()

        # Botón para editar los parámetros
        edit_button = tk.Button(self.root, text="Editar Parámetros", command=self.edit_parameters)
        edit_button.pack()

        # Crear etiquetas para cada silla
        self.sillas_labels = [tk.Label(self.root, text=f"Silla {i+1}: Libre") for i in range(self.sillasLibres)]
        for label in self.sillas_labels:
            label.pack()

    # Función para el comportamiento de barbero
    def barbero(self):
        while self.simulation_running:
            self.sem_clientes.acquire() # Esperar a que lleguen clientes
            self.sem_sillasAccesibles.acquire() # Bloquear acceso a las sillas
            for i in range(len(self.sillasOcupadas)):
                if self.sillasOcupadas[i]:
                    self.sillasLibres += 1 # Liberar una silla
                    self.sillasOcupadas[i] = False # Marcar silla como libre
                    self.update_sillas_solo_nombres() # Actualizar interfaz gráfica
                    self.clientesAtendidos += 1 # Incrementar contador de clientes atendidos
                    self.update_labels() # Actualizar etiquetas en la interfaz
                    self.log_event(f"Barbero: Atendiendo al cliente en silla {i+1}")
                    break
            self.sem_sillasAccesibles.release() # Liberar acceso a las sillas
            delay = random.uniform(self.intervalo_ini, self.intervalo_fin) # Tiempo de corte de pelo
            self.log_event(f"Barbero: Terminando de atender en {delay:.2f} segundos")
            self.barbero_status_label.config(text=f"Barbero: Atendiendo cliente ({delay:.2f}s)")
            time.sleep(delay) # Simular tiempo de corte de pelo
            self.sem_barberoListo.release() # Indicar que el barbero está listo para el próximo cliente
            self.barbero_status_label.config(text="Barbero: Durmiendo")

    # Función que simula la llegada de un cliente
    def cliente(self):
        self.log_event("Cliente: Llega a la barbería")
        self.sem_sillasAccesibles.acquire() # Bloquear acceso a las sillas
        for i in range(len(self.sillasOcupadas)):
            if not self.sillasOcupadas[i]:
                self.sillasLibres -= 1 # Ocupa una silla
                self.sillasOcupadas[i] = True # Marcar silla como ocupada
                self.update_sillas_solo_nombres() # Actualizar interfaz gráfica
                self.log_event(f"Cliente: Se sienta en la silla {i+1}") 
                self.sem_clientes.release() # Avisar al barbero que hay un cliente
                self.sem_sillasAccesibles.release() # Liberar acceso a las sillas
                self.sem_barberoListo.acquire() # Esperar a que el barbero esté listo
                return
        self.sem_sillasAccesibles.release() # Liberar acceso a las sillas si no hay espacio
        self.clientesSeFueron += 1 # Incrementa contador de clientes que se fueron
        self.update_labels() # Actualizar etiquetas en la interfaz
        self.log_event("Cliente: Se va porque la barbería está llena")

    # Función principal que maneja la simulación
    def main(self):
        self.simulation_running = True # Indicar que la simulación está ejecutandose
        t_barbero = threading.Thread(target=self.barbero) # Crear hilo para el barbero
        t_barbero.start() # Iniciar el hilo del barbero

        cliente_threads = []
        for _ in range(self.cantClientes):
            if not self.simulation_running:
                break
            delay = random.uniform(self.intervalo_ini_llega, self.intervalo_fin_llega) # Tiempo entre llegadas de clientes
            time.sleep(delay)
            t_cliente = threading.Thread(target=self.cliente) # Crear hilo para el cliente
            cliente_threads.append(t_cliente) # Añadir hilo a la lista de hilos de clientes
            t_cliente.start() # Iniciar el hilo del cliente

        for t in cliente_threads:
            t.join() # Esperar a que todos los hilos de clientes terminen

        self.simulation_running = False # Para indicar que la simulación ha terminado
        self.log_event(f"Clientes atendidos: {self.clientesAtendidos}")
        self.log_event(f"Clientes que se fueron: {self.clientesSeFueron}")

    # Función para iniciar la simulación
    def start_simulation(self):
        if not self.simulation_running:
            self.reset_simulation()
            threading.Thread(target=self.main).start()

    def edit_parameters(self):
        def save_parameters():
            self.sillasLibres = int(sillasLibres_var.get())
            self.intervalo_ini = float(intervalo_ini_var.get())
            self.intervalo_fin = float(intervalo_fin_var.get())
            self.intervalo_ini_llega = float(intervalo_ini_llega_var.get())
            self.intervalo_fin_llega = float(intervalo_fin_llega_var.get())
            self.cantClientes = int(cantClientes_var.get())

            self.sillasOcupadas = [False] * self.sillasLibres

            # Reiniciar la interfaz con los nuevos parámetros
            self.reset_simulation()
            self.update_sillas()
            self.update_labels()

            param_window.destroy()

        param_window = tk.Toplevel(self.root)
        param_window.title("Editar Parámetros")

        sillasLibres_var = tk.StringVar(value=str(self.sillasLibres))
        intervalo_ini_var = tk.StringVar(value=str(self.intervalo_ini))
        intervalo_fin_var = tk.StringVar(value=str(self.intervalo_fin))
        intervalo_ini_llega_var = tk.StringVar(value=str(self.intervalo_ini_llega))
        intervalo_fin_llega_var = tk.StringVar(value=str(self.intervalo_fin_llega))
        cantClientes_var = tk.StringVar(value=str(self.cantClientes))

        tk.Label(param_window, text="Sillas libres:").pack()
        tk.Entry(param_window, textvariable=sillasLibres_var).pack()

        tk.Label(param_window, text="Intervalo inicial de corte:").pack()
        tk.Entry(param_window, textvariable=intervalo_ini_var).pack()

        tk.Label(param_window, text="Intervalo final de corte:").pack()
        tk.Entry(param_window, textvariable=intervalo_fin_var).pack()

        tk.Label(param_window, text="Intervalo inicial de llegada:").pack()
        tk.Entry(param_window, textvariable=intervalo_ini_llega_var).pack()

        tk.Label(param_window, text="Intervalo final de llegada:").pack()
        tk.Entry(param_window, textvariable=intervalo_fin_llega_var).pack()

        tk.Label(param_window, text="Cantidad de clientes:").pack()
        tk.Entry(param_window, textvariable=cantClientes_var).pack()

        tk.Button(param_window, text="Guardar", command=save_parameters).pack()

    def reset_simulation(self):
        self.clientesAtendidos = 0
        self.clientesSeFueron = 0
        self.update_labels()
        self.sem_clientes = threading.Semaphore(0)
        self.sem_sillasAccesibles = threading.Semaphore(1)
        self.sem_barberoListo = threading.Semaphore(0)

    def update_sillas_solo_nombres(self):
        for i in range(len(self.sillasOcupadas)):
            if self.sillasOcupadas[i]:
                self.sillas_labels[i].config(text=f"Silla {i+1}: Ocupada")
            else:
                self.sillas_labels[i].config(text=f"Silla {i+1}: Libre")

    def update_sillas(self):
        # Borrar las etiquetas de sillas antiguas
        for widget in self.root.pack_slaves():
            if isinstance(widget, tk.Label) and widget not in [self.atendidos_label, self.se_fueron_label, self.barbero_status_label]:
                widget.pack_forget()

        # Re-crear etiquetas basadas en el número de sillasLibres
        self.sillas_labels = [tk.Label(self.root, text=f"Silla {i+1}: Libre") for i in range(self.sillasLibres)]
        for label in self.sillas_labels:
            label.pack()

    def update_labels(self):
        self.atendidos_label.config(text=f"Clientes atendidos: {self.clientesAtendidos}")
        self.se_fueron_label.config(text=f"Clientes que se fueron: {self.clientesSeFueron}")

    def log_event(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.yview(tk.END)

#######################################################################################################################

# Clase para el problema de Lectores-escritores
class LectoresEscritoresApp: 
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")

        # Inicializar las colas y parámetros
        self.cola_creacion = Queue()
        self.mutex = threading.Semaphore(1) # Semáforo para controlar el acceso mutuo a la sección crítica
        self.cuarto_vacio = threading.Semaphore(1) # Semáforo para controlar el acceso al cuarto cuando no hay escritores
        self.mecanismo_control = threading.Semaphore(1) # Semáforo para controlar el acceso al cuarto cuando hay lectores y escritores
        self.lectores = 0 # Contador de lectores, inicialmente en 0
        
        # Variables para los intervalos de tiempo
        self.intervalo_iniL = tk.DoubleVar(value=0)
        self.intervalo_finL = tk.DoubleVar(value=4)
        self.intervalo_iniE = tk.DoubleVar(value=0)
        self.intervalo_finE = tk.DoubleVar(value=4)
        self.tiempoEstaticoL = tk.DoubleVar(value=0)
        self.tiempoEstaticoE = tk.DoubleVar(value=0)
        self.Estatico = tk.BooleanVar(value=False)

        # Inicializar la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Campos para los intervalos de tiempo de los lectores
        tk.Label(frame, text="Intervalo Lectores (inicio, fin)").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.intervalo_iniL).grid(row=0, column=1)
        tk.Entry(frame, textvariable=self.intervalo_finL).grid(row=0, column=2)

        # Campos para los intervalos de tiempo de los escritores
        tk.Label(frame, text="Intervalo Escritores (inicio, fin)").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.intervalo_iniE).grid(row=1, column=1)
        tk.Entry(frame, textvariable=self.intervalo_finE).grid(row=1, column=2)

        # Campos para el tiempo estático de los lectores
        tk.Label(frame, text="Tiempo Estático Lector").grid(row=2, column=0)
        tk.Entry(frame, textvariable=self.tiempoEstaticoL).grid(row=2, column=1)

        # Campos para el tiempo estático de los escritores
        tk.Label(frame, text="Tiempo Estático Escritor").grid(row=3, column=0)
        tk.Entry(frame, textvariable=self.tiempoEstaticoE).grid(row=3, column=1)

        # Checkbox para activar el modo estático
        tk.Checkbutton(frame, text="Estatico", variable=self.Estatico).grid(row=4, columnspan=2)

        # Botones para interactuar con la cola de procesos y la simulación
        tk.Button(frame, text="Agregar Procesos", command=self.mostrar_dialogo_procesos).grid(row=5, columnspan=3)
        tk.Button(frame, text="Vaciar Cola", command=self.vaciar_cola).grid(row=6, columnspan=3)
        tk.Button(frame, text="Iniciar", command=self.iniciar_procesos).grid(row=7, columnspan=3)
        tk.Button(frame, text="Ver Cola", command=self.ver_cola).grid(row=8, columnspan=3)

        # frame para guardar el Text y el Scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(padx=10, pady=10)

        self.text = tk.Text(text_frame, state='disabled', height=10, width=50)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(text_frame, command=self.text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text.config(yscrollcommand=scroll.set)

    # Mostrar un dialogo(como JDialog de Java) para agregar procesos a la cola
    def mostrar_dialogo_procesos(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Agregar Procesos")

        tk.Label(dialogo, text="Cantidad de procesos a crear:").grid(row=0, column=0)
        cantidad_var = tk.IntVar()
        tk.Entry(dialogo, textvariable=cantidad_var).grid(row=0, column=1)

        tk.Label(dialogo, text="Tipo de proceso (0 = lectores, 1 = escritores):").grid(row=1, column=0)
        tipo_var = tk.IntVar()
        tk.Entry(dialogo, textvariable=tipo_var).grid(row=1, column=1)

        # Agregar los procesos a la cola (es una cola de tuplas (cantidad de procesos , tipo de proceso [0-lector; 1-escritor] ))
        def agregar_procesos():
            p1 = cantidad_var.get()
            p2 = tipo_var.get()
            elemento = (p1, p2)
            self.cola_creacion.put(elemento)
            self.log(f"Agregado {p1} {'lectores' if p2 == 0 else 'escritores'} a la cola")
            dialogo.destroy()

        tk.Button(dialogo, text="Agregar", command=agregar_procesos).grid(row=2, columnspan=2)

    # Vaciar la cola de procesos
    def vaciar_cola(self):
        with self.cola_creacion.mutex:
            self.cola_creacion.queue.clear()
        self.log("Se ha vaciado la cola de procesos")
        self.mostrar_dialogo_procesos()

    def iniciar_procesos(self):
        self.text.configure(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.configure(state='disabled')

        self.estatico = self.Estatico.get()
        intervalo_iniL = self.intervalo_iniL.get()
        intervalo_finL = self.intervalo_finL.get()
        intervalo_iniE = self.intervalo_iniE.get()
        intervalo_finE = self.intervalo_finE.get()
        tiempoEstaticoL = self.tiempoEstaticoL.get()
        tiempoEstaticoE = self.tiempoEstaticoE.get()

        # Función para los escritores
        def escritor():
            self.mecanismo_control.acquire() # Adquirir el mecanismo_control para acceder al cuarto
            self.cuarto_vacio.acquire() # Adquirir el cuarto para escritura
            if self.estatico:
                delay = tiempoEstaticoE
            else:
                delay = random.uniform(intervalo_iniE, intervalo_finE)
            self.log(f"Escritor escribiendo {delay:.2f} segundos para terminar")
            time.sleep(delay) # Simular la escritura
            self.cuarto_vacio.release() # Liberar el cuarto después de la escritura
            self.mecanismo_control.release() # Liberar el mecanismo_control para permitir el acceso de otros

        # Función para los lectores
        def lector():
            self.mecanismo_control.acquire() # Adquirir el mecanismo_control para acceder al cuarto
            self.mecanismo_control.release() # Liberar el mecanismo_control
            self.mutex.acquire() # Adquirir el mutex para acceder a la sección crítica
            self.lectores += 1 # Incrementar el contador de lectores
            if self.lectores == 1: # Si es el primer lector
                self.cuarto_vacio.acquire() # Adquirir el cuarto para la lectura
            self.mutex.release() # Liberar el mutex
            if self.estatico:
                delay = tiempoEstaticoL
            else:
                delay = random.uniform(intervalo_iniL, intervalo_finL)
            self.log(f"Lector leyendo {delay:.2f} segundos para terminar")
            time.sleep(delay) # Simular lectura
            
            self.mutex.acquire() # Adquirir el mutex para acceder a la sección crítica
            self.lectores -= 1 # Decrementar el contador de lectores
            if self.lectores == 0: # Si no hay más lectores
                self.cuarto_vacio.release() # Liberar el cuarto para permitir la escritura
            self.mutex.release() # Liberar el mutex

        # Función principal para iniciar los hilos de los procesos
        def main():
            start_time = time.time()
            size = self.cola_creacion.qsize()
            threads = []
            for _ in range(size):
                tupla_temp = self.cola_creacion.get()
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
            for t in threads:
                t.join()
            end_time = time.time()
            total_time = end_time - start_time
            self.log(f"El tiempo total de ejecución de todos los procesos fue de {total_time:.2f} segundos.")

        threading.Thread(target=main).start()

    def ver_cola(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Ver Cola")

        frame = tk.Frame(dialogo)
        frame.pack(padx=10, pady=10)

        text = tk.Text(frame, state='normal', height=10, width=50)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(frame, command=text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        text.config(yscrollcommand=scroll.set)

        with self.cola_creacion.mutex:
            for item in list(self.cola_creacion.queue):
                p1, p2 = item
                text.insert(tk.END, f"{p1} {'lectores' if p2 == 0 else 'escritores'}\n")
        
        text.configure(state='disabled')

    def log(self, message):
        self.text.configure(state='normal')
        self.text.insert(tk.END, message + "\n")
        self.text.configure(state='disabled')

#############################################################################################################

# Clase para el problema de Filosofos-comensales
class FilosofosComensalesApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x400")
        self.root.title("Problema de los Filósofos Comensales")
        self.root.configure(bg='white')
        
        # Inicializar variables
        self.num_filo = 5 # Número de filósofos
        self.cantidad_comidas = 5 # Cantidad de veces que cada filósofo debe comer
        self.intervalo_ini = 1 # Tiempo mínimo de espera
        self.intervalo_fin = 3 # Tiempo máximo de espera
        self.estados = ['Pensando'] * self.num_filo # Estado inicial de cada filósofo
        self.comidas_contador = [0] * self.num_filo # Contador de comidas por filósofo
        self.tenedores = [threading.Lock() for _ in range(self.num_filo)] # Inicialización de los tenedores (lock)
        
        self.estado_labels = []
        self.png_animators = []

        self.init_ui()

    def init_ui(self):
        # Crear etiquetas para los estados de los filósofos
        self.estado_labels = [tk.Label(self.root, text=f'Filósofo {i + 1}: Pensando', bg='white', font=('Helvetica', 10)) for i in range(self.num_filo)]
        for label in self.estado_labels:
            label.pack()

        # Botón para iniciar la simulación
        self.start_button = tk.Button(self.root, text="Start", command=self.start_simulation)
        self.start_button.pack()

        # Botón para editar parámetros
        self.edit_button = tk.Button(self.root, text="Editar Parámetros", command=self.edit_parameters)
        self.edit_button.pack()

        # Etiqueta para mostrar resultados
        self.resultado_label = tk.Label(self.root, text="", bg='white', font=('Helvetica', 11))
        self.resultado_label.pack(pady=10)

        # Directorios a las secuencias de imágenes PNG
        self.ruta_actual = os.path.abspath(__file__)
        self.directorio_actual = os.path.dirname(self.ruta_actual)

        # Inicializar animadores de imágenes para cada filósofo
        self.png_animators = [self.PNGAnimator(self.root, self.directorio_actual, 5, 20 + i * 150, 200, i, self.comidas_contador) for i in range(self.num_filo)]

    # Clase para animar los png
    class PNGAnimator:
        def __init__(self, master, img_dir, num_frames, x, y, id, comidas_contador):
            self.master = master
            # Cargar frames de animación
            self.frames = [tk.PhotoImage(file=os.path.join(img_dir, f"RSC_{i}.png")).subsample(2, 2) for i in range(num_frames)]
            self.frame_index = 0
            self.label = tk.Label(master, image=self.frames[self.frame_index], bg=master['bg'])  # Para ajustar color de fondo
            self.label.place(x=x, y=y + 20)
            self.state_label = tk.Label(master, text=f'F {id + 1}: Pensando', bg=master['bg'], font=('Helvetica', 8))
            self.state_label.place(x=x, y=y)
            self.counter_label = tk.Label(master, text=f'Comidas: {comidas_contador[id]}', bg=master['bg'], font=('Helvetica', 10))
            self.counter_label.place(x=x, y=y + 150)
            self.running = False

        # Método para iniciar la animación
        def start(self):
            self.running = True
            self.update_frame()

        # Método para detener la animación
        def stop(self):
            self.running = False

        # Método para actualizar el frame de la animación
        def update_frame(self):
            if self.running:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.label.config(image=self.frames[self.frame_index])
                self.master.after(100, self.update_frame)

        # Método para actualizar el estado del filósofo
        def update_state(self, estado):
            self.state_label.config(text=estado)

        # Método para actualizar el contador de comidas
        def update_counter(self, contador):
            self.counter_label.config(text=f'Comidas: {contador+1}')

    # Método principal del filósofo
    def filosofo(self, id):
        comidas = 0 # Contador de comidas para cada filósofo
        while comidas < self.cantidad_comidas: # Cada filósofo comerá 5 veces en el caso base de ejemplo
            self.piensa(id)
            self.levanta_tenedores(id)
            self.come(id)
            self.suelta_tenedores(id)
            comidas += 1 # incrementamos el contador de comidas
            self.comidas_contador[id] = comidas
            self.actualizar_estado(id, 'Pensando')

    # Método para simular el pensamiento del filósofo
    def piensa(self, id):
        delay = round(random.uniform(self.intervalo_ini, self.intervalo_fin), 2)
        self.actualizar_estado(id, f'Hambriento ({delay}s)')
        time.sleep(delay)

    # Método para levantar los tenedores
    def levanta_tenedores(self, id):
        if (id % 2 == 0): # Si el filósofo es zurdo
            tenedor1 = self.tenedores[id] # tenedor zurdo
            tenedor2 = self.tenedores[(id + 1) % self.num_filo] # tenedor a su derecha
        else: # Si el filósofo es diestro
            tenedor1 = self.tenedores[(id + 1) % self.num_filo] # tenedor a su derecha
            tenedor2 = self.tenedores[id] # tenedor zurdo
        tenedor1.acquire() #Intenta tomar el primer tenedo
        self.actualizar_estado(id, 'Toma el 1er tenedor')
        tenedor2.acquire() #Intenta tomar el segundo tenedor
        self.actualizar_estado(id, 'Toma los 2 tenedores')

    # Método para soltar los tenedores
    def suelta_tenedores(self, id): 
        self.tenedores[(id + 1) % self.num_filo].release() # Suelta el segundo tenedor
        self.tenedores[id].release() # Suelta el primer tenedor
        self.actualizar_estado(id, 'Pensando') 

    # Método para simular la acción de comer del filósofo
    def come(self, id):
        delay = round(random.uniform(self.intervalo_ini, self.intervalo_fin), 2)
        self.actualizar_estado(id, f'Comiendo ({delay}s)')
        self.png_animators[id].start()  # Iniciar la animación de la secuencia de imágenes
        time.sleep(delay)
        self.png_animators[id].stop()  # Detener la animación de la secuencia de imágenes
        self.actualizar_comidas(id, self.comidas_contador[id])

    # Método para actualizar el estado del filósofo en la interfaz
    def actualizar_estado(self, id, estado):
        self.estados[id] = estado
        self.estado_labels[id].config(text=f'Filósofo {id + 1}: {estado}')
        self.png_animators[id].update_state(f'F {id + 1}: {estado}')

    # Método para actualizar el contador de comidas en la interfaz
    def actualizar_comidas(self, id, contador):
        self.comidas_contador[id] = contador
        self.png_animators[id].update_counter(contador)

    # Método para iniciar la simulación
    def start_simulation(self):
        threading.Thread(target=self.main).start()

    def edit_parameters(self):
        def save_parameters():
            self.cantidad_comidas = int(cantidad_comidas_var.get())
            self.intervalo_ini = float(intervalo_ini_var.get())
            self.intervalo_fin = float(intervalo_fin_var.get())
            param_window.destroy()

        param_window = tk.Toplevel(self.root)
        param_window.title("Editar Parámetros")

        cantidad_comidas_var = tk.StringVar(value=str(self.cantidad_comidas))
        intervalo_ini_var = tk.StringVar(value=str(self.intervalo_ini))
        intervalo_fin_var = tk.StringVar(value=str(self.intervalo_fin))

        tk.Label(param_window, text="Cantidad de comidas:").pack()
        tk.Entry(param_window, textvariable=cantidad_comidas_var).pack()

        tk.Label(param_window, text="Intervalo inicial:").pack()
        tk.Entry(param_window, textvariable=intervalo_ini_var).pack()

        tk.Label(param_window, text="Intervalo final:").pack()
        tk.Entry(param_window, textvariable=intervalo_fin_var).pack()

        tk.Button(param_window, text="Guardar", command=save_parameters).pack()

    # Método para actualizar la interfaz después de cambiar los parámetros
    def actualizar_interfaz(self):
        for label in self.estado_labels:
            label.destroy()
        self.estado_labels = [tk.Label(self.root, text=f'Filósofo {i + 1}: Pensando', bg=self.root['bg'], font=('Helvetica', 10)) for i in range(self.num_filo)]
        for label in self.estado_labels:
            label.pack()
        for animator in self.png_animators:
            animator.label.destroy()
            animator.state_label.destroy()
            animator.counter_label.destroy()
        self.png_animators = [self.PNGAnimator(self.root, self.directorio_actual, 5, 20 + i * 150, 200, i, self.comidas_contador) for i in range(self.num_filo)]

    # Método principal para iniciar y controlar los hilos de los filósofos
    def main(self):
        start_time = time.time()

        filosofos = []
        for i in range(self.num_filo):
            fil = threading.Thread(target=self.filosofo, args=[i])
            filosofos.append(fil)
            fil.start()

        for fil in filosofos:
            fil.join()

        end_time = time.time()
        total_time = end_time - start_time

        print(f"Todos los filósofos han comido {self.cantidad_comidas} veces. Demoró {total_time:.2f} segundos en total.")
        self.resultado_label.config(text=f"Todos los filósofos han comido {self.cantidad_comidas} veces. Demoró {total_time:.2f} segundos en total.")

###########################################################################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
