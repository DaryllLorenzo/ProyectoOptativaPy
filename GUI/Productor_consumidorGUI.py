import threading
import time
import random
import tkinter as tk
from tkinter import ttk
import os

### GUI DE PRODUCTOR CONSUMIDOR

class ProductorConsumidorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Productor-Consumidor")
        self.master.geometry("720x480")  # Cambiar para modificar el tam

        # Crear estilos personalizados
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 16))
        style.configure("TButton", font=("Helvetica", 16))

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

        self.s1 = threading.Semaphore(self.tamanoBuffer)
        self.s2 = threading.Semaphore(0)
        self.s3 = threading.Semaphore(1)

        self.productor_msg = ""
        self.consumidor_msg = ""

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

        # Redimensionar los frames del GIF con subsample
        self.gif_frames = []
        for i in range(6):
            frame = self.gif_image.subsample(2, 2)  # a mayor valor mas pequeño (4,4) 
            self.gif_frames.append(frame)
            self.gif_image.configure(file=ruta_Prod_GIF, format=f"gif - {i}")

        self.gif_index = 0
        self.gif_label = tk.Label(self.master, image=self.gif_frames[self.gif_index])
        self.gif_label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)
        self.update_gif()

    def update_gif(self):
        self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
        self.gif_label.config(image=self.gif_frames[self.gif_index])
        self.master.after(100, self.update_gif)  # Se actualiza cada 100 ms.


    def load_gif2(self):
        # Cargar el GIF
        ruta_actual2 = os.path.abspath(__file__)
        directorio_actual2 = os.path.dirname(ruta_actual2)
        ruta_Prod_GIF2 = os.path.join(directorio_actual2, "farming-farm.gif")

        # Cargar el GIF
        self.gif_image2 = tk.PhotoImage(file=ruta_Prod_GIF2)

        # Redimensionar los frames del GIF con subsample
        self.gif_frames2 = []
        for i2 in range(6):
            frame2 = self.gif_image2.subsample(3, 3)  # a mayor valor mas pequeño (4,4) 
            self.gif_frames2.append(frame2)
            self.gif_image2.configure(file=ruta_Prod_GIF2, format=f"gif - {i2}")

        self.gif_index2 = 0
        self.gif_label2 = tk.Label(self.master, image=self.gif_frames2[self.gif_index2])
        self.gif_label2.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SW)
        self.update_gif2()

    def update_gif2(self):
        self.gif_index2 = (self.gif_index2 + 1) % len(self.gif_frames2)
        self.gif_label2.config(image=self.gif_frames2[self.gif_index2])
        self.master.after(100, self.update_gif2)  # Se actualiza cada 100 ms.


###############

    def update_buffer_display(self):
        self.buffer_display.config(text=" ".join(self.buffer))
        self.master.update_idletasks()

    def productor(self):
        contador_produccion = 0
        inicio_produccion = time.time()

        while contador_produccion < self.productos:
            dato = "a"
            self.s1.acquire()

            if self.Estatico:
                delay = self.tiempoEstaticoP
            else:
                delay = random.uniform(self.intervalo_iniP, self.intervalo_finP)
            
            mensaje = f" {delay:.2f} segundos para producir "
            self.productor_message_label.config(text=mensaje)  # para actualizar el mensaje del productor

            print(mensaje)
            time.sleep(delay)

            self.bufferLogico.append(dato)

            for i in range(self.tamanoBuffer):
                if self.buffer[i] == "-":
                    self.buffer[i] = "x"
                    self.update_buffer_display()
                    break

            self.s2.release()
            contador_produccion += 1

        fin_produccion = time.time()
        tiempo_total_produccion = fin_produccion - inicio_produccion
        self.productor_msg = f"Tiempo total de producción: {tiempo_total_produccion:.2f} segundos "
        self.productor_message_label.config(text=self.productor_msg)  # SE actualiza el mensaje del productor al finalizar

    def consumidor(self):
        contador_consumo = 0
        inicio_consumo = time.time()

        while contador_consumo < self.productos:
            self.s2.acquire()

            if self.Estatico:
                delay = self.tiempoEstaticoC
            else:
                delay = random.uniform(self.intervalo_iniC, self.intervalo_finC)
            
            mensaje2 = f" {delay:.2f} segundos para consumir  "
            self.consumidor_message_label.config(text=mensaje2)  # Actualiza el mensaje del productor

            print(f"Esperando {delay:.2f} segundos para consumir  ")
            time.sleep(delay)

            self.bufferLogico.pop()

            for i in reversed(range(self.tamanoBuffer)):
                if self.buffer[i] == "x":
                    self.buffer[i] = "-"
                    self.update_buffer_display()
                    break

            self.s1.release()
            contador_consumo += 1

        fin_consumo = time.time()
        tiempo_total_consumo = fin_consumo - inicio_consumo
        self.consumidor_msg = f"Tiempo total de consumo: {tiempo_total_consumo:.2f} segundos"
        self.consumidor_message_label.config(text=self.consumidor_msg)  # Actualiza el mensaje del consumidor al terminar

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

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductorConsumidorApp(root)
    root.mainloop()
