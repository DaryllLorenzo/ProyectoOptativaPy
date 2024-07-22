import streamlit as st
import os

# Audio para la pagina
st.sidebar.title("Música")
st.sidebar.header("Para escuchar musiquita en lo que se lee la pagina")
audio = st.sidebar.file_uploader("Sube un archivo mp3", type=["mp3"])
if audio is not None:
    audio_bytes = audio.read()
    st.sidebar.audio(audio_bytes, format='audio/mp3', start_time=0) # para que empiece desde que se abre la pagina


## pagina principal
st.title("_Proyecto optativa Python :)_") # los _ _ agregan cursiva

ruta_actual = os.path.abspath(__file__)
directorio_actual = os.path.dirname(ruta_actual)
ruta_foto = os.path.join(directorio_actual, "snake.jpg")

st.image(ruta_foto)


st.header("Título: Simulador de Problemas Clásicos de Sincronización de Procesos con Interfaz Gráfica")

st.header("Descripción breve")

st.markdown("Este programa permite simular y visualizar de manera animada los problemas clásicos de sincronización de procesos, como el problema del productor-consumidor, el problema de los lectores-escritores, entre otros. Además, el programa es parametrizable, lo que significa que se pueden ajustar la cantidad de procesos, el tiempo máximo que demora un proceso en un estado determinado, el tiempo total o la cantidad de iteraciones para su finalización. Al finalizar la simulación, se muestra un resumen con estadísticas básicas sobre el rendimiento y el comportamiento de los procesos.")

st.header("Descripción del proyecto")

st.markdown("Este proyecto tiene como objetivo simular varios problemas clásicos de sincronización de procesos utilizando tanto una interfaz de línea de comandos (CLI) como una interfaz gráfica (GUI) desarrollada con Tkinter. Los problemas abordados son:")

st.markdown("**1.  Productor-Consumidor**")
st.markdown("**2.  Barbero Dormilón**")
st.markdown("**3.  Lectores-Escritores**")
st.markdown("**4.  Filósofos Comensales**")

st.markdown("La sincronización de procesos es un tema crucial en sistemas operativos y programación concurrente. Estos problemas clásicos ayudan a entender cómo gestionar el acceso concurrente a recursos compartidos.")

st.header("Bibliotecas estándar de Python utilizadas")

st.markdown("**1. threading**: Para trabajar con hilos (threads) y semáforos.")
st.markdown("**2. time**: Para el conteo del tiempo, y las simulaciones de procesos.")
st.markdown("**3. tkinter**: Para crear interfaces gráficas de usuario (GUIs).")
st.markdown("**4. queue**: Para trabajar con la estructura de datos cola.")
st.markdown("**5. os**: Para manejar rutas absolutas y otras operaciones del sistema operativo.")

st.markdown("Los codigos están comentados, revisar **MainConsole.py** y **MAIN.py** dentro de GUI/MainFRAME.")

st.header("Problemas Clásicos de Sincronización")

st.markdown("<h3>1. Productor-Consumidor</h3>", unsafe_allow_html=True)

st.markdown("Un productor genera datos y los coloca en un buffer. Un consumidor toma datos del buffer. La sincronización asegura que el productor no añada datos cuando el buffer está lleno y el consumidor no intente tomar datos cuando el buffer está vacío.")

st.markdown("<h3>2. Barbero Dormilón</h3>", unsafe_allow_html=True)

st.markdown("En una barbería, un barbero corta el pelo de los clientes que llegan. Si no hay clientes, el barbero duerme. Si un cliente llega y el barbero está ocupado, el cliente espera en una silla. Si no hay sillas disponibles, el cliente se va.")

st.markdown("<h3>3. Lectores-Escritores</h3>", unsafe_allow_html=True)
st.markdown("Varios lectores pueden leer simultáneamente un recurso compartido, pero un escritor debe tener acceso exclusivo. La sincronización asegura que ningún escritor escriba mientras un lector está leyendo y viceversa.")

st.markdown("<h3>4. Filósofos Comensales</h3>", unsafe_allow_html=True)
st.markdown("Cinco filósofos se sientan alrededor de una mesa con un plato de espaguetis y cinco tenedores. Para comer, un filósofo necesita dos tenedores. Los filósofos pasan por los estados de pensar, comer y hambrientos. La sincronización evita que se produzca un deadlock.")

