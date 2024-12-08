import pandas as pd
import sys
import os
import mne
import numpy as np
import matplotlib.pyplot as plt


# Directorio donde estan los archivos
folder_path = os.path.dirname(os.path.abspath(__file__))
print(f"Directorio donde se buscan los archivos: {folder_path}")


# Buscar archivos que terminen en .csv en el directorio actual
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
print(f"Archivos encontrados: {csv_files}")


if not csv_files:
    raise FileNotFoundError("No se encontraron archivos .csv en el repositorio.")

# Usar el primer archivo encontrado como ejemplo
selected_file_path = os.path.join(folder_path, csv_files[0])
print(f"Ruta seleccionada: {selected_file_path}")


# Verificar que el archivo exista
if not os.path.isfile(selected_file_path):
    raise FileNotFoundError(f"No se puede encontrar el archivo: {selected_file_path}")

# Función para leer un archivo CSV
def read_data(selected_file_path):
    '''Lee el archivo CSV y devuelve un dataframe.'''
    df = pd.read_csv(selected_file_path)  # Leer el archivo CSV
    print(f"Datos cargados desde {selected_file_path}")
    print(df.head())  # Mostrar las primeras filas del dataframe cargado
    return df

# Leer el archivo
df = read_data(selected_file_path)
   
#--------------------------------------------------------------------------------

# Limpiar espacios de los nombres de las columnas
df.columns = df.columns.str.strip()



# Comprobar los nombres de las columnas
print(f"las columnas encontradas son {df.columns}")


if 'n_Targets' in df.columns:
    print(df['n_Targets'].head())  # Imprimir los primeros valores
    print(df['Response_type'].head())
else:
    print("La columna 'n_Targets' no existe en el DataFrame.")
    print("La columna 'Response_type' no existe en el DataFrame.")
    
    

abs_Time = df['Abs_Time']
block_Idx = df['Block_Idx']
trial_Idx = df['Trial_Idx']
n_Targets = df['n_Targets']
asked_for_target = df['Asked_for_target']
response_type = df['Response_type']
response_time = df['Response_Time']


# Convertir la columna 'Response_Time' a numérico, forzando que los valores no válidos se conviertan en NaN
df['Response_Time'] = pd.to_numeric(df['Response_Time'], errors='coerce')

# Si prefieres eliminar las filas con NaN después de la conversión:
df = df.dropna(subset=['Response_Time'])

# o reemplzar las filas NaN por el promedio
#df['Response_Time'] = df['Response_Time'].fillna(df['Response_Time'].mean())

#_________________________________________________________

# Filtrar datos por número de targets (en este caso, 2)
filtered_data = df[df['n_Targets'] == 2]


# Calcular el promedio y la desviación estándar de 'Response_Time' por 'Abs_Time'
mean_response_time = filtered_data.groupby('Abs_Time')['Response_Time'].mean()
std_response_time = filtered_data.groupby('Abs_Time')['Response_Time'].std()

# Graficar los tiempos de respuesta en función del tiempo absoluto
plt.figure(figsize=(5, 3))

# Rellenar con la desviación estándar (±1 Std Dev)
plt.fill_between(mean_response_time.index, 
                 mean_response_time - std_response_time, 
                 mean_response_time + std_response_time, 
                 color='blue', alpha=0.2, label='±1 Std Dev')


# Graficar el promedio de los tiempos de respuesta
plt.plot(mean_response_time.index, mean_response_time, label='Mean Response Time', color='blue')

# Definir el nombre del archivo de salida
output_file = "csv [0].png"

# Etiquetas y título
plt.xlabel('Absolute Time (s)')
plt.ylabel('Response Time (s)')
plt.title('Response Time vs Absolute Time (with Std Dev) - 2')
plt.xlim ()
plt.ylim ()

# Mostrar la leyenda y la cuadrícula
plt.legend()
plt.grid(True)

plt.savefig(output_file)  # Guardar el gráfico como archivo de imagen
print(f"Figura guardada como {output_file}")  # Confirmar que la figura fue guardada
# Mostrar el gráfico
plt.show()

#__________________________________________________________________________

"""
# Filtrar datos por 'n_Targets' igual a 2 y 'Response_type' igual a 'true_pos'
filtered_data = df[(df['n_Targets'] == 2) & (df['Response_type'] == 'true_pos')]

# Calcular el promedio y la desviación estándar de 'Response_Time' por 'Response_type'
mean_response_time = filtered_data.groupby('Response_Time').mean()
std_response_time = filtered_data.groupby('Response_Time').std()

# Graficar los tiempos de respuesta en función del tipo de respuesta
plt.figure(figsize=(5, 3))

# Rellenar con la desviación estándar (±1 Std Dev)
plt.fill_between(mean_response_time.index, 
                 mean_response_time - std_response_time, 
                 mean_response_time + std_response_time, 
                 color='blue', alpha=0.2, label='±1 Std Dev')

# Graficar el promedio de los tiempos de respuesta
plt.plot(mean_response_time.index, mean_response_time, label='Mean Response Time', color='blue')

# Etiquetas y título
plt.xlabel('Response Type')
plt.ylabel('Response Time (s)')
plt.title('Response Time vs Response Type (with Std Dev) - 2')

# Limitar los ejes (ajustar según sea necesario)
plt.xlim()  
plt.ylim()  

# Mostrar la leyenda y la cuadrícula
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()

"""












def main():
    # Verificar si el número correcto de argumentos fue pasado desde la línea de comandos
    if len(sys.argv) != 2:  # Validar número de argumentos
        print("Uso: python Código_files_csv.py 'archivo.csv'")  # Instrucciones de uso
        sys.exit(1)  # Salir si el número de argumentos es incorrecto
    
    # Obtener la ruta del archivo CSV desde los argumentos
    selected_file_path = sys.argv[1]
    
    # Verificar si el archivo existe
    if not os.path.isfile(selected_file_path):
        print(f"Error: El archivo '{selected_file_path}' no existe.")
        sys.exit(1)
    
    # Leer y procesar el archivo CSV
    df = read_data(selected_file_path)
    print("Archivo procesado con éxito.")
     






if __name__ == '__main__':
    # Obtener el directorio actual del script
    folder_path = os.path.dirname(os.path.abspath(__file__))  
    print(f"Directorio del script: {folder_path}")
    
    # Buscar archivos .csv en el directorio
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    if not csv_files:
        print("No se encontraron archivos .csv en el directorio actual.")
        sys.exit(1)

    # Seleccionar el primer archivo .csv encontrado
    selected_file_path = os.path.join(folder_path, csv_files[0])
    print(f"Archivo seleccionado: {selected_file_path}")

    # Simulación de argumentos en Spyder
    sys.argv = ['Código_files_csv.py', selected_file_path]

    # Llamar a la función principal
    main()