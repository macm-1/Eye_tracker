# Respecto a las carpetas, se creó la carpeta "a git-hub" para dejar todos los archivos realmente necesarios en el repositorio, se incluyó:
- script ET.py junto con su plot ET.png
- script código_files_csv junto con su plot "csv.png [0]"
- los datos del sujeto sAMozo. Tanto los datos completos .csv como los datos recortados a la mitad del archivo .asc
- El informe de la investigación como fundamento teórico de los scripts

# Se debe usar solo lo que está contenido en la carpeta "a git-hub", los demás son solamente intentos fallidos del pasado que deben ser ignorados.


# Son 2 códigos importantes, pero el más funcional es ET.py, el otro (Código_files_csv.py) es sólo un ejemplo, aún no esta terminado, pero deberían funcionar ambos.
hubo un error al subir los archivos a git-hub.

# respecto a ET.py 

analiza datos de un dispositivo de seguimiento ocular que marca eventos de forma automática, tomando datos de número de muestras, posición en el eje x, posición en el eje y, diámetro pupilar junto con un código de sincronización muestreal.

se calibran los datos y se produce la toma de datos con una frecuencia de muestreo de 1000Hz, por masomenos 60minutos por persona.


# protocolo experimental sobre la toma de datos Eye_tracker, archivo ET.py

Se adquirió datos por medio de un dispositivo de seguimiento ocular EyeLink 1000 Plus, versión II CL v5.50 (junio 2022), y se almacenaron en formato EDF (Eye Data File), convertidos y etiquetados con el software edfapi 4.4.1, y el componente EyeLink Dataviewer Subcomponent, con ayuda de una cámara Eyelink GL Version 1.2 con un sensor AI7.

participantes:
primeramente, se puso a las 21 participantes mujeres entre 19 y 24 años de edad a las que previamente se les hizo un pequeño cuestionario para llevar un registro y descartar alguna condición atencional especial o médica. De los cuales 10 fueron finalmente usados para el grupo experimental y los análisis estadísticos y correlacionales.

Diseño experimental:
se realizaron 4 bloques con 30 ensayos cada uno, para un total de 120 ensayos por participante. En cada ensayo se presentaron 8 círculos de color plano definido como (-1,-1,0) que luego cambian brevemente a un color distintivo (-1,-0,7,-1), dependiendo del bloque se pintan 2, 3 o 4 círculos de forma aleatoria.

En una silla, sentado y con respaldo de mentón y un Eye tracker, frente a una ventana de 1920x1080 pixeles con un fondo gris oscuro (-0,6, -0,6, -0,6) se procedió al experimento. Primeramente, se puso en medio de la pantalla una cruz de fijación de 0,4 unidades de durante 2,5 a 5 segundos de preparación, posteriormente los 8 círculos de radio 0,16 unidades se desplazan a una velocidad de 1.5 unidades/segundo por 7 segundos, luego se detienen a los 18 segundos, se espera 0,5 segundos y se pregunta a los participantes si el círculo seleccionado era uno de los objetivos iniciales o no con respuestas booleanas, después de la respuesta se le da una retroalimentación (correcto o incorrecto), esto en un tiempo de máximo 21 segundos, donde se les 2,5 segundos para procesar la información, finalmente, los participantes observaban una cruz de descanso en el centro de la pantalla por 20 segundos. Se realizo un protocolo de 120 ensayos por participante dividido en 30 ensayos por bloque donde se variaba el número de círculos pintados.

# Respecto al script ET.py

analiza datos de un dispositivo de seguimiento ocular que marca eventos de forma automática, tomando datos de número de muestras, posición en el eje x, posición en el eje y, diámetro pupilar junto con un código de sincronización muestreal.

se calibran los datos y se produce la toma de datos con una frecuencia de muestreo de 1000Hz, por masomenos 60minutos por persona.


# protocolo experimental sobre la toma de datos Eye_tracker, archivo ET.py

Se adquirió datos por medio de un dispositivo de seguimiento ocular EyeLink 1000 Plus, versión II CL v5.50 (junio 2022), y se almacenaron en formato EDF (Eye Data File), convertidos y etiquetados con el software edfapi 4.4.1, y el componente EyeLink Dataviewer Subcomponent, con ayuda de una cámara Eyelink GL Version 1.2 con un sensor AI7.

participantes:
primeramente, se puso a las 21 participantes mujeres entre 19 y 24 años de edad a las que previamente se les hizo un pequeño cuestionario para llevar un registro y descartar alguna condición atencional especial o médica. De los cuales 10 fueron finalmente usados para el grupo experimental y los análisis estadísticos y correlacionales.

Diseño experimental:
se realizaron 4 bloques con 30 ensayos cada uno, para un total de 120 ensayos por participante. En cada ensayo se presentaron 8 círculos de color plano definido como (-1,-1,0) que luego cambian brevemente a un color distintivo (-1,-0,7,-1), dependiendo del bloque se pintan 2, 3 o 4 círculos de forma aleatoria.