st.markdown("<h3>Implementación general</h3>", unsafe_allow_html=True)

st.markdown("<h4>Uso de Semáforos y Funciones acquire(como un down() ) y release(como un up() ) :</h4>", unsafe_allow_html=True)
st.markdown("Para manejar la concurrencia y sincronización de procesos, se utilizó la biblioteca threading de Python, que proporciona semáforos y otras primitivas de sincronización. Los semáforos son utilizados para controlar el acceso a los recursos compartidos y asegurar que se respeten las restricciones de concurrencia. Las funciones acquire y release de los semáforos se usan para bloquear y desbloquear el acceso a estos recursos.")
st.markdown("<h4>Creación de Hilos:</h4>", unsafe_allow_html=True)
st.markdown("La biblioteca threading también se utiliza para crear y manejar hilos (threads) en Python. Los hilos permiten ejecutar múltiples operaciones simultáneamente, lo que es crucial para la simulación de problemas de sincronización de procesos. Cada hilo representa un proceso independiente (por ejemplo, un productor, un consumidor, un filósofo, etc.) que interactúa con otros procesos en tiempo real.")
st.markdown("<h4>En el caso de los filósofos: </h4>", unsafe_allow_html=True)
st.markdown("Uso de threading.Lock para los tenedores y necesaria la creación de una clase para animar png ya que Tkinter no maneja bien el tema de las transparencias y cuando detenía el gif se quedaba el fondo pegado, entonces la mejor solución fue descomprimir el gif en varias imágenes png y animarlas.")
st.markdown("<h4>En el caso de lectores-escritores: </h4>", unsafe_allow_html=True)
st.markdown("El uso de queue para manejar las colas, creé una cola de tuplas (cant procesos, tipo procesos) y luego trabajo con esta estructura realizando su vaciado y agregar nuevos elementos a la misma.")
st.markdown("<h4>Interfaz Gráfica (GUI): </h4>", unsafe_allow_html=True)
st.markdown("La interfaz gráfica desarrollada con Tkinter permite visualizar la simulación de cada problema. Los elementos clave de la GUI incluyen:")
st.markdown("**Botones** para iniciar y detener la simulación.")
st.markdown("**Etiquetas** para mostrar el estado actual de cada proceso")
st.markdown("**Animaciones simples** para ilustrar la actividad de los procesos.")
st.markdown("**Ventanas de diálogo** para ajustar parámetros como tiempos de espera y número de procesos.")

st.header("Para ejecutar el proyecto:")
st.markdown("<h4>Por archivos .py: </h4>", unsafe_allow_html=True)
st.markdown("Para la versión CLI, navega al directorio correspondiente y ejecuta el archivo Python por la terminal o por el Visual Studio Code, MainConsole.py (el codigo esta comentado) o se puede ejecutar modular que estaria en la carpeta Version_modular_consola.")
st.markdown("Para la versión GUI, navega al directorio correspondiente y ejecuta el archivo Python por la terminal o por el Visual Studio Code, MAIN.py (el codigo esta comentado) dentro de la carpeta GUI/MainFRAME, o tambien se puede ejecutar modular.")
st.markdown("<h4>Por ejecutables: </h4>", unsafe_allow_html=True)
st.markdown("También se proporcionan ejecutables para las plataformas de Windows y Linux, estos ejecutables fueron creados con pyinstaller instalado a través de pip. Sería simplemente doble click al ejecutable en caso de Windows, y en el caso de Linux dentro de la carpeta Ejecutables_Linux hay un archivo con instrucciones para la apertura.Además tenemos un archivo **leer++.txt** que abordo más acerca de la compatibilidad con los sistemas Linux y tal.")

st.header("Conclusión")

st.markdown("1. Este proyecto proporciona una herramienta interactiva para entender y visualizar problemas clásicos de sincronización de procesos en sistemas operativos. La combinación de interfaces de línea de comandos y gráficas facilita la comprensión tanto para principiantes como para usuarios más avanzados.")

rutavideo = os.path.join(directorio_actual, "video.mp4")

st.markdown("2. Destacar: ")
st.video(rutavideo)