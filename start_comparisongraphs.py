# Autore: Tomas Lovato
# Data: 2024/08/22 14:00
# Grafici di comparazione tra gli output dei PC#1 e PC#2

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm

# Variabile globale per decidere se mostrare o salvare i grafici
SHOW_PLOTS = False

# Funzione per leggere i dati dal file
def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        line = line.strip()
        if line:
            fields = line.split('|')
            data.append([int(fields[1]), int(fields[2]), int(fields[3]), int(fields[4]), int(fields[5]), float(fields[6]), float(fields[7]), float(fields[8]), int(fields[9])])

    columns = ['msg_len', 'signed_msg_len', 'pub_key_size', 'priv_key_size', 'signature_size', 'keygen_time', 'sign_time', 'verify_time', 'hash_len']

    df = pd.DataFrame(data, columns=columns)
    return df

# Funzione per salvare o mostrare il grafico
def save_or_show_plot(filename):
    if SHOW_PLOTS:
        plt.show()
    else:
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(filename)
    plt.clf()

# Funzione per leggere e unire i dati da più file
def read_multiple_files(filenames):
    dataframes = [read_data(file) for file in filenames]
    for df, file in zip(dataframes, filenames):
        df['algorithm'] = file.split('/')[3]  # estrai il nome dell'algoritmo dal nome del file
        # Aggiungi colonna per distinguere tra REF e AVX2
        if 'avx2' in file:
            df['device'] = 'AVX2'
        else:
            df['device'] = 'REF'
        # Aggiungi colonna per distinguere tra PC#1 e PC#2
        if 'i9' in file:
            df['device'] = 'PC#1 i9 - AVX2'
        else:
            df['device'] = 'PC#2 i7 - AVX2'
    return pd.concat(dataframes, ignore_index=True)

# Dizionario per mappare i nomi degli algoritmi ai nuovi nomi
algorithm_name_mapping = {
    'dilithium2_avx2': 'Dilithium 2',
    'dilithium3_avx2': 'Dilithium 3',
    'dilithium5_avx2': 'Dilithium 5',
    'dilithium2_sha256_avx2': 'Dilithium 2 SHA-256',
    'dilithium3_sha256_avx2': 'Dilithium 3 SHA-256',
    'dilithium5_sha256_avx2': 'Dilithium 5 SHA-256',
    'dilithium2_sha512_avx2': 'Dilithium 2 SHA-512',
    'dilithium3_sha512_avx2': 'Dilithium 3 SHA-512',
    'dilithium5_sha512_avx2': 'Dilithium 5 SHA-512',
    'falcon2_avx2': 'Falcon 512',
    'falcon5_avx2': 'Falcon 1024',
    'falcon2_avx2_sha256': 'Falcon 2 SHA-256',
    'falcon5_avx2_sha256': 'Falcon 5 SHA-256',
    'falcon2_avx2_sha512': 'Falcon 2 SHA-512',
    'falcon5_avx2_sha512': 'Falcon 5 SHA-512',
    'sphincs128_avx2': 'SPHINCS+ 128',
    'sphincs192_avx2': 'SPHINCS+ 192',
    'sphincs256_avx2': 'SPHINCS+ 256',
    'sphincs128_sha256_avx2': 'SPHINCS+ 128 SHA-256',
    'sphincs192_sha256_avx2': 'SPHINCS+ 192 SHA-256',
    'sphincs256_sha256_avx2': 'SPHINCS+ 256 SHA-256',
    'sphincs128_sha512_avx2': 'SPHINCS+ 128 SHA-512',
    'sphincs192_sha512_avx2': 'SPHINCS+ 192 SHA-512',
    'sphincs256_sha512_avx2': 'SPHINCS+ 256 SHA-512',
    'rsa_80_sha256': 'RSA 1024',
    'rsa_80_sha512': 'RSA 1024',
    'rsa_112_sha256': 'RSA 2048',
    'rsa_112_sha512': 'RSA 2048',
    'rsa_128_sha256': 'RSA 3072',
    'rsa_128_sha512': 'RSA 3072',
    'rsa_192_sha256': 'RSA 7680',
    'rsa_192_sha512': 'RSA 7680',
    'rsa_256_sha256': 'RSA 15360',
    'rsa_256_sha512': 'RSA 15360',
    'risultati_Dilithium2_avx2': 'Dilithium 2 LIBOQS',
    'risultati_Dilithium3_avx2': 'Dilithium 3 LIBOQS',
    'risultati_Dilithium5_avx2': 'Dilithium 5 LIBOQS',
    'risultati_Falcon-512_avx2': 'Falcon 512 LIBOQS',
    'risultati_Falcon-1024_avx2': 'Falcon 1024 LIBOQS',
    'risultati_SPHINCS+-SHA2-128f-simple_avx2': 'SPHINCS+ 128 LIBOQS',
    'risultati_SPHINCS+-SHA2-192f-simple_avx2': 'SPHINCS+ 192 LIBOQS',
    'risultati_SPHINCS+-SHA2-256f-simple_avx2': 'SPHINCS+ 256 LIBOQS'
}

plot_colors = {
    'PC#1 i9 - AVX2': '#1b8dc1',
    'PC#2 i7 - AVX2': '#9b0014'
}



