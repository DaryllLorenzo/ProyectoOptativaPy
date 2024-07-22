import threading
import random
import time
import tkinter as tk

class Barberia:
    def __init__(self, root):

        self.sillasLibres = 5
        self.sillasOcupadas = [False] * self.sillasLibres
        self.clientesAtendidos = 0
        self.clientesSeFueron = 0
        self.intervalo_ini = 1
        self.intervalo_fin = 4
        self.intervalo_ini_llega = 0.5
        self.intervalo_fin_llega = 1
        self.cantClientes = 10

        # Semáforos
        self.sem_clientes = threading.Semaphore(0)
        self.sem_sillasAccesibles = threading.Semaphore(1)
        self.sem_barberoListo = threading.Semaphore(0)

        self.simulation_running = False

        # Creacion de la interfaz gráfica
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Crear etiquetas de sillas
        for widget in self.root.pack_slaves():
            if isinstance(widget, tk.Label) and widget not in [self.atendidos_label, self.se_fueron_label, self.barbero_status_label]:
                widget.pack_forget()

        self.atendidos_label = tk.Label(self.root, text=f"Clientes atendidos: {self.clientesAtendidos}")
        self.atendidos_label.pack()

        self.se_fueron_label = tk.Label(self.root, text=f"Clientes que se fueron: {self.clientesSeFueron}")
        self.se_fueron_label.pack()

        self.barbero_status_label = tk.Label(self.root, text="Barbero: Durmiendo")
        self.barbero_status_label.pack()

        log_frame = tk.Frame(self.root)
        log_frame.pack(padx=10, pady=10)

        self.log_text = tk.Text(log_frame, state='disabled', height=15, width=60)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        log_scroll = tk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text.config(yscrollcommand=log_scroll.set)

        start_button = tk.Button(self.root, text="Start", command=self.start_simulation)
        start_button.pack()

        edit_button = tk.Button(self.root, text="Editar Parámetros", command=self.edit_parameters)
        edit_button.pack()

        self.sillas_labels = [tk.Label(self.root, text=f"Silla {i+1}: Libre") for i in range(self.sillasLibres)]
        for label in self.sillas_labels:
            label.pack()

    def barbero(self):
        while self.simulation_running:
            self.sem_clientes.acquire() # Espera a que haya un cliente
            self.sem_sillasAccesibles.acquire() # Accede a las sillas
            for i in range(len(self.sillasOcupadas)):
                if self.sillasOcupadas[i]:
                    self.sillasLibres += 1
                    self.sillasOcupadas[i] = False
                    self.update_sillas_solo_nombres()
                    self.clientesAtendidos += 1
                    self.update_labels()
                    self.log_event(f"Barbero: Atendiendo al cliente en silla {i+1}")
                    break
            self.sem_sillasAccesibles.release() # Da el acceso a las sillas
            delay = random.uniform(self.intervalo_ini, self.intervalo_fin)
            self.log_event(f"Barbero: Terminando de atender en {delay:.2f} segundos")
            self.barbero_status_label.config(text=f"Barbero: Atendiendo cliente ({delay:.2f}s)")
            time.sleep(delay)
            self.sem_barberoListo.release() # Indica que el barbero está listo para el próximo cliente
            self.barbero_status_label.config(text="Barbero: Durmiendo")

    def cliente(self):
        self.log_event("Cliente: Llega a la barbería")
        self.sem_sillasAccesibles.acquire() # Accede a las sillas
        for i in range(len(self.sillasOcupadas)):
            if not self.sillasOcupadas[i]:
                self.sillasLibres -= 1
                self.sillasOcupadas[i] = True
                self.update_sillas_solo_nombres()
                self.log_event(f"Cliente: Se sienta en la silla {i+1}")
                self.sem_clientes.release() # Indica que hay un cliente esperando
                self.sem_sillasAccesibles.release() # Da el acceso a las sillas
                self.sem_barberoListo.acquire() # Espera a que el barbero esté listo
                return
        self.sem_sillasAccesibles.release() # Da el acceso a las sillas si estaban llenas
        self.clientesSeFueron += 1
        self.update_labels()
        self.log_event("Cliente: Se va porque la barbería está llena")

    def main(self):
        self.simulation_running = True
        t_barbero = threading.Thread(target=self.barbero)
        t_barbero.start()

        cliente_threads = []
        for _ in range(self.cantClientes):
            if not self.simulation_running:
                break
            delay = random.uniform(self.intervalo_ini_llega, self.intervalo_fin_llega)
            time.sleep(delay)
            t_cliente = threading.Thread(target=self.cliente)
            cliente_threads.append(t_cliente)
            t_cliente.start()

        for t in cliente_threads:
            t.join()

        self.simulation_running = False
        self.log_event(f"Clientes atendidos: {self.clientesAtendidos}")
        self.log_event(f"Clientes que se fueron: {self.clientesSeFueron}")

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
        # Para borrar las etiquetas de sillas antiguas
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

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Barbería Durmiente")
root.geometry("500x600")
barberia = Barberia(root)
root.mainloop()