En una silla, sentado y con respaldo de mentón y un Eye tracker, frente a una ventana de 1920x1080 pixeles con un fondo gris oscuro (-0,6, -0,6, -0,6) se procedió al experimento. Primeramente, se puso en medio de la pantalla una cruz de fijación de 0,4 unidades de durante 2,5 a 5 segundos de preparación, posteriormente los 8 círculos de radio 0,16 unidades se desplazan a una velocidad de 1.5 unidades/segundo por 7 segundos, luego se detienen a los 18 segundos, se espera 0,5 segundos y se pregunta a los participantes si el círculo seleccionado era uno de los objetivos iniciales o no con respuestas booleanas, después de la respuesta se le da una retroalimentación (correcto o incorrecto), esto en un tiempo de máximo 21 segundos, donde se les 2,5 segundos para procesar la información, finalmente, los participantes observaban una cruz de descanso en el centro de la pantalla por 20 segundos. Se realizo un protocolo de 120 ensayos por participante dividido en 30 ensayos por bloque donde se variaba el número de círculos pintados.

# Respecto al script ET.py

EyeLink almacena directamente los eventos oculares como sacadas (SSACC, ESACC), Fijaciones (EFIX, SFIX) y parpadeos buenos (EBLINK) y malos BAD_EBLINK  en "anotaciones"

Esta región del código lo ejemplifica mejor:

    # Cargar los datos crudos de Eyelink
    raw_et = mne.io.read_raw_eyelink(file_path, create_annotations=True)

    # Obtener los eventos y sus identificadores desde las anotaciones
    et_events, et_event_ids = mne.events_from_annotations(raw_et)


raw_et es un objeto de los datos crudos del EyeTracker, en este caso se están guardando esos datos utilizando una librería importante que necesitamos conocer:
librería de datos neurofisiológicos MEG, EEG, fMRI y EyeTracker.

raw_et es un objeto de los datos crudos del EyeTracker.

et_events es un marcador de eventos que se almacenan como un diccionario con IDs en et_event_ids.

se guardan los eventos también con ayuda de
 create_annotations=True, en file_path.
 

por medio de la librería os, una librería para interactuar con el sistema operativo y los directorios.

se abre el directorio de la carpeta donde esté el script actualmente convirtiéndolo en una ruta absoluta por medio de

os.path.abspath(__file__)


luego de eso read_data lee los archivos que están en formato .asc

 y se escoge entre "LEFT" o "RIGHT", de modo que se usa solamente un ojo para cada sujeto.

y se escoge con .pick

luego se filtran los datos (0.5,30Hz), se interpolan los parpadeos erróneos

y se busca un evento en base a este código de eventos:


sistema de representación de eventos por medio de códigos numéricos marcando el inicio del ensayo (10), inicio del movimiento (11), inicio de la pregunta (12) e inicio del descanso (80). Junto con esto se grabaron las respuestas del participante: verdadero positivo (101), verdadero negativo (102), falso positivo (103), falso negativo (104).

escoge el evento objetivo, en este caso 12 y se busca tmin, tmax elegidos.

y se epocan los datos entre esos tiempos, el 0,0 es el evento.

se ignoran los valores NaN y se realiza el promedio y la desviación estándar de las épocas.

np.nanmean, np.nanstd.


luego con estos datos y el tiempo se plotea.

con plt.fill_beetween se genera un limite base inferior y superior (mas/menos desviación estándar en este caso)

y se crea un área sombreada rodeando a la linea promedio con porcentaje de transparencia escogido (Alpha)

y luego se guarda una figura con savefig(output_file)


#____________________________________

Finalmente se realiza un main, se verifican los argumentos (la longitud con len()) y se crea la forma de llamarlo desde bash:

se llama con Python ET.py 'archivo.asc'

se dan dos argumentos, el nombre (ET.py) se espera la ruta del archivo (sys.argv[1]) asc


Recordar que anteriormente se eligió el primer archivo de la carpeta [0], pero esta debería iterar sobre todos los archivos, entonces debería poder abrir archivos 

file_path = os.path.join(script_dir, asc_files[0])

finalmente se vuelve a llamar a la función que itera sobre los archivos del directorio que terminan en 'asc'

finalmente se selecciona el primer archivo encontrado [0] en el directorio, 

se le llama a este script ET.py 
y finalmente se devuelve la llamada al main()

de modo que hay que escribir desde bash

Python ET.py 'archivo.asc'
Se sube también un archivo .asc para el ejemplo por medio de la terminal.
Lamentablemente no se puede disminuir el tamaño, puesto que no sé bién cuales datos son de que parte específica de cual trial y prefiero no intentarlo.

#IMPORTANTE: el Script ET.py y los archivos.asc deben estar en el mismo directorio para funcionar.

Antes de usar MNE se necesita instalar en la terminal con
pip install mne




##################################################################################################################




# Respecto al script código_files_csv que lee archivos csv

El archivo .csv es un archivo de 7 columnas:
Abs_Time, Block_Idx, Trial_Idx, n_Targets, Asked_for_target, Response_type, Response_Time

lo que hace el script es básicamente leer los datos de los archivos que tengan .csv en la parte final de su numbre dentro de la carpeta del directorio donde está guardado código_files_csv.py
y convertirlos a un df, luego crear un archivo para cada columna y después juntarlas respecto al interés:

