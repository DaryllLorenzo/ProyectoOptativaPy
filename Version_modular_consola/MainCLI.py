import os
import platform

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
sistema_operativo = platform.system()

ruta_actual = os.path.abspath(__file__)
directorio_actual = os.path.dirname(ruta_actual)

opcion = int(input("Seleccione una opción: "))

if opcion == 1: # YA OK
    ruta_Prod_consum = os.path.join(directorio_actual, "Productor-consumidor.py")
    if sistema_operativo == "Windows":
        os.system(f"python {ruta_Prod_consum}")
    elif sistema_operativo == "Linux":
        os.system(f"python3 {ruta_Prod_consum}")
    else:
        print("Sistema operativo no compatible.")
    # invocar archivo Productores-consumidores.py
    pass
elif opcion == 2:
    ruta_Barbero_dormilon = os.path.join(directorio_actual, "Barbero_dormilon.py")
    if sistema_operativo == "Windows":
        os.system(f"python {ruta_Barbero_dormilon}")
    elif sistema_operativo == "Linux":
        os.system(f"python3 {ruta_Barbero_dormilon}")
    else:
        print("Sistema operativo no compatible.")
    # invocar archivo Barbero-dormilon.py
    pass
elif opcion == 3:
    ruta_Lectores_Escritores = os.path.join(directorio_actual, "Lectores_Escritores.py")
    if sistema_operativo == "Windows":
        os.system(f"python {ruta_Lectores_Escritores}")
    elif sistema_operativo == "Linux":
        os.system(f"python3 {ruta_Lectores_Escritores}")
    else:
        print("Sistema operativo no compatible.")
    # invocar archivo Lectores-Escritores.py
    pass
elif opcion == 4: # YA OK
    ruta_Filosofos_Comensales = os.path.join(directorio_actual, "Filosofos_Comensales.py")
    if sistema_operativo == "Windows":
        os.system(f"python {ruta_Filosofos_Comensales}")
    elif sistema_operativo == "Linux":
        os.system(f"python3 {ruta_Filosofos_Comensales}")
    else:
        print("Sistema operativo no compatible.")
    # invocar archivo Filosofos_Comensales.py
    pass
else:
    print("Hasta pronto !")
    pass