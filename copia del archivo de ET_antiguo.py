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



def select_channel(file_path):
    # Cargar los datos crudos de Eyelink usando MNE
    raw_et = mne.io.read_raw_eyelink(file_path, create_annotations=True)

    # Obtener los eventos y sus identificadores desde las anotaciones
    et_events, et_event_ids = mne.events_from_annotations(raw_et)

    # Encontrar los canales de datos pupilares (izquierdo y derecho)
    for ch_name in raw_et.ch_names:
        if 'left' in ch_name:  # Si el canal es de la pupila izquierda
            pupil = 'pupil_left'
        elif 'right' in ch_name:  # Si el canal es de la pupila derecha
            pupil = 'pupil_right'

    # Seleccionar el canal correspondiente para el análisis
    raw_et.pick([pupil])
            
        
def preprocess_raw_et_data(raw_et, et_event_ids, et_events):
    # Filtrar los datos (por ejemplo, entre 0.5 y 30 Hz)
    raw_et.filter(l_freq=0.5, h_freq=30)
    
    #interpola los parapdeos malos de la señal
    inter = ['BAD_blink']
    raw_et =mne.preprocessing.eyetracking.interpolate_blinks(raw_et, (0.01, 0.01), match=inter)
    
    
    # Definir los parámetros para el epoching (segmentación temporal)
    event_id = et_event_ids['103']  # Usar el ID de evento 'e' (por ejemplo, un evento específico)
    tmin, tmax = -5, 5  # Definir el rango temporal de los epochs, -a,b segundos alrededor del evento

    # Crear los epochs a partir de los datos crudos y eventos definidos
    epochs = mne.Epochs(raw_et, events=et_events, event_id=event_id, tmin=tmin, tmax=tmax,
                         preload=True, reject=None, reject_by_annotation=False)
    
        
    # Obtener los datos de los epochs
    epoch_data = epochs.get_data()
   
    return epoch_data, epochs
       
    
    
def process_epochs(epochs, epoch_data, raw_et, threshold=3):
    """Procesa epochs, corrige línea base, calcula z-scores, corrige outliers, e interpola valores NaN"""

    # Aplicar corrección de línea base
    epochs.apply_baseline((-0.2, 0))  # Ajusta usando los 200 ms previos al evento
    
    # Calcular el z-score para los datos del epoch
    data = epochs.get_data()  # Obtener datos del Epochs (n_epochs, n_channels, n_times)
    mean = np.mean(data, axis=-1, keepdims=True)  # Promedio sobre el eje de tiempo
    std = np.std(data, axis=-1, keepdims=True)    # Desviación estándar
    z_score_data = (data - mean) / std

    
    # Calcular nan-mean y nan-standard deviation a través de los epochs
    mean_time_series = np.nanmean(epoch_data, axis=0).squeeze()  # Promedio a través de los epochs
    std_time_series = np.nanstd(epoch_data, axis=0).squeeze()    # Desviación estándar a través de los epochs
    
    # Manejar casos donde todos los valores son NaN
    if np.all(np.isnan(mean_time_series)):
        raise ValueError("Todos los valores en la serie temporal son NaN.")

    # Reducir a una única serie temporal promediando a través de los canales
    mean_time_series = np.nanmean(mean_time_series, axis=0).squeeze()  # (n_times,)
    
    # Calcular la desviación estándar de la serie temporal
    std_time_series = np.nanstd(epoch_data, axis=(0, 1)).squeeze()  # (n_times,)

    # Crear una matriz de tiempo para graficar
    time = epochs.times

    # Identificar outliers
    outliers = np.abs(epoch_data - mean_time_series) > threshold * std_time_series

    # Reemplazar los outliers por NaN
    epoch_data[outliers] = np.nan

    # Interpolación de los valores NaN en los epochs
    raw_et = mne.preprocessing.eyetracking.interpolate_blinks(raw_et, (0.01, 0.01), match='all')

    # Calcular el número de muestras (tiempo), el número de canales y el promedio pupilar
    N_muestras = epoch_data.shape[2]  # Número de muestras (tiempo)
    N_channel = len(raw_et.ch_names)  # Número de canales
    N_pupil = np.nanmean(epoch_data, axis=0).squeeze()  # Promedio pupilar a lo largo de los epochs

    # Retornar la información relevante
    return N_muestras, N_channel, N_pupil, std_time_series, time
    return time, mean_time_series, std_time_series
    
    
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

    
    
   
    
    
def main():
    # Verificar si el número correcto de argumentos fue pasado desde la línea de comandos
    if len(sys.argv) != 2:  # Validar número de argumentos
        print("Uso: python ET.py 'archivo.asc'")  # Instrucciones de uso
        sys.exit(1)  # Salir si el número de argumentos es incorrecto


    # Ruta al archivo Eyelink pasado como argumento
    archivo = sys.argv[1]

    # Llamar a la función de lectura de datos
    raw_et, et_events, et_event_ids = read_data(archivo)

    # Preprocesar datos
    epoch_data, epochs = preprocess_raw_et_data(raw_et, et_event_ids, et_events)

    # Procesar epochs
    N_muestras, N_channel, N_pupil, std_time_series, time = process_epochs(epochs, epoch_data, raw_et)

    #  # Graficar los resultados de la pupila con desviación estándar
    plot_data(time, N_pupil, std_time_series)



    archivo = sys.argv[1]  # Ruta al archivo de datos Eyelink que se pasará como argumento
    N_muestras, N_channel, N_pupil, std_pupil, time = read_data(archivo)  # Llamar a la función de lectura de datos
    plot_data(time, N_pupil, std_pupil)  # Graficar los resultados de la pupila con desviación estándar


if __name__ == '__main__':
    # Simulación de argumentos en Spyder (para pruebas sin argumentos de línea de comandos)
    sys.argv = ['ET.py', os.path.join(script_dir, asc_files[0])]
    main()  # Llamar a la función principal
    
    
    
    
