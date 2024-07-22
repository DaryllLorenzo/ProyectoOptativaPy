import threading
import random
import time
import tkinter as tk
import os

# Variables globales
num_filo = 5
cantidad_comidas = 5
intervalo_ini = 1
intervalo_fin = 3
estados = ['Pensando'] * num_filo
comidas_contador = [0] * num_filo
tenedores = [threading.Lock() for _ in range(num_filo)]

# Clase para animar una secuencia de imágenes PNG
class PNGAnimator:
    def __init__(self, master, img_dir, num_frames, x, y, id):
        self.master = master
        self.frames = [tk.PhotoImage(file=os.path.join(img_dir, f"RSC_{i}.png")).subsample(2, 2) for i in range(num_frames)]
        self.frame_index = 0
        self.label = tk.Label(master, image=self.frames[self.frame_index], bg=root['bg'])  # Para ajustar color de fondo
        self.label.place(x=x, y=y + 20)
        self.state_label = tk.Label(master, text=f'F {id + 1}: Pensando', bg=root['bg'], font=('Helvetica', 8))
        self.state_label.place(x=x, y=y)
        self.counter_label = tk.Label(master, text=f'Comidas: {comidas_contador[id]}', bg=root['bg'], font=('Helvetica', 10))
        self.counter_label.place(x=x, y=y + 150)
        self.running = False

    def start(self):
        self.running = True
        self.update_frame()

    def stop(self):
        self.running = False

    def update_frame(self):
        if self.running:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.label.config(image=self.frames[self.frame_index])
            self.master.after(100, self.update_frame)

    def update_state(self, estado):
        self.state_label.config(text=estado)

    def update_counter(self, contador):
        self.counter_label.config(text=f'Comidas: {contador+1}')

# Funciones de los filósofos
def filosofo(id):
    comidas = 0
    while comidas < cantidad_comidas:
        piensa(id)
        levanta_tenedores(id)
        come(id)
        suelta_tenedores(id)
        comidas += 1
        comidas_contador[id] = comidas
        actualizar_estado(id, 'Pensando')

def piensa(id):
    delay = round(random.uniform(intervalo_ini, intervalo_fin), 2)
    actualizar_estado(id, f'Hambriento ({delay}s)')
    time.sleep(delay)

def levanta_tenedores(id):
    if (id % 2 == 0):
        tenedor1 = tenedores[id]
        tenedor2 = tenedores[(id + 1) % num_filo]
    else:
        tenedor1 = tenedores[(id + 1) % num_filo]
        tenedor2 = tenedores[id]
    tenedor1.acquire()
    actualizar_estado(id, 'Toma el 1er tenedor')
    tenedor2.acquire()
    actualizar_estado(id, 'Toma los 2 tenedores')

def suelta_tenedores(id):
    tenedores[(id + 1) % num_filo].release()
    tenedores[id].release()
    actualizar_estado(id, 'Pensando')

def come(id):
    delay = round(random.uniform(intervalo_ini, intervalo_fin), 2)
    actualizar_estado(id, f'Comiendo ({delay}s)')
    png_animators[id].start()  # Iniciar la animación de la secuencia de imágenes
    time.sleep(delay)
    png_animators[id].stop()  # Detener la animación de la secuencia de imágenes
    actualizar_comidas(id, comidas_contador[id])

# Funciones de la interfaz gráfica
def actualizar_estado(id, estado):
    estados[id] = estado
    estado_labels[id].config(text=f'Filósofo {id + 1}: {estado}')
    png_animators[id].update_state(f'F {id + 1}: {estado}')

def actualizar_comidas(id, contador):
    comidas_contador[id] = contador
    png_animators[id].update_counter(contador)

def start_simulation():
    threading.Thread(target=main).start()

def edit_parameters():
    global cantidad_comidas, intervalo_ini, intervalo_fin

    def save_parameters():
        global cantidad_comidas, intervalo_ini, intervalo_fin  # Que las variables sean globales
        cantidad_comidas = int(cantidad_comidas_var.get())
        intervalo_ini = float(intervalo_ini_var.get())
        intervalo_fin = float(intervalo_fin_var.get())
        param_window.destroy()

    param_window = tk.Toplevel(root)
    param_window.title("Editar Parámetros")

    cantidad_comidas_var = tk.StringVar(value=str(cantidad_comidas))
    intervalo_ini_var = tk.StringVar(value=str(intervalo_ini))
    intervalo_fin_var = tk.StringVar(value=str(intervalo_fin))

    tk.Label(param_window, text="Cantidad de comidas:").pack()
    tk.Entry(param_window, textvariable=cantidad_comidas_var).pack()

    tk.Label(param_window, text="Intervalo inicial:").pack()
    tk.Entry(param_window, textvariable=intervalo_ini_var).pack()

    tk.Label(param_window, text="Intervalo final:").pack()
    tk.Entry(param_window, textvariable=intervalo_fin_var).pack()

    tk.Button(param_window, text="Guardar", command=save_parameters).pack()

def actualizar_interfaz():
    global estado_labels, png_animators
    for label in estado_labels:
        label.destroy()
    estado_labels = [tk.Label(root, text=f'Filósofo {i + 1}: Pensando', bg=root['bg'], font=('Helvetica', 10)) for i in range(num_filo)]
    for label in estado_labels:
        label.pack()
    for animator in png_animators:
        animator.label.destroy()
        animator.state_label.destroy()
        animator.counter_label.destroy()
    png_animators = [PNGAnimator(root, directorio_actual, 5, 20 + i * 150, 200, i) for i in range(num_filo)]

def main():
    start_time = time.time()

    filosofos = []
    for i in range(num_filo):
        fil = threading.Thread(target=filosofo, args=[i])
        filosofos.append(fil)
        fil.start()

    for fil in filosofos:
        fil.join()

    end_time = time.time()
    total_time = end_time - start_time

    print(f"¡Todos los filósofos han comido {cantidad_comidas} veces! Tardó {total_time:.2f} segundos en total.")
    resultado_label.config(text=f"¡Todos los filósofos han comido {cantidad_comidas} veces! Tardó {total_time:.2f} segundos en total.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Problema de los Filósofos Comensales")
root.geometry("800x400")  # Para ajustar el tamaño de la ventana
root.configure(bg='white')  # Para ajustar el color de fondo de la ventana

estado_labels = [tk.Label(root, text=f'Filósofo {i + 1}: Pensando', bg='white', font=('Helvetica', 10)) for i in range(num_filo)]
for label in estado_labels:
    label.pack()

start_button = tk.Button(root, text="Start", command=start_simulation)
start_button.pack()

edit_button = tk.Button(root, text="Editar Parámetros", command=edit_parameters)
edit_button.pack()

resultado_label = tk.Label(root, text="", bg='white', font=('Helvetica', 11))
resultado_label.pack(pady=10)

# Directorios a las secuencias de imágenes PNG
ruta_actual = os.path.abspath(__file__)
directorio_actual = os.path.dirname(ruta_actual)

png_animators = [PNGAnimator(root, directorio_actual, 5, 20 + i * 150, 200, i) for i in range(num_filo)]

root.mainloop()
