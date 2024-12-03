import mne
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Lista de archivos de sujetos
file_path = [
    "C:/Users/Usuario/Desktop/Universidad/Sobre BIO295A/sujetos/ET/YCollio_filtered - copia.asc"
    # Agrega más archivos si tienes más sujetos
]


# Clase para procesar y filtrar archivos de Eyelink
class EyelinkProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.all_pupil_data = []  # guardar todo para graficar al final
        
            
    def process_all_subjects(self):
        # Itera sobre los archivos de EyeLink
        for file_path in self.file_path:
            print(f"Procesando archivo: {file_path}")
            
            # Filtra y limpia el archivo de sacadas
            filtered_file = self.directory_eyelink_file(file_path)
            
            # Si no se pudo filtrar, se salta el archivo
            if filtered_file is None:
                print(f"Saltando procesamiento para {file_path} debido a la falta de datos válidos.")
                continue
            
            # Ahora el archivo está limpio de sacadas
            cleaned_file = self.filter_saccades(filtered_file)
            
            # Si no se pudo limpiar, se salta el archivo
            if cleaned_file is None:
                print(f"Saltando procesamiento para {file_path} debido a la falta de datos válidos.")
                continue
            
            # Aquí ya no llamamos a load_and_process_eyelink_data con file_path,
            # porque ya lo estamos procesando dentro del flujo actual
            raw_et = self.filter_eyelink_data(cleaned_file)
            
            # Si los datos son válidos, entonces puedes trabajar con ellos
            if raw_et:
                self.plot_data(raw_et)
        
        
        
    def process_eyelink_file(self, eyelink_file_path):
        """Procesa un archivo de EyeLink, crea el directorio preprocesado si no existe y devuelve la ruta del archivo filtrado."""
        # Obtener el nombre base del archivo para identificar al sujeto
        subject_name = os.path.splitext(os.path.basename(eyelink_file_path))[0]
        
        # Definir el directorio de preprocesamiento
        eyelink_file_path = "C:/Users/Usuario/Desktop/Universidad/Sobre BIO295A/sujetos/preprocesamiento"
        os.makedirs(eyelink_file_path, exist_ok=True)  # Crea la carpeta si no existe
        
        # Definir la ruta dinámica para el archivo filtrado
        filtered_file_path = os.path.join(eyelink_file_path, f"{subject_name}_filtered.asc")
        
        # Preprocesar el archivo y guardar los datos filtrados
        filtered_data = self.preprocess_eyelink_file(eyelink_file_path)
        self.save_filtered_file(filtered_data, filtered_file_path)
        
        # Llamar a la función para cargar y procesar los datos filtrados
        pupil_diameter = self.load_and_process_eyelink_data(filtered_file_path)
        
        # Obtener el canal de la pupila
        pupil_channel = self.get_pupil_channel(pupil_diameter)
        print(f"Canal de pupila encontrado: {pupil_channel}")
        
        return filtered_file_path


    def directory_eyelink_file(self, eyelink_file_path):
        """Crea el directorio si no existe, devuelve la ruta del archivo filtrado."""
        # Obtener el nombre base del archivo para identificar al sujeto
        subject_name = os.path.splitext(os.path.basename(eyelink_file_path))[0]
        
        # Definir el directorio de preprocesamiento
        eyelink_file_path = "C:/Users/Usuario/Desktop/Universidad/Sobre BIO295A/sujetos/preprocesamiento"
        os.makedirs(eyelink_file_path, exist_ok=True)  # Crea la carpeta si no existe
        
        # Definir la ruta dinámica para el archivo filtrado
        filtered_file_path = os.path.join(eyelink_file_path, f"{subject_name}_filtered.asc")
        
        # Eliminar la llamada a self.save_filtered_file(filtered_file_path)
        
        return filtered_file_path
    
    
    def load_filter_data(self, filtered_file):
        # Intentar cargar el archivo de EyeLink usando MNE
        raw_et = mne.io.read_raw_eyelink(filtered_file, create_annotations=True)
        
        # Obtener eventos y sus IDs a partir de las anotaciones
        et_events, et_event_ids = mne.events_from_annotations(raw_et)
    
        # Aquí raw_et sigue siendo un objeto Raw de MNE
        return raw_et
    
    
    def load_and_process_eyelink_data(self, file_path):
        """Procesar los datos del archivo de EyeLink"""
        data = pd.read_csv(file_path, delimiter='\t', header=None)
        
        # Filtrar solo las 5 primeras columnas
        data_filtered = data.iloc[:, [0, 1, 2, 3, 4]]
        
        # Asegurarse de que la columna de diámetro pupilar esté en la cuarta columna
        pupil_diameter = data_filtered.iloc[:, 3].values  # Cuarta columna
    
        return pupil_diameter
        
    
    def get_pupil_channel(self, raw_et):
        pupil_channel = None
        # Search for 'left' or 'right' in channel names
        for ch_name in raw_et.ch_names:
            if 'left' in ch_name:
                pupil = 'pupil_left'
            elif 'right' in ch_name:
                pupil = 'pupil_right'
        
        return pupil_channel

        
    def filter_eyelink_data(self, filtered_file):
        # Paso 1: Leer y filtrar los datos
        filtered_data = self.read_and_filter_data(filtered_file)
        if not filtered_data:
            print(f"Advertencia: No hay datos válidos en {filtered_file} para procesar.")
            return None
    
        # Paso 2: Crear objeto Raw de MNE
        raw_et = self.create_raw_et(filtered_data)
    
        # Paso 3: Verificar y seleccionar los canales de pupila
        if not self.select_pupil_channels(raw_et, filtered_file):
            return None
    
        # Paso 4: Filtrar la señal para el preprocesamiento
        raw_et = self.filter_signal(raw_et)
        
        # Filtrar los datos (por ejemplo, entre 0.5 y 30 Hz)
        raw_et.filter(l_freq=0.5, h_freq=30)
    
        return raw_et
    
    
    def read_and_filter_data(self, filtered_file):
        """
        Lee, filtra, no considera valor fijo columnas"""
        filtered_data = []
        with open(filtered_file, 'r') as file:
            for line in file:
                # Eliminar espacios al inicio y al final, y separar los valores
                parts = line.strip().split()
                
                # Validaciones: que no tenga columnas con "." en las primeras 2 columnas y que la columna 3 no sea "0,0"
                if len(parts) >= 1 and not any('.' in part for part in parts[:2]) and (len(parts) < 3 or parts[2] != "0,0"):
                    filtered_data.append(parts)  # Agregar la línea completa sin imponer número fijo de columnas
        
        return filtered_data
    
    
    def create_raw_et(self, filtered_data):
        # Convertir filtered_data a DataFrame si es una lista
        if isinstance(filtered_data, list):
            filtered_data = pd.DataFrame(filtered_data)
    
        # Filtrar filas que no sean numéricas
        filtered_data_numeric = filtered_data.apply(pd.to_numeric, errors='coerce').dropna()
    
        # Crear info para el RawArray
        info = mne.create_info(ch_names=[str(ch) for ch in filtered_data_numeric.columns.tolist()], sfreq=1000, ch_types='pupil')
    
        # Crear el RawArray con los datos numéricos
        raw_et = mne.io.RawArray(filtered_data_numeric.values.T, info)
    
        # Buscar los eventos "START" y "END" en la primera columna
        start_indices = filtered_data[filtered_data.iloc[:, 0].str.contains('START', na=False)].index
        end_indices = filtered_data[filtered_data.iloc[:, 0].str.contains('END', na=False)].index
    
        # Verificar si hay al menos un par START-END
        if len(start_indices) == 0 or len(end_indices) == 0:
            raise ValueError("No se encontraron eventos 'START' o 'END' en los datos.")
    
        # Crear las épocas, suponiendo que cada par "START"-"END" define un bloque
        epochs = []
        for start, end in zip(start_indices, end_indices):
            # Seleccionamos los datos entre 'START' y 'END'
            epoch_data = filtered_data_numeric.iloc[start:end]
            
            # Puedes crear un RawArray o simplemente almacenar estos bloques en una lista
            epoch_info = mne.create_info(ch_names=[str(ch) for ch in epoch_data.columns.tolist()], sfreq=1000, ch_types='pupil')
            epoch_raw = mne.io.RawArray(epoch_data.values.T, epoch_info)
            epochs.append(epoch_raw)
    
        # Ahora 'epochs' contiene una lista de los bloques (RawArrays)
        return epochs  # Regresa la lista de las épocas



    def select_pupil_channels(self, raw_et, filtered_file):
        # Si raw_et es una lista de bloques (épocas)
        if isinstance(raw_et, list):
            for epoch in raw_et:
                if 'LEFT' in epoch.ch_names:
                    selected_channel = 'LEFT'
                elif 'RIGHT' in epoch.ch_names:
                    selected_channel = 'RIGHT'
                else:
                    continue
                # Procesar el bloque con el canal seleccionado
                print(f"Canal seleccionado: {selected_channel}")
                # Aquí añadir el código de procesamiento necesario
    
        else:
            if 'LEFT' in raw_et.ch_names:
                selected_channel = 'LEFT'
            elif 'RIGHT' in raw_et.ch_names:
                selected_channel = 'RIGHT'
            else:
                return None
            # Procesar el bloque con el canal seleccionado
            print(f"Canal seleccionado: {selected_channel}")
    
    
        
        def pick_valid_channel(self, raw_et, left_channel, right_channel):
            pupil = None  # Inicializamos pupil como None
            
            if left_channel is not None:
                pupil = left_channel
            elif right_channel is not None:
                pupil = right_channel
    
            if pupil is not None:
                raw_et.pick([pupil])
                
    
    def filter_saccades(self, filtered_file):
        """Filtra los eventos de sacadas y guarda el archivo limpio sin eventos de sacadas."""
        # Definir los eventos a filtrar (sacadas y otros relacionados)
        saccade_events = ['ESACC', 'SFIX', 'INPUT', 'MSG', 'BUTTON', 'SBLINK', 'EFIX', 'SSACC']
        
        # Leer los datos del archivo
        filtered_data = self.read_and_filter_data(filtered_file)
        
        # Verificar si hay datos en el archivo antes de filtrar
        if not filtered_data:
            print(f"Advertencia: El archivo {filtered_file} no contiene datos válidos.")
            return None
        
        # Filtrar las filas, eliminando aquellas que contienen los eventos de sacadas
        filtered_data_no_saccades = [
            row for row in filtered_data if row[0] not in saccade_events
        ]
        
        # Verificar si después de filtrar, los datos siguen presentes
        if not filtered_data_no_saccades:
            print(f"Advertencia: Después de filtrar las sacadas, el archivo {filtered_file} está vacío.")
            return None
        
        # Guardar el archivo filtrado sin las sacadas
        cleaned_file_path = filtered_file.replace(".asc", "_no_saccades.asc")
        
        # Guardar el archivo solo si tiene datos
        with open(cleaned_file_path, 'w') as f:
            for row in filtered_data_no_saccades:
                f.write(" ".join(row) + "\n")
        
        print(f"Archivo filtrado guardado como: {cleaned_file_path}")
        return cleaned_file_path
    
    
    def process_all_subjects(self):
        """Procesa todos los archivos en la lista de sujetos."""
        for file_path in self.file_path:
            print(f"Procesando archivo: {file_path}")
            
            # Obtener la ruta del archivo filtrado
            filtered_file = self.directory_eyelink_file(file_path)
            
            # Llamar a la función para filtrar las sacadas
            cleaned_file = self.filter_saccades(filtered_file)
            
            # Si el archivo filtrado es None, significa que no hubo datos válidos o no se guardó un archivo limpio
            if cleaned_file is None:
                print(f"Saltando procesamiento para {file_path} debido a la falta de datos válidos.")
                continue
            
            # Procesar el archivo limpio (sin sacadas)
            raw_et = self.filter_eyelink_data(cleaned_file)
            
            if raw_et:
                self.plot_data(raw_et)  # Llamar a la función para graficar los datos procesados
                
            print(f"Procesamiento de {file_path} finalizado.\n")

    
    def search_start_eyelink_file(self, eyelink_file_path):
        """Lee el archivo y crea épocas basadas en 'START' y 'END'."""
        lines = self.read_file(eyelink_file_path)
        epochs = self.create_epochs_from_lines(lines)
        return epochs
    
    def read_file(self, file_path):
        """Lee un archivo y retorna las líneas no vacías."""
        lines = []
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():  # Saltar líneas vacías
                    lines.append(line.strip())
        return lines
    
    
    def create_epochs_from_lines(self, lines):
        """Crea épocas a partir de las líneas del archivo."""
        epochs = []  # Lista para almacenar las épocas
        current_epoch = []  # Almacena los datos de la época actual
        start_found = False
    
        for line in lines:
            if "START" in line:
                current_epoch = self.handle_start(line, current_epoch, epochs)
                start_found = True
            elif "END" in line and start_found:
                self.handle_end(line, current_epoch, epochs)
                current_epoch = []  # Reiniciar la época
                start_found = False
            elif start_found:
                current_epoch.append(line)
        
        # Agregar la última época si no terminó con un "END"
        if current_epoch:
            epochs.append(current_epoch)
        
        return epochs
    
    def handle_start(self, line, current_epoch, epochs):
        """Maneja la lógica cuando se encuentra un 'START'."""
        if current_epoch:  # Si hay datos en la época actual, agregarla a las épocas
            epochs.append(current_epoch)
        return [line]  # Iniciar una nueva época con el "START"
    
    def handle_end(self, line, current_epoch, epochs):
        """Maneja la lógica cuando se encuentra un 'END'."""
        current_epoch.append(line)
        epochs.append(current_epoch)  # Agregar la época completa
        
    def filter_signal(self, raw_et):
        """filtrar señal, eliminando frecuencias menores a 0.5 y mayores a 30 Hz."""
        int_et = raw_et.copy()
        int_et.filter(l_freq=0.5, h_freq=30)
        return int_et           
    
    def interpolate_blinks(self, int_et):
        inter = ['BAD_blink']
        int_et=mne.preprocessing.eyetracking.interpolate_blinks(int_et, (0.01, 0.01), match=inter)
    
    
    def plot_data(self, raw_et):
        """Graficar los datos procesados."""
        raw_et.plot(scalings=dict(eyegaze=1e3))
        plt.show()  # Asegúrate de llamar a plt.show() para mostrar el gráfico



# Ejecutar el procesamiento para todos los sujetos
processor = EyelinkProcessor(file_path)
processor.process_all_subjects()


# Crear una instancia del procesador de Eyelink
eyelink_processor = EyelinkProcessor(file_path)