Se convierten a datos numéricos con .to_numeric
y se elimnan las columnas con NaN en 'Response_Time'

luego se filtra el df respecto a la columna 'n_Targets' respecto al valor 2.

luego calcula el promedio y la desviación estándar de 'Response_Time' por 'Abs_Time'

y se usan para graficar el promedio de los tiempos de respuesta en función del tiempo absoluto.

se guarda el archivo como "csv_files[0]" (se puede cambiar el nombre respecto al sujeto analizado)

Finalmente se define el main y la forma de llamarlo desde la terminal o bash.

se escribe: python código_files_csv.py para abrirlo desde la terminal, se ejecutará el plot de los datos.


# Respecto a Eye_tracker_ET.py Se deja solamente como muestra ejemplo de un intento iterativo.

este contiene estas funciones importantes, pero no logró funcionar adecuadamente, se reemplaza por ET.py

Resumen detallado de las funciones más importantes (esto solamente respecto a Eye_tracker_ET.py, pero lamentablemente no funcionó adecuadamente).

1.	process_all_subjects
Procesa múltiples archivos de EyeLink iterativamente. Para cada archivo, filtra eventos como sacadas y blinks, selecciona canales de pupila ('LEFT' o 'RIGHT') y aplica filtros de frecuencia (0.5-30 Hz) para eliminar ruido. Si el archivo contiene datos válidos, genera gráficos para visualizar los resultados procesados.
2.	directory_eyelink_file
Crea un directorio para almacenar archivos preprocesados si no existe. Retorna la ruta del archivo filtrado que incluirá datos limpios tras el procesamiento.
3.	filter_saccades
Filtra eventos irrelevantes como 'ESACC', 'SFIX', entre otros, para eliminar sacadas y otros datos no deseados. Guarda los datos restantes en un nuevo archivo con el sufijo _no_saccades.
4.	filter_eyelink_data
Carga los datos filtrados y convierte la señal en un objeto Raw de MNE. Aplica un filtro de frecuencia entre 0.5 y 30 Hz para mejorar la calidad de la señal, y selecciona canales de pupila relevantes ('LEFT' o 'RIGHT') para análisis posterior.
5.	create_raw_et
Convierte los datos filtrados a un objeto RawArray de MNE. Detecta eventos 'START' y 'END' para dividir los datos en épocas. Esto permite un análisis detallado por segmentos.
6.	load_and_process_eyelink_data
Carga archivos de EyeLink como DataFrames. Filtra las cinco primeras columnas y extrae el diámetro pupilar de la cuarta columna para su análisis.
7.	plot_data
Visualiza los datos procesados utilizando la función de graficado de MNE. Los gráficos muestran la evolución de la señal pupilar procesada, destacando eventos relevantes.
8.	filter_signal
Aplica un filtro pasa banda (0.5-30 Hz) para eliminar artefactos y ruido de baja frecuencia (como movimientos lentos) y altas frecuencias (como ruido eléctrico) en los datos pupilares.
procesamiento:
9.	interpolate_blinks
Interpola datos faltantes debidos a parpadeos detectados en el canal de pupila. Utiliza funciones de MNE para sustituir estas interrupciones con valores estimados, garantizando la continuidad de la señal pupilar.
10.	read_and_filter_data
Lee los datos crudos desde el archivo de EyeLink línea por línea. Filtra filas basándose en condiciones específicas, como la ausencia de puntos decimales en las primeras columnas o la presencia de valores irrelevantes como "0,0" en la tercera columna.
11.	select_pupil_channels
Verifica si los canales de pupila ('LEFT' o 'RIGHT') están presentes en los datos procesados. Selecciona el canal válido para continuar con el análisis. Si ambos están disponibles, prioriza uno para evitar conflictos.
12.	create_epochs_from_lines
Divide los datos en épocas basándose en eventos delimitadores 'START' y 'END'. Cada época representa un bloque temporal que puede ser analizado de manera independiente, lo que es útil para identificar patrones específicos en cada segmento.
13.	handle_start y handle_end
Gestionan los eventos 'START' y 'END'. handle_start inicializa una nueva época cuando encuentra un evento de inicio, mientras que handle_end completa y almacena la época actual cuando detecta un evento de cierre.
14.	process_eyelink_file
Procesa un archivo individual de EyeLink, asegurando que los datos sean preprocesados y filtrados. Combina múltiples pasos, desde el filtrado de sacadas hasta la selección de canales, y genera archivos intermedios para facilitar análisis posteriores.
15.	get_pupil_channel
Identifica el canal de pupila ('LEFT' o 'RIGHT') dentro de los datos crudos. Este paso es esencial para trabajar con el canal correcto en las etapas posteriores de procesamiento.
16.	save_filtered_file (implícita en los métodos)
Guarda los datos filtrados en archivos separados. Esto evita sobrescribir el archivo original y garantiza la conservación de los datos crudos para futuras referencias o análisis.
17.	plot_data
Genera una representación gráfica de los datos pupilares procesados. Utiliza escalas específicas para destacar eventos clave y permite visualizar artefactos o resultados del procesamiento.


