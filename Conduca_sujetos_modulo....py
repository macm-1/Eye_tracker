import mne
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


# Lista de archivos de sujetos
file_paths = [
    "C:/Users/Usuario/Desktop/Universidad/Sobre BIO295A/sujetos/conducta/YCollio/exp_log_sYCollio.csv"
    # Agrega más archivos si tienes más sujetos
]


# Definir la función para cargar los datos
def load_data(file_path):
    """Lee el archivo CSV y devuelve un dataframe."""
    df = pd.read_csv(file_path)  # Leer el archivo CSV
    print(f"Datos cargados desde {file_path}")
    return df


# Función para separar los datos por columna de bloque (columna [1]) y tipo de respuesta (columna [6])
def separate_by_block_and_response(df):
    separated_data = []
    
    # Separar por Bloque (columna [1])
    for block in df[' Block_Idx'].unique():
        block_data = df[df[' Block_Idx'] == block]
        separated_data[block] = []
        
        # Separar dentro de cada bloque por tipo de respuesta (columna [6])
        for response in block_data[' Response_type'].unique():
            response_data = block_data[block_data[' Response_type'] == response]
            separated_data[block][response] = response_data
    
    return separated_data


# Cargar y separar los datos para cada sujeto
dataframes = []
for file_path in file_paths:
    df = load_data(file_path)
    subject_name = os.path.basename(file_path).replace('.csv', '')  # Nombre del sujeto
    separated_data = separate_by_block_and_response(df)
    dataframes[subject_name] = separated_data
    

# Mostrar un ejemplo de los datos separados
for subject, blocks in dataframes.items():
    print(f"\nSujeto: {subject}")
    for block, responses in blocks.items():
        for response_type, response_data in responses.items():
            print(f"  Bloque {block}, Respuesta {response_type}: {response_data.shape[0]} filas, {response_data.shape[1]} columnas")
            print(f"    Primeras filas de Bloque {block}, Respuesta {response_type}:")
            print(response_data.head())  # Mostrar las primeras filas del bloque y tipo de respuesta

#-----------------------------------------------------------------------------------

# Función para cargar y separar los datos de los sujetos
def load_and_separate_data(separated_data):
    # Inicializar las listas para almacenar los tiempos de respuesta
    reaction_times_true_pos = []
    reaction_times_true_neg = []
    reaction_times_false_pos = []
    reaction_times_false_neg = []
    
    # Recorrer los datos de los sujetos y separar los tiempos de respuesta por tipo
    for subject, blocks in separated_data.items():
        if 1 in blocks:  # Verificar que el bloque 1 existe
            block_1_data = blocks[1]  # Obtener el bloque 1

            # Asegurémonos de que block_1_data sea un DataFrame
            block_1_data = pd.DataFrame(block_1_data)
            
            # Filtrar según el tipo de respuesta (columna 6, 'Response_type')
            true_pos_data = block_1_data[block_1_data.iloc[:, 5] == 'true_pos']
            true_neg_data = block_1_data[block_1_data.iloc[:, 5] == 'true_neg']
            false_pos_data = block_1_data[block_1_data.iloc[:, 5] == 'false_pos']
            false_neg_data = block_1_data[block_1_data.iloc[:, 5] == 'false_neg']
            
            # Añadir los tiempos de respuesta a las listas correspondientes
            reaction_times_true_pos.extend(true_pos_data.iloc[:, 6])  # Columna 7: 'Response_Time'
            reaction_times_true_neg.extend(true_neg_data.iloc[:, 6])
            reaction_times_false_pos.extend(false_pos_data.iloc[:, 6])
            reaction_times_false_neg.extend(false_neg_data.iloc[:, 6])
    
    # Ver las primeras respuestas de cada categoría
    print("Primeros tiempos de respuesta (true_pos):", reaction_times_true_pos[:5])
    print("Primeros tiempos de respuesta (true_neg):", reaction_times_true_neg[:5])
    print("Primeros tiempos de respuesta (false_pos):", reaction_times_false_pos[:5])
    print("Primeros tiempos de respuesta (false_neg):", reaction_times_false_neg[:5])

    return reaction_times_true_pos, reaction_times_true_neg, reaction_times_false_pos, reaction_times_false_neg  

#----------------------------------------------------------------------------------

# Función para graficar los tiempos de reacción para cada tipo de respuesta
def plot_reaction_times(true_pos, true_neg, false_pos, false_neg):
    # Verificar si las listas tienen datos
    print(f"true_pos tiene {len(true_pos)} elementos")
    print(f"true_neg tiene {len(true_neg)} elementos")
    print(f"false_pos tiene {len(false_pos)} elementos")
    print(f"false_neg tiene {len(false_neg)} elementos")

    # Verificar si hay datos en alguna lista
    if not true_pos or not true_neg or not false_pos or not false_neg:
        print("No hay datos suficientes para graficar")
        return

    # Graficar los tiempos de reacción para cada tipo de respuesta
    plt.figure(figsize=(10, 6))

    # Crear un histograma para cada tipo de respuesta
    plt.hist(true_pos, bins=20, alpha=0.5, label='True Positive', color='g')
    plt.hist(true_neg, bins=20, alpha=0.5, label='True Negative', color='b')
    plt.hist(false_pos, bins=20, alpha=0.5, label='False Positive', color='r')
    plt.hist(false_neg, bins=20, alpha=0.5, label='False Negative', color='y')

    # Añadir etiquetas y título
    plt.xlabel('Tiempo de Reacción (segundos)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Tiempos de Reacción por Tipo de Respuesta')
    plt.legend(loc='upper right')

    # Mostrar el gráfico
    plt.show()

# Llamar a la función load_and_separate_data para obtener los tiempos de reacción
reaction_times_true_pos, reaction_times_true_neg, reaction_times_false_pos, reaction_times_false_neg = load_and_separate_data(dataframes)

# Llamar a la función plot para graficar
plot_reaction_times(reaction_times_true_pos, reaction_times_true_neg, reaction_times_false_pos, reaction_times_false_neg)
