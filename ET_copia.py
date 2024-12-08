import sys
import os
import mne
import numpy as np
import matplotlib.pyplot as plt


# Directorio donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Buscar archivos que terminen en .asc en el directorio actual
asc_files = [f for f in os.listdir(script_dir) if f.endswith(".asc")]

if not asc_files:
    raise FileNotFoundError("No se encontraron archivos .asc en el repositorio.")

print(f"Archivos encontrados: {asc_files}")

# Usar el primer archivo encontrado como ejemplo
file_path = os.path.join(script_dir, asc_files[0])
print(f"Ruta al archivo seleccionado: {file_path}")


def read_data(file_path):
    """
    Cargar datos crudos de Eyelink usando MNE y obtener eventos.
    """
    # Cargar los datos crudos de Eyelink
    raw_et = mne.io.read_raw_eyelink(file_path, create_annotations=True)

    # Obtener los eventos y sus identificadores desde las anotaciones
    et_events, et_event_ids = mne.events_from_annotations(raw_et)
    print("Eventos obtenidos:", et_events)
    print("IDs de eventos:", et_event_ids)

    return raw_et, et_events, et_event_ids


# Llamar a la función con el archivo seleccionado
raw_data, events, event_ids = read_data(file_path)


def select_pupil_channel(file_path):
    """Función para seleccionar el canal de la pupila (izquierda o derecha) en los datos de Eyelink."""
    
    # Cargar los datos crudos de Eyelink
    raw_et = mne.io.read_raw_eyelink(file_path, create_annotations=True)

    # Obtener los eventos y sus identificadores desde las anotaciones
    et_events, et_event_ids = mne.events_from_annotations(raw_et)

    # Find pupil data channel
    for ch_name in raw_et.ch_names:
        if 'left' in ch_name:
            pupil = 'pupil_left'
        elif 'right' in ch_name:
            pupil = 'pupil_right'

    # Seleccionar el canal de pupila correspondiente
    raw_et.pick([pupil])
    
    return raw_et, et_events, et_event_ids


def preprocess_raw_et_data(raw_et, et_event_ids, et_events):
    """
    Filtrar datos, interpolar parpadeos y crear epochs.
    """
    # Filtrar los datos (por ejemplo, entre 0.5 y 30 Hz)
    raw_et.filter(l_freq=0.5, h_freq=30)
    
    # Interpolar parpadeos
    inter = ['BAD_blink']
    raw_et = mne.preprocessing.eyetracking.interpolate_blinks(raw_et, (0.01, 0.01), match=inter)
    
    # Crear epochs
    event_id = et_event_ids['12']  # Ajustar el evento específico según tu análisis
    tmin, tmax = -5, 5  # Rango temporal de los epochs
    epochs = mne.Epochs(raw_et, events=et_events, event_id=event_id, tmin=tmin, tmax=tmax,
                        preload=True, reject=None, reject_by_annotation=False)
    return epochs





def preprocess_raw_et_data(raw_et, et_event_ids, et_events):
    # Filtrar los datos (por ejemplo, entre 0.5 y 30 Hz)
    raw_et.filter(l_freq=0.5, h_freq=30)
    
    #interpola los parapdeos malos de la señal
    inter = ['BAD_blink']
    raw_et =mne.preprocessing.eyetracking.interpolate_blinks(raw_et, (0.01, 0.01), match=inter)
    
    
    # Definir los parámetros para el epoching (segmentación temporal)
    event_id = et_event_ids['12']  # Usar el ID de evento 'e' (por ejemplo, un evento específico)
    tmin, tmax = -5, 5  # Definir el rango temporal de los epochs, -a,b segundos alrededor del evento

    # Crear los epochs a partir de los datos crudos y eventos definidos
    epochs = mne.Epochs(raw_et, events=et_events, event_id=event_id, tmin=tmin, tmax=tmax,
                         preload=True, reject=None, reject_by_annotation=False)
    
        
    # Obtener los datos de los epochs
    epoch_data = epochs.get_data()
   
    return epoch_data, epochs


def process_epoch_data(epochs):
    # Obtener datos de los epochs
    epoch_data = epochs.get_data()

    # Calcular la media y desviación estándar a través de los epochs
    mean_time_series = np.nanmean(epoch_data, axis=0).squeeze()  # Promedio entre epochs
    std_time_series = np.nanstd(epoch_data, axis=0).squeeze()    # Desviación estándar entre epochs

    # Crear un arreglo de tiempo para graficar
    time = epochs.times

    return mean_time_series, std_time_series, time


def plot_data(time, mean_pupil, std_pupil, output_file="ET.png"):
    # Graficar la serie temporal promedio de la pupila junto con la desviación estándar
    plt.figure(figsize=(10, 6))
    plt.plot(time, mean_pupil, label='Mean Time Series', color='blue')  # Graficar la media
    plt.fill_between(time, mean_pupil - std_pupil, mean_pupil + std_pupil, color='blue', alpha=0.2, label='±1 Std Dev')  # Rellenar con la desviación estándar
    plt.xlabel('Time (s)')  # Etiqueta del eje X
    plt.ylabel('Pupil Size')  # Etiqueta del eje Y
    plt.title('Epoch Mean with Standard Deviation')  # Título del gráfico
    plt.legend()  # Leyenda del gráfico
    plt.grid(True)  # Mostrar la cuadrícula
    plt.savefig(output_file)  # Guardar el gráfico como archivo de imagen
    print(f"Figura guardada como {output_file}")  # Confirmar que la figura fue guardada
    
    plt.show()
    
plt.show()







def main():
    # Verificar si el número correcto de argumentos fue pasado desde la línea de comandos
    if len(sys.argv) != 2:  # Validar número de argumentos
        print("Uso: python ET.py 'archivo.asc'")  # Instrucciones de uso
        sys.exit(1)  # Salir si el número de argumentos es incorrecto
        
    archivo = sys.argv[1]  # Ruta al archivo de datos Eyelink que se pasará como argumento


if __name__ == '__main__':
    # Simulación de argumentos en Spyder (para pruebas sin argumentos de línea de comandos)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtener directorio del script
    asc_files = [f for f in os.listdir(script_dir) if f.endswith(".asc")]


     # Seleccionar el primer archivo .asc encontrado
    sys.argv = ['ET.py', os.path.join(script_dir, asc_files[0])]
    main()  # Llamar a la función principal