### ================================================
### ======== TEMPI DI KEYGEN TRA ALGORITMI =========
### ================================================

# Funzione per creare il grafico con la media dei tempi di keygen
def create_keygen_time_histogram(df_all, output_file, title):
    plt.figure(figsize=(12,7))

    # Calcola la media dei tempi di keygen per ogni algoritmo e versione
    df_mean_keygen_time = df_all.groupby(['algorithm', 'device'])['keygen_time'].mean().reset_index()
    
    # Crea un grafico a barre
    sns.barplot(x='algorithm', y='keygen_time', hue='device', data=df_mean_keygen_time, palette=plot_colors)

    plt.xlabel('Algorithms and Versions')
    plt.ylabel('Average Keygen Time (seconds)')
    plt.title('Device Performance Comparison - Average Keygen Time - ' + title)
    plt.legend(title='Device')
    plt.yscale('log')
    plt.grid(True)
    
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [
    [['./output/20240822_i9/dilithium2_avx2',   './output/20240822_i9/dilithium3_avx2', './output/20240822_i9/dilithium5_avx2', './output/20240822_i7/dilithium2_avx2',   './output/20240822_i7/dilithium3_avx2', './output/20240822_i7/dilithium5_avx2'], 'TM_KG_dilithium.png', 'Dilithium Versions'],
    [['./output/20240822_i9/falcon2_avx2',      './output/20240822_i9/falcon5_avx2', './output/20240822_i7/falcon2_avx2',      './output/20240822_i7/falcon5_avx2'],   'TM_KG_falcon.png', 'Falcon Versions'],
    [['./output/20240822_i9/sphincs128_avx2',   './output/20240822_i9/sphincs192_avx2', './output/20240822_i9/sphincs256_avx2','./output/20240822_i7/sphincs128_avx2',   './output/20240822_i7/sphincs192_avx2', './output/20240822_i7/sphincs256_avx2'], 'TM_KG_sphincs.png', 'Sphincs+ Versions'],
    [['./output/20240822_i9/rsa_80_sha256',    './output/20240822_i9/rsa_112_sha256',  './output/20240822_i9/rsa_128_sha256',    './output/20240822_i9/rsa_192_sha256',  './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/rsa_80_sha256',    './output/20240822_i7/rsa_112_sha256',  './output/20240822_i7/rsa_128_sha256',    './output/20240822_i7/rsa_192_sha256',  './output/20240822_i7/rsa_256_sha256'], 'TM_KG_rsa.png', 'RSA Versions'],
    [['./output/20240822_i9/dilithium2_avx2',   './output/20240822_i9/falcon2_avx2',    './output/20240822_i9/sphincs128_avx2', './output/20240822_i9/rsa_128_sha256', './output/20240822_i7/dilithium2_avx2',   './output/20240822_i7/falcon2_avx2',    './output/20240822_i7/sphincs128_avx2', './output/20240822_i7/rsa_128_sha256'], 'TM_KG_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/20240822_i9/dilithium3_avx2',   './output/20240822_i9/sphincs192_avx2', './output/20240822_i9/rsa_192_sha256', './output/20240822_i7/dilithium3_avx2',   './output/20240822_i7/sphincs192_avx2', './output/20240822_i7/rsa_192_sha256'], 'TM_KG_192bit_security_level.png', 'Security Level 3'],
    [['./output/20240822_i9/dilithium5_avx2',   './output/20240822_i9/falcon5_avx2',    './output/20240822_i9/sphincs256_avx2', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/dilithium5_avx2',   './output/20240822_i7/falcon5_avx2',    './output/20240822_i7/sphincs256_avx2', './output/20240822_i7/rsa_256_sha256'], 'TM_KG_256bit_security_level.png', 'Security Level 5'],
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating KeyGen Time Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con la media dei tempi di keygen
        create_keygen_time_histogram(df_all, './plot/comparison/Time_Keygen/' + file_paths[1], file_paths[2])





# Dizionario per mappare i nomi degli algoritmi ai nuovi nomi
algorithm_name_mapping = {
    'dilithium2_avx2': 'Dilithium 2',
    'dilithium3_avx2': 'Dilithium 3',
    'dilithium5_avx2': 'Dilithium 5',
    'dilithium2_sha256_avx2': 'Dilithium 2 SHA-256',
    'dilithium3_sha256_avx2': 'Dilithium 3 SHA-256',
    'dilithium5_sha256_avx2': 'Dilithium 5 SHA-256',
    'dilithium2_sha512_avx2': 'Dilithium 2 SHA-512',
    'dilithium3_sha512_avx2': 'Dilithium 3 SHA-512',
    'dilithium5_sha512_avx2': 'Dilithium 5 SHA-512',
    'falcon2_avx2': 'Falcon 512',
    'falcon5_avx2': 'Falcon 1024',
    'falcon2_avx2_sha256': 'Falcon 2 SHA-256',
    'falcon5_avx2_sha256': 'Falcon 5 SHA-256',
    'falcon2_avx2_sha512': 'Falcon 2 SHA-512',
    'falcon5_avx2_sha512': 'Falcon 5 SHA-512',
    'sphincs128_avx2': 'SPHINCS+ 128',
    'sphincs192_avx2': 'SPHINCS+ 192',
    'sphincs256_avx2': 'SPHINCS+ 256',
    'sphincs128_sha256_avx2': 'SPHINCS+ 128 SHA-256',
    'sphincs192_sha256_avx2': 'SPHINCS+ 192 SHA-256',
    'sphincs256_sha256_avx2': 'SPHINCS+ 256 SHA-256',
    'sphincs128_sha512_avx2': 'SPHINCS+ 128 SHA-512',
    'sphincs192_sha512_avx2': 'SPHINCS+ 192 SHA-512',
    'sphincs256_sha512_avx2': 'SPHINCS+ 256 SHA-512',
    'rsa_80_sha256': 'RSA 80 SHA-256',
    'rsa_80_sha512': 'RSA 80 SHA-512',
    'rsa_112_sha256': 'RSA 112 SHA-256',
    'rsa_112_sha512': 'RSA 112 SHA-512',
    'rsa_128_sha256': 'RSA 128 SHA-256',
    'rsa_128_sha512': 'RSA 128 SHA-512',
    'rsa_192_sha256': 'RSA 192 SHA-256',
    'rsa_192_sha512': 'RSA 192 SHA-512',
    'rsa_256_sha256': 'RSA 256 SHA-256',
    'rsa_256_sha512': 'RSA 256 SHA-512',
    'risultati_Dilithium2_avx2': 'Dilithium 2 LIBOQS',
    'risultati_Dilithium3_avx2': 'Dilithium 3 LIBOQS',
    'risultati_Dilithium5_avx2': 'Dilithium 5 LIBOQS',
    'risultati_Falcon-512_avx2': 'Falcon 512 LIBOQS',
    'risultati_Falcon-1024_avx2': 'Falcon 1024 LIBOQS',
    'risultati_SPHINCS+-SHA2-128f-simple_avx2': 'SPHINCS+ 128 LIBOQS',
    'risultati_SPHINCS+-SHA2-192f-simple_avx2': 'SPHINCS+ 192 LIBOQS',
    'risultati_SPHINCS+-SHA2-256f-simple_avx2': 'SPHINCS+ 256 LIBOQS'
}





### ================================================
### ======== TEMPI DI FIRMA TRA ALGORITMI ==========
### ================================================

# Funzione per creare il grafico con simboli diversi per REF e AVX2
def create_sign_time_plot(df_all, output_file, title):
    plt.figure(figsize=(10,6))
    
    # Definisci la palette di colori per gli algoritmi
    palette = sns.color_palette("tab10", n_colors=len(df_all['algorithm'].unique()))
    color_mapping = {algorithm: color for algorithm, color in zip(df_all['algorithm'].unique(), palette)}
    
    # Definisci i marcatori per le versioni
    markers = {'PC#1 i9 - AVX2': 'o', 'PC#2 i7 - AVX2': 'X'}
    
    # Disegna le linee
    for algorithm in df_all['algorithm'].unique():
        for device in ['PC#1 i9 - AVX2', 'PC#2 i7 - AVX2']:
            subset = df_all[(df_all['algorithm'] == algorithm) & (df_all['device'] == device)]
            if not subset.empty:
                sns.lineplot(x='msg_len', y='sign_time', data=subset, marker=markers[device], color=color_mapping[algorithm], label=f'{algorithm} {device}')
    
    plt.xlabel('Message Length (bytes)')
    plt.ylabel('Sign Time (seconds)')
    plt.title('Device Performance Comparison - Sign Time vs Message Length - ' + title)
    plt.legend(title='Algorithm and Device')
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [# NORMAL VERSIONS
    [['./output/20240822_i9/dilithium2_avx2', './output/20240822_i9/dilithium3_avx2', './output/20240822_i9/dilithium5_avx2', './output/20240822_i7/dilithium2_avx2', './output/20240822_i7/dilithium3_avx2', './output/20240822_i7/dilithium5_avx2'], 'TM_SG_dilithium.png', 'Dilithium Versions'],
    [['./output/20240822_i9/falcon2_avx2', './output/20240822_i9/falcon5_avx2', './output/20240822_i7/falcon2_avx2', './output/20240822_i7/falcon5_avx2'], 'TM_SG_falcon.png', 'Falcon Versions'],
    [['./output/20240822_i9/sphincs128_avx2', './output/20240822_i9/sphincs192_avx2', './output/20240822_i9/sphincs256_avx2', './output/20240822_i7/sphincs128_avx2', './output/20240822_i7/sphincs192_avx2', './output/20240822_i7/sphincs256_avx2'], 'TM_SG_sphincs.png', 'Sphincs+ Versions'],
    [['./output/20240822_i9/rsa_80_sha256', './output/20240822_i9/rsa_80_sha512', './output/20240822_i9/rsa_112_sha256',  './output/20240822_i9/rsa_112_sha512',  './output/20240822_i9/rsa_128_sha256', './output/20240822_i9/rsa_128_sha512', './output/20240822_i9/rsa_192_sha256', './output/20240822_i9/rsa_192_sha512', './output/20240822_i9/rsa_256_sha256', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/rsa_80_sha256', './output/20240822_i7/rsa_80_sha512', './output/20240822_i7/rsa_112_sha256',  './output/20240822_i7/rsa_112_sha512',  './output/20240822_i7/rsa_128_sha256', './output/20240822_i7/rsa_128_sha512', './output/20240822_i7/rsa_192_sha256', './output/20240822_i7/rsa_192_sha512', './output/20240822_i7/rsa_256_sha256', './output/20240822_i7/rsa_256_sha512'], 'TM_SG_rsa.png', 'RSA Versions'],
    # WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/dilithium5_sha256_avx2'], 'deprecated/TM_SG_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
    [['./output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/falcon5_avx2_sha256'], 'deprecated/TM_SG_falcon_sha256.png', 'Falcon Versions with SHA-256'],
    [['./output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/sphincs256_sha256_avx2'], 'deprecated/TM_SG_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
    [['./output/20240822_i9/rsa_80_sha256', './output/20240822_i9/rsa_112_sha256',  './output/20240822_i9/rsa_128_sha256', './output/20240822_i9/rsa_192_sha256', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/rsa_80_sha256',    './output/20240822_i7/rsa_112_sha256',  './output/20240822_i7/rsa_128_sha256', './output/20240822_i7/rsa_192_sha256', './output/20240822_i7/rsa_256_sha256'], 'deprecated/TM_SG_rsa_sha256.png', 'RSA Versions with SHA-256'],
    # WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/dilithium5_sha512_avx2'], 'deprecated/TM_SG_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
    [['./output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/falcon5_avx2_sha512'], 'deprecated/TM_SG_falcon_sha512.png', 'Falcon Versions with SHA-512'],
    [['./output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/sphincs256_sha512_avx2'], 'deprecated/TM_SG_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
    [['./output/20240822_i9/rsa_80_sha512', './output/20240822_i9/rsa_112_sha512',  './output/20240822_i9/rsa_128_sha512', './output/20240822_i9/rsa_192_sha512', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/rsa_80_sha512', './output/20240822_i7/rsa_112_sha512',  './output/20240822_i7/rsa_128_sha512', './output/20240822_i7/rsa_192_sha512', './output/20240822_i7/rsa_256_sha512'], 'deprecated/TM_SG_rsa_sha512.png', 'RSA Versions with SHA-512'],
    # ONLY DILITHIUM 2,3,5
    [['./output/20240822_i9/dilithium2_avx2', './output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i7/dilithium2_avx2', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/dilithium2_sha512_avx2'], 'TM_SG_dilithium_2_All.png', 'Dilithium 2 Versions vs SHA'],
    [['./output/20240822_i9/dilithium3_avx2', './output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i7/dilithium3_avx2', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/dilithium3_sha512_avx2'], 'TM_SG_dilithium_3_All.png', 'Dilithium 3 Versions vs SHA'],
    [['./output/20240822_i9/dilithium5_avx2', './output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i7/dilithium5_avx2', './output/20240822_i7/dilithium5_sha256_avx2', './output/20240822_i7/dilithium5_sha512_avx2'], 'TM_SG_dilithium_5_All.png', 'Dilithium 5 Versions vs SHA'],
    # ONLY FALCON 512 and 1024
    [['./output/20240822_i9/falcon2_avx2', './output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i7/falcon2_avx2', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/falcon2_avx2_sha512'], 'TM_SG_falcon_2_All.png', 'Falcon 2 Versions vs SHA'],
    [['./output/20240822_i9/falcon5_avx2', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i7/falcon5_avx2', './output/20240822_i7/falcon5_avx2_sha256', './output/20240822_i7/falcon5_avx2_sha512'], 'TM_SG_falcon_5_All.png', 'Falcon 5 Versions vs SHA'],
    # ONLY SPHINCS+ 128,192,256
    [['./output/20240822_i9/sphincs128_avx2', './output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i7/sphincs128_avx2', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/sphincs128_sha512_avx2'], 'TM_SG_sphincs_128_All.png', 'SPHINCS+ 128 Versions vs SHA'],
    [['./output/20240822_i9/sphincs192_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i7/sphincs192_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/sphincs192_sha512_avx2'], 'TM_SG_sphincs_192_All.png', 'SPHINCS+ 192 Versions vs SHA'],
    [['./output/20240822_i9/sphincs256_avx2', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i7/sphincs256_avx2', './output/20240822_i7/sphincs256_sha256_avx2', './output/20240822_i7/sphincs256_sha512_avx2'], 'TM_SG_sphincs_256_All.png', 'SPHINCS+ 256 Versions vs SHA'],
    # DIFFERENT SECURITY LEVELS WITH NO SHA
    [['./output/20240822_i9/dilithium2_avx2', './output/20240822_i9/falcon2_avx2', './output/20240822_i9/sphincs128_avx2', './output/20240822_i7/dilithium2_avx2', './output/20240822_i7/falcon2_avx2', './output/20240822_i7/sphincs128_avx2'], 'TM_SG_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/20240822_i9/dilithium3_avx2', './output/20240822_i9/sphincs192_avx2', './output/20240822_i7/dilithium3_avx2', './output/20240822_i7/sphincs192_avx2'], 'TM_SG_192bit_security_level.png', 'Security Level 3'],
    [['./output/20240822_i9/dilithium5_avx2', './output/20240822_i9/falcon5_avx2', './output/20240822_i9/sphincs256_avx2', './output/20240822_i7/dilithium5_avx2', './output/20240822_i7/falcon5_avx2', './output/20240822_i7/sphincs256_avx2'], 'TM_SG_256bit_security_level.png', 'Security Level 5'],
    # DIFFERENT SECURITY LEVELS WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/rsa_128_sha256', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/rsa_128_sha256'], 'deprecated/TM_SG_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
    [['./output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/rsa_192_sha256', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/rsa_192_sha256'], 'deprecated/TM_SG_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
    [['./output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/dilithium5_sha256_avx2', './output/20240822_i7/falcon5_avx2_sha256', './output/20240822_i7/sphincs256_sha256_avx2', './output/20240822_i7/rsa_256_sha256'], 'deprecated/TM_SG_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
    # DIFFERENT SECURITY LEVELS WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/rsa_128_sha512', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/rsa_128_sha512'], 'deprecated/TM_SG_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
    [['./output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/rsa_192_sha512', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/rsa_192_sha512'], 'deprecated/TM_SG_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
    [['./output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/dilithium5_sha512_avx2', './output/20240822_i7/falcon5_avx2_sha512', './output/20240822_i7/sphincs256_sha512_avx2', './output/20240822_i7/rsa_256_sha512'], 'deprecated/TM_SG_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512'],
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Sign Time Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_sign_time_plot(df_all, './plot/comparison/Time_Sign/' + file_paths[1], file_paths[2])




### =========================================================
### === TEMPI DI FIRMA TRA ALGORITMI con SHA - ISTOGRAMMI ===
### =========================================================

# Funzione per creare il grafico a barre con il tempo medio di firma
def create_sign_time_histogram_plot(df_all, output_file, title):
    plt.figure(figsize=(12,7))
    
    # Calcola il tempo medio di firma per ogni combinazione di algoritmo e versione
    avg_sign_times = df_all.groupby(['algorithm', 'device'])['sign_time'].mean().reset_index()
    
    # Crea il grafico a barre
    sns.barplot(x='algorithm', y='sign_time', hue='device', data=avg_sign_times, palette=plot_colors)
    
    plt.xlabel('Algorithm')
    plt.ylabel('Average Sign Time (seconds)')
    plt.title('Device Performance Comparison - Average Sign Time by Algorithm and Version - ' + title)
    plt.legend(title='Device')
    plt.grid(True)
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [ # WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/dilithium5_sha256_avx2'], 'TM_SG_H_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
    [['./output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/falcon5_avx2_sha256'], 'TM_SG_H_falcon_sha256.png', 'Falcon Versions with SHA-256'],
    [['./output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/sphincs256_sha256_avx2'], 'TM_SG_H_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
    [['./output/20240822_i9/rsa_80_sha256', './output/20240822_i9/rsa_112_sha256',  './output/20240822_i9/rsa_128_sha256', './output/20240822_i9/rsa_192_sha256', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/rsa_80_sha256',    './output/20240822_i7/rsa_112_sha256',  './output/20240822_i7/rsa_128_sha256', './output/20240822_i7/rsa_192_sha256', './output/20240822_i7/rsa_256_sha256'], 'deprecated/TM_SG_rsa_sha256.png', 'RSA Versions with SHA-256'],
    # WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/dilithium5_sha512_avx2'], 'TM_SG_H_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
    [['./output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/falcon5_avx2_sha512'], 'TM_SG_H_falcon_sha512.png', 'Falcon Versions with SHA-512'],
    [['./output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/sphincs256_sha512_avx2'], 'TM_SG_H_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
    [['./output/20240822_i9/rsa_80_sha512', './output/20240822_i9/rsa_112_sha512',  './output/20240822_i9/rsa_128_sha512', './output/20240822_i9/rsa_192_sha512', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/rsa_80_sha512', './output/20240822_i7/rsa_112_sha512',  './output/20240822_i7/rsa_128_sha512', './output/20240822_i7/rsa_192_sha512', './output/20240822_i7/rsa_256_sha512'], 'deprecated/TM_SG_rsa_sha512.png', 'RSA Versions with SHA-512'],
    # DIFFERENT SECURITY LEVELS WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/rsa_128_sha256', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/rsa_128_sha256'], 'TM_SG_H_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
    [['./output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/rsa_192_sha256', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/rsa_192_sha256'], 'TM_SG_H_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
    [['./output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/dilithium5_sha256_avx2', './output/20240822_i7/falcon5_avx2_sha256', './output/20240822_i7/sphincs256_sha256_avx2', './output/20240822_i7/rsa_256_sha256'], 'TM_SG_H_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
    # DIFFERENT SECURITY LEVELS WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/rsa_128_sha512', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/rsa_128_sha512'], 'TM_SG_H_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
    [['./output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/rsa_192_sha512', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/rsa_192_sha512'], 'TM_SG_H_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
    [['./output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/dilithium5_sha512_avx2', './output/20240822_i7/falcon5_avx2_sha512', './output/20240822_i7/sphincs256_sha512_avx2', './output/20240822_i7/rsa_256_sha512'], 'TM_SG_H_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512']
]



# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Sign Time H-Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_sign_time_histogram_plot(df_all, './plot/comparison/Time_Sign/' + file_paths[1], file_paths[2])


### ================================================
### ======= TEMPI DI VERIFICA TRA ALGORITMI ========
### ================================================

# Funzione per creare il grafico con simboli diversi per REF e AVX2
def create_verify_time_plot(df_all, output_file, title):
    plt.figure(figsize=(10,6))
    
    # Definisci la palette di colori per gli algoritmi
    palette = sns.color_palette("tab10", n_colors=len(df_all['algorithm'].unique()))
    color_mapping = {algorithm: color for algorithm, color in zip(df_all['algorithm'].unique(), palette)}
    
    # Definisci i marcatori per le versioni
    markers = {'PC#1 i9 - AVX2': 'o', 'PC#2 i7 - AVX2': 'X'}
    
    # Disegna le linee
    for algorithm in df_all['algorithm'].unique():
        for device in ['PC#1 i9 - AVX2', 'PC#2 i7 - AVX2']:
            subset = df_all[(df_all['algorithm'] == algorithm) & (df_all['device'] == device)]
            if not subset.empty:
                sns.lineplot(x='msg_len', y='verify_time', data=subset, marker=markers[device], color=color_mapping[algorithm], label=f'{algorithm} {device}')
    
    plt.xlabel('Message Length (bytes)')
    plt.ylabel('Verify Time (seconds)')
    plt.title('Device Performance Comparison - Verify Time vs Message Length - ' + title)
    plt.legend(title='Algorithm and Device')
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [# NORMAL VERSIONS
    [['./output/20240822_i9/dilithium2_avx2', './output/20240822_i9/dilithium3_avx2', './output/20240822_i9/dilithium5_avx2', './output/20240822_i7/dilithium2_avx2', './output/20240822_i7/dilithium3_avx2', './output/20240822_i7/dilithium5_avx2'], 'TM_SG_dilithium.png', 'Dilithium Versions'],
    [['./output/20240822_i9/falcon2_avx2', './output/20240822_i9/falcon5_avx2', './output/20240822_i7/falcon2_avx2', './output/20240822_i7/falcon5_avx2'], 'TM_SG_falcon.png', 'Falcon Versions'],
    [['./output/20240822_i9/sphincs128_avx2', './output/20240822_i9/sphincs192_avx2', './output/20240822_i9/sphincs256_avx2', './output/20240822_i7/sphincs128_avx2', './output/20240822_i7/sphincs192_avx2', './output/20240822_i7/sphincs256_avx2'], 'TM_SG_sphincs.png', 'Sphincs+ Versions'],
    [['./output/20240822_i9/rsa_80_sha256', './output/20240822_i9/rsa_80_sha512', './output/20240822_i9/rsa_112_sha256',  './output/20240822_i9/rsa_112_sha512',  './output/20240822_i9/rsa_128_sha256', './output/20240822_i9/rsa_128_sha512', './output/20240822_i9/rsa_192_sha256', './output/20240822_i9/rsa_192_sha512', './output/20240822_i9/rsa_256_sha256', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/rsa_80_sha256', './output/20240822_i7/rsa_80_sha512', './output/20240822_i7/rsa_112_sha256',  './output/20240822_i7/rsa_112_sha512',  './output/20240822_i7/rsa_128_sha256', './output/20240822_i7/rsa_128_sha512', './output/20240822_i7/rsa_192_sha256', './output/20240822_i7/rsa_192_sha512', './output/20240822_i7/rsa_256_sha256', './output/20240822_i7/rsa_256_sha512'], 'TM_SG_rsa.png', 'RSA Versions'],
    # WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/dilithium5_sha256_avx2'], 'deprecated/TM_SG_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
    [['./output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/falcon5_avx2_sha256'], 'deprecated/TM_SG_falcon_sha256.png', 'Falcon Versions with SHA-256'],
    [['./output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/sphincs256_sha256_avx2'], 'deprecated/TM_SG_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
    [['./output/20240822_i9/rsa_80_sha256', './output/20240822_i9/rsa_112_sha256',  './output/20240822_i9/rsa_128_sha256', './output/20240822_i9/rsa_192_sha256', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/rsa_80_sha256',    './output/20240822_i7/rsa_112_sha256',  './output/20240822_i7/rsa_128_sha256', './output/20240822_i7/rsa_192_sha256', './output/20240822_i7/rsa_256_sha256'], 'deprecated/TM_SG_rsa_sha256.png', 'RSA Versions with SHA-256'],
    # WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/dilithium5_sha512_avx2'], 'deprecated/TM_SG_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
    [['./output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/falcon5_avx2_sha512'], 'deprecated/TM_SG_falcon_sha512.png', 'Falcon Versions with SHA-512'],
    [['./output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/sphincs256_sha512_avx2'], 'deprecated/TM_SG_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
    [['./output/20240822_i9/rsa_80_sha512', './output/20240822_i9/rsa_112_sha512',  './output/20240822_i9/rsa_128_sha512', './output/20240822_i9/rsa_192_sha512', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/rsa_80_sha512', './output/20240822_i7/rsa_112_sha512',  './output/20240822_i7/rsa_128_sha512', './output/20240822_i7/rsa_192_sha512', './output/20240822_i7/rsa_256_sha512'], 'deprecated/TM_SG_rsa_sha512.png', 'RSA Versions with SHA-512'],
    # ONLY DILITHIUM 2,3,5
    [['./output/20240822_i9/dilithium2_avx2', './output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i7/dilithium2_avx2', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/dilithium2_sha512_avx2'], 'TM_SG_dilithium_2_All.png', 'Dilithium 2 Versions vs SHA'],
    [['./output/20240822_i9/dilithium3_avx2', './output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i7/dilithium3_avx2', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/dilithium3_sha512_avx2'], 'TM_SG_dilithium_3_All.png', 'Dilithium 3 Versions vs SHA'],
    [['./output/20240822_i9/dilithium5_avx2', './output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i7/dilithium5_avx2', './output/20240822_i7/dilithium5_sha256_avx2', './output/20240822_i7/dilithium5_sha512_avx2'], 'TM_SG_dilithium_5_All.png', 'Dilithium 5 Versions vs SHA'],
    # ONLY FALCON 512 and 1024
    [['./output/20240822_i9/falcon2_avx2', './output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i7/falcon2_avx2', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/falcon2_avx2_sha512'], 'TM_SG_falcon_2_All.png', 'Falcon 2 Versions vs SHA'],
    [['./output/20240822_i9/falcon5_avx2', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i7/falcon5_avx2', './output/20240822_i7/falcon5_avx2_sha256', './output/20240822_i7/falcon5_avx2_sha512'], 'TM_SG_falcon_5_All.png', 'Falcon 5 Versions vs SHA'],
    # ONLY SPHINCS+ 128,192,256
    [['./output/20240822_i9/sphincs128_avx2', './output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i7/sphincs128_avx2', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/sphincs128_sha512_avx2'], 'TM_SG_sphincs_128_All.png', 'SPHINCS+ 128 Versions vs SHA'],
    [['./output/20240822_i9/sphincs192_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i7/sphincs192_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/sphincs192_sha512_avx2'], 'TM_SG_sphincs_192_All.png', 'SPHINCS+ 192 Versions vs SHA'],
    [['./output/20240822_i9/sphincs256_avx2', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i7/sphincs256_avx2', './output/20240822_i7/sphincs256_sha256_avx2', './output/20240822_i7/sphincs256_sha512_avx2'], 'TM_SG_sphincs_256_All.png', 'SPHINCS+ 256 Versions vs SHA'],
    # DIFFERENT SECURITY LEVELS WITH NO SHA
    [['./output/20240822_i9/dilithium2_avx2', './output/20240822_i9/falcon2_avx2', './output/20240822_i9/sphincs128_avx2', './output/20240822_i7/dilithium2_avx2', './output/20240822_i7/falcon2_avx2', './output/20240822_i7/sphincs128_avx2'], 'TM_SG_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/20240822_i9/dilithium3_avx2', './output/20240822_i9/sphincs192_avx2', './output/20240822_i7/dilithium3_avx2', './output/20240822_i7/sphincs192_avx2'], 'TM_SG_192bit_security_level.png', 'Security Level 3'],
    [['./output/20240822_i9/dilithium5_avx2', './output/20240822_i9/falcon5_avx2', './output/20240822_i9/sphincs256_avx2', './output/20240822_i7/dilithium5_avx2', './output/20240822_i7/falcon5_avx2', './output/20240822_i7/sphincs256_avx2'], 'TM_SG_256bit_security_level.png', 'Security Level 5'],
    # DIFFERENT SECURITY LEVELS WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/rsa_128_sha256', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/rsa_128_sha256'], 'deprecated/TM_SG_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
    [['./output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/rsa_192_sha256', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/rsa_192_sha256'], 'deprecated/TM_SG_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
    [['./output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/dilithium5_sha256_avx2', './output/20240822_i7/falcon5_avx2_sha256', './output/20240822_i7/sphincs256_sha256_avx2', './output/20240822_i7/rsa_256_sha256'], 'deprecated/TM_SG_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
    # DIFFERENT SECURITY LEVELS WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/rsa_128_sha512', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/rsa_128_sha512'], 'deprecated/TM_SG_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
    [['./output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/rsa_192_sha512', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/rsa_192_sha512'], 'deprecated/TM_SG_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
    [['./output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/dilithium5_sha512_avx2', './output/20240822_i7/falcon5_avx2_sha512', './output/20240822_i7/sphincs256_sha512_avx2', './output/20240822_i7/rsa_256_sha512'], 'deprecated/TM_SG_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512'],
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Verify Time Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_verify_time_plot(df_all, './plot/comparison/Time_Verify/' + file_paths[1], file_paths[2])




### ============================================================
### === TEMPI DI VERIFICA TRA ALGORITMI con SHA - ISTOGRAMMI ===
### ============================================================

# Funzione per creare il grafico a barre con il tempo medio di firma
def create_sign_time_histogram_plot(df_all, output_file, title):
    plt.figure(figsize=(12,7))
    
    # Calcola il tempo medio di firma per ogni combinazione di algoritmo e versione
    avg_sign_times = df_all.groupby(['algorithm', 'device'])['verify_time'].mean().reset_index()
    
    # Crea il grafico a barre
    sns.barplot(x='algorithm', y='verify_time', hue='device', data=avg_sign_times, palette=plot_colors)
    
    plt.xlabel('Algorithm')
    plt.ylabel('Average Verify Time (seconds)')
    plt.title('Device Performance Comparison - Average Verify Time by Algorithm and Version - ' + title)
    plt.legend(title='Device')
    plt.grid(True)
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [ # WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/dilithium5_sha256_avx2'], 'TM_SG_H_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
    [['./output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/falcon5_avx2_sha256'], 'TM_SG_H_falcon_sha256.png', 'Falcon Versions with SHA-256'],
    [['./output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/sphincs256_sha256_avx2'], 'TM_SG_H_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
    [['./output/20240822_i9/rsa_80_sha256', './output/20240822_i9/rsa_112_sha256',  './output/20240822_i9/rsa_128_sha256', './output/20240822_i9/rsa_192_sha256', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/rsa_80_sha256',    './output/20240822_i7/rsa_112_sha256',  './output/20240822_i7/rsa_128_sha256', './output/20240822_i7/rsa_192_sha256', './output/20240822_i7/rsa_256_sha256'], 'deprecated/TM_SG_rsa_sha256.png', 'RSA Versions with SHA-256'],
    # WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/dilithium5_sha512_avx2'], 'TM_SG_H_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
    [['./output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/falcon5_avx2_sha512'], 'TM_SG_H_falcon_sha512.png', 'Falcon Versions with SHA-512'],
    [['./output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/sphincs256_sha512_avx2'], 'TM_SG_H_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
    [['./output/20240822_i9/rsa_80_sha512', './output/20240822_i9/rsa_112_sha512',  './output/20240822_i9/rsa_128_sha512', './output/20240822_i9/rsa_192_sha512', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/rsa_80_sha512', './output/20240822_i7/rsa_112_sha512',  './output/20240822_i7/rsa_128_sha512', './output/20240822_i7/rsa_192_sha512', './output/20240822_i7/rsa_256_sha512'], 'deprecated/TM_SG_rsa_sha512.png', 'RSA Versions with SHA-512'],
    # DIFFERENT SECURITY LEVELS WITH SHA-256
    [['./output/20240822_i9/dilithium2_sha256_avx2', './output/20240822_i9/falcon2_avx2_sha256', './output/20240822_i9/sphincs128_sha256_avx2', './output/20240822_i9/rsa_128_sha256', './output/20240822_i7/dilithium2_sha256_avx2', './output/20240822_i7/falcon2_avx2_sha256', './output/20240822_i7/sphincs128_sha256_avx2', './output/20240822_i7/rsa_128_sha256'], 'TM_SG_H_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
    [['./output/20240822_i9/dilithium3_sha256_avx2', './output/20240822_i9/sphincs192_sha256_avx2', './output/20240822_i9/rsa_192_sha256', './output/20240822_i7/dilithium3_sha256_avx2', './output/20240822_i7/sphincs192_sha256_avx2', './output/20240822_i7/rsa_192_sha256'], 'TM_SG_H_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
    [['./output/20240822_i9/dilithium5_sha256_avx2', './output/20240822_i9/falcon5_avx2_sha256', './output/20240822_i9/sphincs256_sha256_avx2', './output/20240822_i9/rsa_256_sha256', './output/20240822_i7/dilithium5_sha256_avx2', './output/20240822_i7/falcon5_avx2_sha256', './output/20240822_i7/sphincs256_sha256_avx2', './output/20240822_i7/rsa_256_sha256'], 'TM_SG_H_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
    # DIFFERENT SECURITY LEVELS WITH SHA-512
    [['./output/20240822_i9/dilithium2_sha512_avx2', './output/20240822_i9/falcon2_avx2_sha512', './output/20240822_i9/sphincs128_sha512_avx2', './output/20240822_i9/rsa_128_sha512', './output/20240822_i7/dilithium2_sha512_avx2', './output/20240822_i7/falcon2_avx2_sha512', './output/20240822_i7/sphincs128_sha512_avx2', './output/20240822_i7/rsa_128_sha512'], 'TM_SG_H_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
    [['./output/20240822_i9/dilithium3_sha512_avx2', './output/20240822_i9/sphincs192_sha512_avx2', './output/20240822_i9/rsa_192_sha512', './output/20240822_i7/dilithium3_sha512_avx2', './output/20240822_i7/sphincs192_sha512_avx2', './output/20240822_i7/rsa_192_sha512'], 'TM_SG_H_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
    [['./output/20240822_i9/dilithium5_sha512_avx2', './output/20240822_i9/falcon5_avx2_sha512', './output/20240822_i9/sphincs256_sha512_avx2', './output/20240822_i9/rsa_256_sha512', './output/20240822_i7/dilithium5_sha512_avx2', './output/20240822_i7/falcon5_avx2_sha512', './output/20240822_i7/sphincs256_sha512_avx2', './output/20240822_i7/rsa_256_sha512'], 'TM_SG_H_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512']
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Verify Time H-Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_sign_time_histogram_plot(df_all, './plot/comparison/Time_Verify/' + file_paths[1], file_paths[2])