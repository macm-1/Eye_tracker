# Son 2 códigos, pero el funcional es solo uno, el otro es solo de ejemplo, se debe ignorar todo y solamente utilizar ET.py
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


