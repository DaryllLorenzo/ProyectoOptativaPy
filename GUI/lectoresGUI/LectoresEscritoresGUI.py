import threading
import time
import random
import tkinter as tk
from queue import Queue

# Inicializar las colas y parámetros
cola_creacion = Queue()
Estatico = False

mutex = threading.Semaphore(1)
cuarto_vacio = threading.Semaphore(1)
mecanismo_control = threading.Semaphore(1)
lectores = 0

class LectoresEscritoresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lectores y Escritores")
        self.root.geometry("600x400")  

        self.intervalo_iniL = tk.DoubleVar(value=0)
        self.intervalo_finL = tk.DoubleVar(value=4)
        self.intervalo_iniE = tk.DoubleVar(value=0)
        self.intervalo_finE = tk.DoubleVar(value=4)
        self.tiempoEstaticoL = tk.DoubleVar(value=0)
        self.tiempoEstaticoE = tk.DoubleVar(value=0)
        self.Estatico = tk.BooleanVar(value=False)
        
        # UI
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Intervalo Lectores (inicio, fin)").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.intervalo_iniL).grid(row=0, column=1)
        tk.Entry(frame, textvariable=self.intervalo_finL).grid(row=0, column=2)

        tk.Label(frame, text="Intervalo Escritores (inicio, fin)").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.intervalo_iniE).grid(row=1, column=1)
        tk.Entry(frame, textvariable=self.intervalo_finE).grid(row=1, column=2)

        tk.Label(frame, text="Tiempo Estático Lector").grid(row=2, column=0)
        tk.Entry(frame, textvariable=self.tiempoEstaticoL).grid(row=2, column=1)

        tk.Label(frame, text="Tiempo Estático Escritor").grid(row=3, column=0)
        tk.Entry(frame, textvariable=self.tiempoEstaticoE).grid(row=3, column=1)

        tk.Checkbutton(frame, text="Estatico", variable=self.Estatico).grid(row=4, columnspan=2)

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

    def mostrar_dialogo_procesos(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Agregar Procesos")

        tk.Label(dialogo, text="Cantidad de procesos a crear:").grid(row=0, column=0)
        cantidad_var = tk.IntVar()
        tk.Entry(dialogo, textvariable=cantidad_var).grid(row=0, column=1)

        tk.Label(dialogo, text="Tipo de proceso (0 = lectores, 1 = escritores):").grid(row=1, column=0)
        tipo_var = tk.IntVar()
        tk.Entry(dialogo, textvariable=tipo_var).grid(row=1, column=1)

        def agregar_procesos():
            p1 = cantidad_var.get()
            p2 = tipo_var.get()
            elemento = (p1, p2)
            cola_creacion.put(elemento)
            self.log(f"Agregado {p1} {'lectores' if p2 == 0 else 'escritores'} a la cola")
            dialogo.destroy()

        tk.Button(dialogo, text="Agregar", command=agregar_procesos).grid(row=2, columnspan=2)

    def vaciar_cola(self):
        with cola_creacion.mutex:
            cola_creacion.queue.clear()
        self.log("Cola de procesos vaciada")
        self.mostrar_dialogo_procesos()

    def iniciar_procesos(self):
        global Estatico
        self.text.configure(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.configure(state='disabled')

        Estatico = self.Estatico.get()
        intervalo_iniL = self.intervalo_iniL.get()
        intervalo_finL = self.intervalo_finL.get()
        intervalo_iniE = self.intervalo_iniE.get()
        intervalo_finE = self.intervalo_finE.get()
        tiempoEstaticoL = self.tiempoEstaticoL.get()
        tiempoEstaticoE = self.tiempoEstaticoE.get()

        def escritor():
            mecanismo_control.acquire()
            cuarto_vacio.acquire()
            if Estatico:
                delay = tiempoEstaticoE
            else:
                delay = random.uniform(intervalo_iniE, intervalo_finE)
            self.log(f"Escritor escribiendo {delay:.2f} segundos para terminar")
            time.sleep(delay)
            cuarto_vacio.release()
            mecanismo_control.release()

        def lector():
            global lectores
            mecanismo_control.acquire()
            mecanismo_control.release()
            mutex.acquire()
            lectores += 1
            if lectores == 1:
                cuarto_vacio.acquire()
            mutex.release()
            if Estatico:
                delay = tiempoEstaticoL
            else:
                delay = random.uniform(intervalo_iniL, intervalo_finL)
            self.log(f"Lector leyendo {delay:.2f} segundos para terminar")
            time.sleep(delay)
            mutex.acquire()
            lectores -= 1
            if lectores == 0:
                cuarto_vacio.release()
            mutex.release()

        def main():
            start_time = time.time()
            size = cola_creacion.qsize()
            threads = []
            for _ in range(size):
                tupla_temp = cola_creacion.get()
                if tupla_temp[1] == 0:
                    for _ in range(tupla_temp[0]):
                        t = threading.Thread(target=lector)
                        t.start()
                        threads.append(t)
                else:
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

        with cola_creacion.mutex:
            for item in list(cola_creacion.queue):
                p1, p2 = item
                text.insert(tk.END, f"{p1} {'lectores' if p2 == 0 else 'escritores'}\n")
        
        text.configure(state='disabled')

    def log(self, message):
        self.text.configure(state='normal')
        self.text.insert(tk.END, message + "\n")
        self.text.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = LectoresEscritoresApp(root)
    root.mainloop()
