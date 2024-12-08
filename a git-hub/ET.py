import sys
import os
import mne
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats



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
    print(f"Eventos obtenidos para {file_path}:", et_events)
    print(f"IDs de eventos para {file_path}:", et_event_ids)

    return raw_et, et_events, et_event_ids




# Llamar a la función con el archivo seleccionado
raw_data, events, event_ids = read_data(file_path)


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



"""Filtrar datos, interpolar parpadeos y crear epochs."""
# Filtrar los datos (por ejemplo, entre 0.5 y 30 Hz)
raw_et.filter(l_freq=0.5, h_freq=30)

# Interpolar parpadeos
inter = ['BAD_blink']
raw_et = mne.preprocessing.eyetracking.interpolate_blinks(raw_et, (0.01, 0.01), match=inter)

# Interpolarvalores NaN automáticamente
raw_et = mne.preprocessing.eyetracking.interpolate_blinks(raw_et)

                                                         
# Crear epochs
event_id = et_event_ids['101']  # Ajustar el evento específico según análisis
tmin, tmax = -5, 15  # Rango temporal de los epochs
epochs = mne.Epochs(raw_et, events=et_events, event_id=event_id, tmin=tmin, tmax=tmax,
                    preload=True, reject=None, reject_by_annotation=False)


# Obtener datos de los epochs
epoch_data = epochs.get_data()

# Calcular la media y desviación estándar a través de los epochs
mean_time_series = np.nanmean(epoch_data, axis=0).squeeze()  # Promedio entre epochs
std_time_series = np.nanstd(epoch_data, axis=0).squeeze()    # Desviación estándar entre epochs


if np.all(np.isnan(mean_time_series)):
    raise ValueError("Todos los valores en la serie temporal son NaN.")

# Reducir a una única serie temporal promediando a través de los canales
mean_time_series = np.nanmean(mean_time_series, axis=0).squeeze()  # (n_times,)

# Calcular la desviación estándar de la serie temporal
std_time_series = np.nanstd(epoch_data, axis=(0, 1)).squeeze()  # (n_times,)






# Crear un arreglo de tiempo para graficar
time = epochs.times

# Aplicar corrección de línea base
epochs.apply_baseline((-0.2, 0))  # Ajusta usando los 200 ms previos al evento

# Identificar outliers
threshold=3
outliers = np.abs(epoch_data - mean_time_series) > threshold * std_time_series

normalized_epochs = (epochs - mean_time_series) / std_time_series


# Extraer los tiempos de los eventos con ID 11
event_times = epochs.events[epochs.events[:, 2] == 11, 0] / epochs.info['sfreq']  # Convertir a segundos



def plot_data(time, mean_time_series, std_time_series, output_file="ET.png"):
    # Graficar la serie temporal promedio de la pupila junto con la desviación estándar
    
    mean_time_series = np.nanmean(epoch_data, axis=0).squeeze()  # Promedio entre epochs
    std_time_series = np.nanstd(epoch_data, axis=0).squeeze()    # Desviación estándar entre epochs

    
    # Graficar la serie temporal promedio de la pupila normalizada junto con la desviación estándar
    plt.figure(figsize=(10, 6))
    plt.plot(time, mean_time_series, label='Pupil Size (Z-score)', color='blue')  # Graficar los datos normalizados
    plt.fill_between(time, mean_time_series -  std_time_series, mean_time_series +  std_time_series, color='blue', alpha=0.2, label='±1 Std Dev')  # Rellenar con la desviación estándar
    plt.xlabel('Time (s)')  # Etiqueta del eje X
    plt.ylabel('Pupil Size (Z-score)')  # Etiqueta del eje Y (normalizado)
    plt.title('mean Pupil Sizewith Standard Deviation')  # Título del gráfico
    plt.legend()  # Leyenda del gráfico
    plt.grid(True)  # Mostrar la cuadrícula
    plt.savefig(output_file)  # Guardar el gráfico como archivo de imagen
    print(f"Figura guardada como {output_file}")  # Confirmar que la figura fue guardada
    
    
    plt.show()
    
    
    








# Extraer los tiempos asociados al evento '11'
event_times = epochs.events[epochs.events[:, 2] == event_ids['12'], 0] / epochs.info['sfreq']

# Tomar el primer evento '11' como referencia para la línea vertical
first_event_time = event_times[0] if len(event_times) > 0 else None

























    























def main():
    # Verificar si el número correcto de argumentos fue pasado desde la línea de comandos
    if len(sys.argv) != 2:  # Validar número de argumentos
        print("Uso: python ET.py 'archivo.asc'")  # Instrucciones de uso
        sys.exit(1)  # Salir si el número de argumentos es incorrecto
        
    archivo = sys.argv[1]  # Ruta al archivo de datos Eyelink que se pasará como argumento
    
    
    raw_et, et_events, et_event_ids = read_data(file_path)

    # Procesar los datos (filtrado, interpolación, epochs, normalización)
    normalized_epoch_data = (epoch_data - mean_time_series) / std_time_series
    

    # Graficar los datos normalizados
    plot_data(time, mean_time_series, std_time_series)
    

  





    
    
    


if __name__ == '__main__':
    # Simulación de argumentos en Spyder (para pruebas sin argumentos de línea de comandos)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtener directorio del script
    asc_files = [f for f in os.listdir(script_dir) if f.endswith(".asc")]


     # Seleccionar el primer archivo .asc encontrado
    sys.argv = ['ET.py', os.path.join(script_dir, asc_files[0])]
    main()  # Llamar a la función principal
