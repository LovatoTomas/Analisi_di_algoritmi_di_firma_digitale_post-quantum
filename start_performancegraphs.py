# Autore: Tomas Lovato
# Data: 2024/07/13 18:00
# Analisi dei dati raccolti dagli algoritmi

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
        df['algorithm'] = file.split('/')[2]  # estrai il nome dell'algoritmo dal nome del file
        # Aggiungi colonna per distinguere tra REF e AVX2
        if 'avx2' in file:
            df['version'] = 'AVX2'
        else:
            df['version'] = 'REF'
    return pd.concat(dataframes, ignore_index=True)

# Dizionario per mappare i nomi degli algoritmi ai nuovi nomi
algorithm_name_mapping = {
    'dilithium2_ref': 'Dilithium 2',
    'dilithium3_ref': 'Dilithium 3',
    'dilithium5_ref': 'Dilithium 5',
    'dilithium2_avx2': 'Dilithium 2',
    'dilithium3_avx2': 'Dilithium 3',
    'dilithium5_avx2': 'Dilithium 5',
    'dilithium2_sha256_ref': 'Dilithium 2 SHA-256',
    'dilithium3_sha256_ref': 'Dilithium 3 SHA-256',
    'dilithium5_sha256_ref': 'Dilithium 5 SHA-256',
    'dilithium2_sha256_avx2': 'Dilithium 2 SHA-256',
    'dilithium3_sha256_avx2': 'Dilithium 3 SHA-256',
    'dilithium5_sha256_avx2': 'Dilithium 5 SHA-256',
    'dilithium2_sha512_ref': 'Dilithium 2 SHA-512',
    'dilithium3_sha512_ref': 'Dilithium 3 SHA-512',
    'dilithium5_sha512_ref': 'Dilithium 5 SHA-512',
    'dilithium2_sha512_avx2': 'Dilithium 2 SHA-512',
    'dilithium3_sha512_avx2': 'Dilithium 3 SHA-512',
    'dilithium5_sha512_avx2': 'Dilithium 5 SHA-512',
    'falcon2_ref': 'Falcon 512',
    'falcon5_ref': 'Falcon 1024',
    'falcon2_avx2': 'Falcon 512',
    'falcon5_avx2': 'Falcon 1024',
    'falcon2_ref_sha256': 'Falcon 2 SHA-256',
    'falcon5_ref_sha256': 'Falcon 5 SHA-256',
    'falcon2_avx2_sha256': 'Falcon 2 SHA-256',
    'falcon5_avx2_sha256': 'Falcon 5 SHA-256',
    'falcon2_ref_sha512': 'Falcon 2 SHA-512',
    'falcon5_ref_sha512': 'Falcon 5 SHA-512',
    'falcon2_avx2_sha512': 'Falcon 2 SHA-512',
    'falcon5_avx2_sha512': 'Falcon 5 SHA-512',
    'sphincs128_ref': 'SPHINCS+ 128',
    'sphincs192_ref': 'SPHINCS+ 192',
    'sphincs256_ref': 'SPHINCS+ 256',
    'sphincs128_avx2': 'SPHINCS+ 128',
    'sphincs192_avx2': 'SPHINCS+ 192',
    'sphincs256_avx2': 'SPHINCS+ 256',
    'sphincs128_sha256_ref': 'SPHINCS+ 128 SHA-256',
    'sphincs192_sha256_ref': 'SPHINCS+ 192 SHA-256',
    'sphincs256_sha256_ref': 'SPHINCS+ 256 SHA-256',
    'sphincs128_sha256_avx2': 'SPHINCS+ 128 SHA-256',
    'sphincs192_sha256_avx2': 'SPHINCS+ 192 SHA-256',
    'sphincs256_sha256_avx2': 'SPHINCS+ 256 SHA-256',
    'sphincs128_sha512_ref': 'SPHINCS+ 128 SHA-512',
    'sphincs192_sha512_ref': 'SPHINCS+ 192 SHA-512',
    'sphincs256_sha512_ref': 'SPHINCS+ 256 SHA-512',
    'sphincs128_sha512_avx2': 'SPHINCS+ 128 SHA-512',
    'sphincs192_sha512_avx2': 'SPHINCS+ 192 SHA-512',
    'sphincs256_sha512_avx2': 'SPHINCS+ 256 SHA-512',
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
    'Private Key Size': '#0a8270',
    'Public Key Size': '#321c6a',
    'REF': '#9b0014',
    'AVX2': '#1b8dc1'
}

### ================================================
### ====== CONFRONTO TRA DIMENSIONI DI CHIAVI ======
### ================================================

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [
    [['./output/dilithium2_ref', './output/dilithium3_ref', './output/dilithium5_ref'], 'KC_dilithium.png', 'Dilithium Versions'],
    [['./output/falcon2_ref', './output/falcon5_ref'], 'KC_falcon.png', 'Falcon Versions'],
    [['./output/sphincs128_ref', './output/sphincs192_ref', './output/sphincs256_ref'], 'KC_sphincs.png', 'Sphincs+ Versions'],
    [['./output/rsa_128_sha256', './output/rsa_192_sha256', './output/rsa_256_sha256'], 'KC_rsa.png', 'RSA Versions'],
    [['./output/dilithium2_ref', './output/falcon2_ref', './output/sphincs128_ref', './output/rsa_128_sha256'], 'KC_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/dilithium3_ref', './output/sphincs192_ref', './output/rsa_192_sha256'], 'KC_192bit_security_level.png', 'Security Level 3'],
    [['./output/dilithium5_ref', './output/falcon5_ref', './output/sphincs256_ref', './output/rsa_256_sha256'], 'KC_256bit_security_level.png', 'Security Level 5'],
    [['./output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2', './liboqs_double_check/risultati_Dilithium2_avx2', './liboqs_double_check/risultati_Dilithium3_avx2', './liboqs_double_check/risultati_Dilithium5_avx2'], 'double_check/KC_dilithium.png', 'Dilithium Version - Double Check'],
    [['./output/falcon2_avx2', './output/falcon5_avx2', './liboqs_double_check/risultati_Falcon-512_avx2', './liboqs_double_check/risultati_Falcon-1024_avx2'], 'double_check/KC_falcon.png', 'Falcon Version - Double Check'],
    [['./output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-128f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-192f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-256f-simple_avx2'], 'double_check/KC_sphincs.png', 'Sphincs+ Version - Double Check']
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Key Sizes Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Calcola le dimensioni medie delle chiavi pubbliche e private per ogni algoritmo
        avg_key_sizes = df_all.groupby('algorithm')[['pub_key_size', 'priv_key_size']].mean().reset_index()
        # Trasformazione dei dati per il grafico a barre
        avg_key_sizes = pd.melt(avg_key_sizes, id_vars=['algorithm'], value_vars=['pub_key_size', 'priv_key_size'],
                                var_name='Key Type', value_name='Key Size')
        # Aggiornamento dei nomi dei tipi di chiave per la legenda
        avg_key_sizes['Key Type'] = avg_key_sizes['Key Type'].replace({
            'pub_key_size': 'Public Key Size',
            'priv_key_size': 'Private Key Size'
        })
        # Creazione del grafico a barre
        plt.figure(figsize=(16, 5))
        sns.barplot(x='algorithm', y='Key Size', hue='Key Type', data=avg_key_sizes, palette=plot_colors)
        plt.xlabel('Algorithm')
        plt.ylabel('Key Size (bytes)')
        plt.title('Key Sizes per Algorithm - ' + file_paths[2])
        plt.legend(title='Key Type', loc='upper right')
        plt.grid(True)
        # Imposta i tick dell'asse Y con intervalli di 256 o 512
        if int(avg_key_sizes['Key Size'].max()) < 256:
            plt.yticks(range(0, int(avg_key_sizes['Key Size'].max()) + 128, 64))  # Intervalli di 64
        elif int(avg_key_sizes['Key Size'].max()) < 4096:
            plt.yticks(range(0, int(avg_key_sizes['Key Size'].max()) + 512, 256))  # Intervalli di 256
        else:   
            plt.yticks(range(0, int(avg_key_sizes['Key Size'].max()) + 512, 512))  # Intervalli di 512
        save_or_show_plot('./plot/Key_Sizes/' + file_paths[1])
        plt.close()
        # Aggiorna la progress bar
        pbar.update(1)




### ================================================
### ========= DIMENSIONI DI INPUT E OUTPUT =========
### ================================================

algorithm_colors = {
    'Dilithium 2': '#ffcc99',
    'Dilithium 3': '#ff9966',
    'Dilithium 5': '#ff6600',
    'Falcon 512': '#66b2ff',
    'Falcon 1024': '#3399ff',
    'SPHINCS+ 128': '#ffb3b3',
    'SPHINCS+ 192': '#ff6666',
    'SPHINCS+ 256': '#ff1a1a',
    'RSA 3072': '#ff3df3',
    'RSA 7680': '#e43af2',
    'RSA 15360': '#c031cc',
    'Dilithium 2 LIBOQS': '#7a3eff',
    'Dilithium 3 LIBOQS': '#5c2fbf',
    'Dilithium 5 LIBOQS': '#4a2699',
    'Falcon 512 LIBOQS': '#99ffcc',
    'Falcon 1024 LIBOQS': '#66ff99',
    'SPHINCS+ 128 LIBOQS': '#ccccff',
    'SPHINCS+ 192 LIBOQS': '#9999ff',
    'SPHINCS+ 256 LIBOQS': '#6666ff'
}

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [
    [['./output/dilithium2_ref', './output/dilithium3_ref', './output/dilithium5_ref'], 'IO_dilithium.png', 'Dilithium Versions'],
    [['./output/falcon2_ref', './output/falcon5_ref'], 'KC_falcon.png', 'Falcon Versions'],
    [['./output/sphincs128_ref', './output/sphincs192_ref', './output/sphincs256_ref'], 'IO_sphincs.png', 'Sphincs+ Versions'],
    [['./output/rsa_128_sha256', './output/rsa_192_sha256', './output/rsa_256_sha256'], 'IO_rsa.png', 'RSA Versions'],
    [['./output/dilithium2_ref', './output/falcon2_ref', './output/sphincs128_ref', './output/rsa_128_sha256'], 'IO_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/dilithium3_ref', './output/sphincs192_ref', './output/rsa_192_sha256'], 'IO_192bit_security_level.png', 'Security Level 3'],
    [['./output/dilithium5_ref', './output/falcon5_ref', './output/sphincs256_ref', './output/rsa_256_sha256'], 'IO_256bit_security_level.png', 'Security Level 5'],
    [['./output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2', './liboqs_double_check/risultati_Dilithium2_avx2', './liboqs_double_check/risultati_Dilithium3_avx2', './liboqs_double_check/risultati_Dilithium5_avx2'], 'double_check/IO_dilithium.png', 'Dilithium Version - Double Check'],
    [['./output/falcon2_avx2', './output/falcon5_avx2', './liboqs_double_check/risultati_Falcon-512_avx2', './liboqs_double_check/risultati_Falcon-1024_avx2'], 'double_check/IO_falcon.png', 'Falcon Version - Double Check'],
    [['./output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-128f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-192f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-256f-simple_avx2'], 'double_check/IO_sphincs.png', 'Sphincs+ Version - Double Check']
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Signature Size Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico a barre
        plt.figure(figsize=(16,10))
        
        # Grafico a istogrammi per le dimensioni delle firme
        sns.barplot(x='algorithm', y='signature_size', hue="algorithm", data=df_all, palette=algorithm_colors)
        
        plt.xlabel('Algorithms and Versions')
        plt.ylabel('Signature Size (bytes)')
        plt.title('Comparison of Signature Sizes - ' + file_paths[2])
        plt.yscale('linear')
        plt.grid(True)
        
        save_or_show_plot('./plot/Message_IO/' + file_paths[1])
        plt.close()
        # Aggiorna la progress bar
        pbar.update(1)




### ================================================
### ======== TEMPI DI KEYGEN TRA ALGORITMI =========
### ================================================

# Funzione per creare il grafico con la media dei tempi di keygen
def create_keygen_time_histogram(df_all, output_file, title):
    plt.figure(figsize=(12,7))

    # Calcola la media dei tempi di keygen per ogni algoritmo e versione
    df_mean_keygen_time = df_all.groupby(['algorithm', 'version'])['keygen_time'].mean().reset_index()
    
    # Crea un grafico a barre
    sns.barplot(x='algorithm', y='keygen_time', hue='version', data=df_mean_keygen_time, palette=plot_colors)

    plt.xlabel('Algorithms and Versions')
    plt.ylabel('Average Keygen Time (seconds)')
    plt.title('Average Keygen Time - ' + title)
    plt.yscale('log')
    plt.grid(True)
    
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [
    [['./output/dilithium2_ref', './output/dilithium3_ref', './output/dilithium5_ref', './output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2'], 'TM_KG_dilithium.png', 'Dilithium Versions'],
    [['./output/falcon2_ref', './output/falcon5_ref', './output/falcon2_avx2', './output/falcon5_avx2'], 'TM_KG_falcon.png', 'Falcon Versions'],
    [['./output/sphincs128_ref', './output/sphincs192_ref', './output/sphincs256_ref', './output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2'], 'TM_KG_sphincs.png', 'Sphincs+ Versions'],
    [['./output/rsa_128_sha256', './output/rsa_192_sha256', './output/rsa_256_sha256'], 'TM_KG_rsa.png', 'RSA Versions'],
    [['./output/dilithium2_ref', './output/falcon2_ref', './output/sphincs128_ref', './output/dilithium2_avx2', './output/falcon2_avx2', './output/sphincs128_avx2', './output/rsa_128_sha256'], 'TM_KG_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/dilithium3_ref', './output/sphincs192_ref', './output/dilithium3_avx2', './output/sphincs192_avx2', './output/rsa_192_sha256'], 'TM_KG_192bit_security_level.png', 'Security Level 3'],
    [['./output/dilithium5_ref', './output/falcon5_ref', './output/sphincs256_ref', './output/dilithium5_avx2', './output/falcon5_avx2', './output/sphincs256_avx2', './output/rsa_256_sha256'], 'TM_KG_256bit_security_level.png', 'Security Level 5'],
    [['./output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2', './liboqs_double_check/risultati_Dilithium2_avx2', './liboqs_double_check/risultati_Dilithium3_avx2', './liboqs_double_check/risultati_Dilithium5_avx2'], 'double_check/TM_KG_dilithium.png', 'Dilithium Version - Double Check'],
    [['./output/falcon2_avx2', './output/falcon5_avx2', './liboqs_double_check/risultati_Falcon-512_avx2', './liboqs_double_check/risultati_Falcon-1024_avx2'], 'double_check/TM_KG_falcon.png', 'Falcon Version - Double Check'],
    [['./output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-128f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-192f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-256f-simple_avx2'], 'double_check/TM_KG_sphincs.png', 'Sphincs+ Version - Double Check']
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating KeyGen Time Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con la media dei tempi di keygen
        create_keygen_time_histogram(df_all, './plot/Time_Keygen/' + file_paths[1], file_paths[2])





# Dizionario per mappare i nomi degli algoritmi ai nuovi nomi
algorithm_name_mapping = {
    'dilithium2_ref': 'Dilithium 2',
    'dilithium3_ref': 'Dilithium 3',
    'dilithium5_ref': 'Dilithium 5',
    'dilithium2_avx2': 'Dilithium 2',
    'dilithium3_avx2': 'Dilithium 3',
    'dilithium5_avx2': 'Dilithium 5',
    'dilithium2_sha256_ref': 'Dilithium 2 SHA-256',
    'dilithium3_sha256_ref': 'Dilithium 3 SHA-256',
    'dilithium5_sha256_ref': 'Dilithium 5 SHA-256',
    'dilithium2_sha256_avx2': 'Dilithium 2 SHA-256',
    'dilithium3_sha256_avx2': 'Dilithium 3 SHA-256',
    'dilithium5_sha256_avx2': 'Dilithium 5 SHA-256',
    'dilithium2_sha512_ref': 'Dilithium 2 SHA-512',
    'dilithium3_sha512_ref': 'Dilithium 3 SHA-512',
    'dilithium5_sha512_ref': 'Dilithium 5 SHA-512',
    'dilithium2_sha512_avx2': 'Dilithium 2 SHA-512',
    'dilithium3_sha512_avx2': 'Dilithium 3 SHA-512',
    'dilithium5_sha512_avx2': 'Dilithium 5 SHA-512',
    'falcon2_ref': 'Falcon 512',
    'falcon5_ref': 'Falcon 1024',
    'falcon2_avx2': 'Falcon 512',
    'falcon5_avx2': 'Falcon 1024',
    'falcon2_ref_sha256': 'Falcon 2 SHA-256',
    'falcon5_ref_sha256': 'Falcon 5 SHA-256',
    'falcon2_avx2_sha256': 'Falcon 2 SHA-256',
    'falcon5_avx2_sha256': 'Falcon 5 SHA-256',
    'falcon2_ref_sha512': 'Falcon 2 SHA-512',
    'falcon5_ref_sha512': 'Falcon 5 SHA-512',
    'falcon2_avx2_sha512': 'Falcon 2 SHA-512',
    'falcon5_avx2_sha512': 'Falcon 5 SHA-512',
    'sphincs128_ref': 'SPHINCS+ 128',
    'sphincs192_ref': 'SPHINCS+ 192',
    'sphincs256_ref': 'SPHINCS+ 256',
    'sphincs128_avx2': 'SPHINCS+ 128',
    'sphincs192_avx2': 'SPHINCS+ 192',
    'sphincs256_avx2': 'SPHINCS+ 256',
    'sphincs128_sha256_ref': 'SPHINCS+ 128 SHA-256',
    'sphincs192_sha256_ref': 'SPHINCS+ 192 SHA-256',
    'sphincs256_sha256_ref': 'SPHINCS+ 256 SHA-256',
    'sphincs128_sha256_avx2': 'SPHINCS+ 128 SHA-256',
    'sphincs192_sha256_avx2': 'SPHINCS+ 192 SHA-256',
    'sphincs256_sha256_avx2': 'SPHINCS+ 256 SHA-256',
    'sphincs128_sha512_ref': 'SPHINCS+ 128 SHA-512',
    'sphincs192_sha512_ref': 'SPHINCS+ 192 SHA-512',
    'sphincs256_sha512_ref': 'SPHINCS+ 256 SHA-512',
    'sphincs128_sha512_avx2': 'SPHINCS+ 128 SHA-512',
    'sphincs192_sha512_avx2': 'SPHINCS+ 192 SHA-512',
    'sphincs256_sha512_avx2': 'SPHINCS+ 256 SHA-512',
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
    markers = {'REF': 'o', 'AVX2': 'X'}
    
    # Disegna le linee
    for algorithm in df_all['algorithm'].unique():
        for version in ['REF', 'AVX2']:
            subset = df_all[(df_all['algorithm'] == algorithm) & (df_all['version'] == version)]
            if not subset.empty:
                sns.lineplot(x='msg_len', y='sign_time', data=subset, marker=markers[version], color=color_mapping[algorithm], label=f'{algorithm} {version}')
    
    plt.xlabel('Message Length (bytes)')
    plt.ylabel('Sign Time (seconds)')
    plt.title('Sign Time vs Message Length - ' + title)
    plt.legend(title='Algorithm and Version')
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [# NORMAL VERSIONS
    [['./output/dilithium2_ref', './output/dilithium3_ref', './output/dilithium5_ref', './output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2'], 'TM_SG_dilithium.png', 'Dilithium Versions'],
    [['./output/falcon2_ref', './output/falcon5_ref', './output/falcon2_avx2', './output/falcon5_avx2'], 'TM_SG_falcon.png', 'Falcon Versions'],
    [['./output/sphincs128_ref', './output/sphincs192_ref', './output/sphincs256_ref', './output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2'], 'TM_SG_sphincs.png', 'Sphincs+ Versions'],
    [['./output/rsa_128_sha256', './output/rsa_128_sha512', './output/rsa_192_sha256', './output/rsa_192_sha512', './output/rsa_256_sha256', './output/rsa_256_sha512'], 'TM_SG_rsa.png', 'RSA Versions'],
    # WITH SHA-256
    [['./output/dilithium2_sha256_ref', './output/dilithium3_sha256_ref', './output/dilithium5_sha256_ref', './output/dilithium2_sha256_avx2', './output/dilithium3_sha256_avx2', './output/dilithium5_sha256_avx2'], 'deprecated/TM_SG_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
    [['./output/falcon2_ref_sha256', './output/falcon5_ref_sha256', './output/falcon2_avx2_sha256', './output/falcon5_avx2_sha256'], 'deprecated/TM_SG_falcon_sha256.png', 'Falcon Versions with SHA-256'],
    [['./output/sphincs128_sha256_ref', './output/sphincs192_sha256_ref', './output/sphincs256_sha256_ref', './output/sphincs128_sha256_avx2', './output/sphincs192_sha256_avx2', './output/sphincs256_sha256_avx2'], 'deprecated/TM_SG_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
    [['./output/rsa_128_sha256', './output/rsa_192_sha256', './output/rsa_256_sha256'], 'deprecated/TM_SG_rsa_sha256.png', 'RSA Versions with SHA-256'],
    # WITH SHA-512
    [['./output/dilithium2_sha512_ref', './output/dilithium3_sha512_ref', './output/dilithium5_sha512_ref', './output/dilithium2_sha512_avx2', './output/dilithium3_sha512_avx2', './output/dilithium5_sha512_avx2'], 'deprecated/TM_SG_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
    [['./output/falcon2_ref_sha512', './output/falcon5_ref_sha512', './output/falcon2_avx2_sha512', './output/falcon5_avx2_sha512'], 'deprecated/TM_SG_falcon_sha512.png', 'Falcon Versions with SHA-512'],
    [['./output/sphincs128_sha512_ref', './output/sphincs192_sha512_ref', './output/sphincs256_sha512_ref', './output/sphincs128_sha512_avx2', './output/sphincs192_sha512_avx2', './output/sphincs256_sha512_avx2'], 'deprecated/TM_SG_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
    [['./output/rsa_128_sha512', './output/rsa_192_sha512', './output/rsa_256_sha512'], 'deprecated/TM_SG_rsa_sha512.png', 'RSA Versions with SHA-512'],
    # ONLY DILITHIUM 2,3,5
    [['./output/dilithium2_ref', './output/dilithium2_sha256_ref', './output/dilithium2_sha512_ref', './output/dilithium2_avx2', './output/dilithium2_sha256_avx2', './output/dilithium2_sha512_avx2'], 'TM_SG_dilithium_2_All.png', 'Dilithium 2 Versions vs SHA'],
    [['./output/dilithium3_ref', './output/dilithium3_sha256_ref', './output/dilithium3_sha512_ref', './output/dilithium3_avx2', './output/dilithium3_sha256_avx2', './output/dilithium3_sha512_avx2'], 'TM_SG_dilithium_3_All.png', 'Dilithium 3 Versions vs SHA'],
    [['./output/dilithium5_ref', './output/dilithium5_sha256_ref', './output/dilithium5_sha512_ref', './output/dilithium5_avx2', './output/dilithium5_sha256_avx2', './output/dilithium5_sha512_avx2'], 'TM_SG_dilithium_5_All.png', 'Dilithium 5 Versions vs SHA'],
    # ONLY FALCON 512 and 1024
    [['./output/falcon2_ref', './output/falcon2_ref_sha256', './output/falcon2_ref_sha512', './output/falcon2_avx2', './output/falcon2_avx2_sha256', './output/falcon2_avx2_sha512'], 'TM_SG_falcon_2_All.png', 'Falcon 2 Versions vs SHA'],
    [['./output/falcon5_ref', './output/falcon5_ref_sha256', './output/falcon5_ref_sha512', './output/falcon5_avx2', './output/falcon5_avx2_sha256', './output/falcon5_avx2_sha512'], 'TM_SG_falcon_5_All.png', 'Falcon 5 Versions vs SHA'],
    # ONLY SPHINCS+ 128,192,256
    [['./output/sphincs128_ref', './output/sphincs128_sha256_ref', './output/sphincs128_sha512_ref', './output/sphincs128_avx2', './output/sphincs128_sha256_avx2', './output/sphincs128_sha512_avx2'], 'TM_SG_sphincs_128_All.png', 'SPHINCS+ 128 Versions vs SHA'],
    [['./output/sphincs192_ref', './output/sphincs192_sha256_ref', './output/sphincs192_sha512_ref', './output/sphincs192_avx2', './output/sphincs192_sha256_avx2', './output/sphincs192_sha512_avx2'], 'TM_SG_sphincs_192_All.png', 'SPHINCS+ 192 Versions vs SHA'],
    [['./output/sphincs256_ref', './output/sphincs256_sha256_ref', './output/sphincs256_sha512_ref', './output/sphincs256_avx2', './output/sphincs256_sha256_avx2', './output/sphincs256_sha512_avx2'], 'TM_SG_sphincs_256_All.png', 'SPHINCS+ 256 Versions vs SHA'],
    # DIFFERENT SECURITY LEVELS WITH NO SHA
    [['./output/dilithium2_ref', './output/falcon2_ref', './output/sphincs128_ref', './output/dilithium2_avx2', './output/falcon2_avx2', './output/sphincs128_avx2'], 'TM_SG_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/dilithium3_ref', './output/sphincs192_ref', './output/dilithium3_avx2', './output/sphincs192_avx2'], 'TM_SG_192bit_security_level.png', 'Security Level 3'],
    [['./output/dilithium5_ref', './output/falcon5_ref', './output/sphincs256_ref', './output/dilithium5_avx2', './output/falcon5_avx2', './output/sphincs256_avx2'], 'TM_SG_256bit_security_level.png', 'Security Level 5'],
    # DIFFERENT SECURITY LEVELS WITH SHA-256
    [['./output/dilithium2_sha256_ref', './output/falcon2_ref_sha256', './output/sphincs128_sha256_ref', './output/dilithium2_sha256_avx2', './output/falcon2_avx2_sha256', './output/sphincs128_sha256_avx2', './output/rsa_128_sha256'], 'deprecated/TM_SG_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
    [['./output/dilithium3_sha256_ref', './output/sphincs192_sha256_ref', './output/dilithium3_sha256_avx2', './output/sphincs192_sha256_avx2', './output/rsa_192_sha256'], 'deprecated/TM_SG_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
    [['./output/dilithium5_sha256_ref', './output/falcon5_ref_sha256', './output/sphincs256_sha256_ref', './output/dilithium5_sha256_avx2', './output/falcon5_avx2_sha256', './output/sphincs256_sha256_avx2', './output/rsa_256_sha256'], 'deprecated/TM_SG_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
    # DIFFERENT SECURITY LEVELS WITH SHA-512
    [['./output/dilithium2_sha512_ref', './output/falcon2_ref_sha512', './output/sphincs128_sha512_ref', './output/dilithium2_sha512_avx2', './output/falcon2_avx2_sha512', './output/sphincs128_sha512_avx2', './output/rsa_128_sha512'], 'deprecated/TM_SG_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
    [['./output/dilithium3_sha512_ref', './output/sphincs192_sha512_ref', './output/dilithium3_sha512_avx2', './output/sphincs192_sha512_avx2', './output/rsa_192_sha512'], 'deprecated/TM_SG_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
    [['./output/dilithium5_sha512_ref', './output/falcon5_ref_sha512', './output/sphincs256_sha512_ref', './output/dilithium5_sha512_avx2', './output/falcon5_avx2_sha512', './output/sphincs256_sha512_avx2', './output/rsa_256_sha512'], 'deprecated/TM_SG_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512'],
    # DOUBLE CHECK
    [['./output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2', './liboqs_double_check/risultati_Dilithium2_avx2', './liboqs_double_check/risultati_Dilithium3_avx2', './liboqs_double_check/risultati_Dilithium5_avx2'], 'double_check/TM_SG_dilithium.png', 'Dilithium Version - Double Check'],
    [['./output/falcon2_avx2', './output/falcon5_avx2', './liboqs_double_check/risultati_Falcon-512_avx2', './liboqs_double_check/risultati_Falcon-1024_avx2'], 'double_check/TM_SG_falcon.png', 'Falcon Version - Double Check'],
    [['./output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-128f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-192f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-256f-simple_avx2'], 'double_check/TM_SG_sphincs.png', 'Sphincs+ Version - Double Check']
]


# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Sign Time Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_sign_time_plot(df_all, './plot/Time_Sign/' + file_paths[1], file_paths[2])




### =========================================================
### === TEMPI DI FIRMA TRA ALGORITMI con SHA - ISTOGRAMMI ===
### =========================================================

# Funzione per creare il grafico a barre con il tempo medio di firma
def create_sign_time_histogram_plot(df_all, output_file, title):
    plt.figure(figsize=(12,7))
    
    # Calcola il tempo medio di firma per ogni combinazione di algoritmo e versione
    avg_sign_times = df_all.groupby(['algorithm', 'version'])['sign_time'].mean().reset_index()
    
    # Crea il grafico a barre
    sns.barplot(x='algorithm', y='sign_time', hue='version', data=avg_sign_times, palette=plot_colors)
    
    plt.xlabel('Algorithm')
    plt.ylabel('Average Sign Time (seconds)')
    plt.title('Average Sign Time by Algorithm and Version - ' + title)
    plt.legend(title='Version')
    plt.grid(True)
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [ # WITH SHA-256
            [['./output/dilithium2_sha256_ref', './output/dilithium3_sha256_ref', './output/dilithium5_sha256_ref', './output/dilithium2_sha256_avx2', './output/dilithium3_sha256_avx2', './output/dilithium5_sha256_avx2'], 'TM_SG_H_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
            [['./output/falcon2_ref_sha256', './output/falcon5_ref_sha256', './output/falcon2_avx2_sha256', './output/falcon5_avx2_sha256'], 'TM_SG_H_falcon_sha256.png', 'Falcon Versions with SHA-256'],
            [['./output/sphincs128_sha256_ref', './output/sphincs192_sha256_ref', './output/sphincs256_sha256_ref', './output/sphincs128_sha256_avx2', './output/sphincs192_sha256_avx2', './output/sphincs256_sha256_avx2'], 'TM_SG_H_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
            [['./output/rsa_128_sha256', './output/rsa_192_sha256', './output/rsa_256_sha256'], 'TM_SG_H_rsa_sha256.png', 'RSA Versions with SHA-256'],
            # WITH SHA-512
            [['./output/dilithium2_sha512_ref', './output/dilithium3_sha512_ref', './output/dilithium5_sha512_ref', './output/dilithium2_sha512_avx2', './output/dilithium3_sha512_avx2', './output/dilithium5_sha512_avx2'], 'TM_SG_H_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
            [['./output/falcon2_ref_sha512', './output/falcon5_ref_sha512', './output/falcon2_avx2_sha512', './output/falcon5_avx2_sha512'], 'TM_SG_H_falcon_sha512.png', 'Falcon Versions with SHA-512'],
            [['./output/sphincs128_sha512_ref', './output/sphincs192_sha512_ref', './output/sphincs256_sha512_ref', './output/sphincs128_sha512_avx2', './output/sphincs192_sha512_avx2', './output/sphincs256_sha512_avx2'], 'TM_SG_H_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
            [['./output/rsa_128_sha512', './output/rsa_192_sha512', './output/rsa_256_sha512'], 'TM_SG_H_rsa_sha512.png', 'RSA Versions with SHA-512'],
            # DIFFERENT SECURITY LEVELS WITH SHA-256
            [['./output/dilithium2_sha256_ref', './output/falcon2_ref_sha256', './output/sphincs128_sha256_ref', './output/dilithium2_sha256_avx2', './output/falcon2_avx2_sha256', './output/sphincs128_sha256_avx2', './output/rsa_128_sha256'], 'TM_SG_H_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
            [['./output/dilithium3_sha256_ref', './output/sphincs192_sha256_ref', './output/dilithium3_sha256_avx2', './output/sphincs192_sha256_avx2', './output/rsa_192_sha256'], 'TM_SG_H_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
            [['./output/dilithium5_sha256_ref', './output/falcon5_ref_sha256', './output/sphincs256_sha256_ref', './output/dilithium5_sha256_avx2', './output/falcon5_avx2_sha256', './output/sphincs256_sha256_avx2', './output/rsa_256_sha256'], 'TM_SG_H_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
            # DIFFERENT SECURITY LEVELS WITH SHA-512
            [['./output/dilithium2_sha512_ref', './output/falcon2_ref_sha512', './output/sphincs128_sha512_ref', './output/dilithium2_sha512_avx2', './output/falcon2_avx2_sha512', './output/sphincs128_sha512_avx2', './output/rsa_128_sha512'], 'TM_SG_H_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
            [['./output/dilithium3_sha512_ref', './output/sphincs192_sha512_ref', './output/dilithium3_sha512_avx2', './output/sphincs192_sha512_avx2', './output/rsa_192_sha512'], 'TM_SG_H_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
            [['./output/dilithium5_sha512_ref', './output/falcon5_ref_sha512', './output/sphincs256_sha512_ref', './output/dilithium5_sha512_avx2', './output/falcon5_avx2_sha512', './output/sphincs256_sha512_avx2', './output/rsa_256_sha512'], 'TM_SG_H_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512']
            ]


# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Sign Time H-Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_sign_time_histogram_plot(df_all, './plot/Time_Sign/' + file_paths[1], file_paths[2])


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
    markers = {'REF': 'o', 'AVX2': 'X'}
    
    # Disegna le linee
    for algorithm in df_all['algorithm'].unique():
        for version in ['REF', 'AVX2']:
            subset = df_all[(df_all['algorithm'] == algorithm) & (df_all['version'] == version)]
            if not subset.empty:
                sns.lineplot(x='msg_len', y='verify_time', data=subset, marker=markers[version], color=color_mapping[algorithm], label=f'{algorithm} {version}')
    
    plt.xlabel('Message Length (bytes)')
    plt.ylabel('Verify Time (seconds)')
    plt.title('Verify Time vs Message Length - ' + title)
    plt.legend(title='Algorithm and Version')
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [# NORMAL VERSIONS
    [['./output/dilithium2_ref', './output/dilithium3_ref', './output/dilithium5_ref', './output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2'], 'TM_VF_dilithium.png', 'Dilithium Versions'],
    [['./output/falcon2_ref', './output/falcon5_ref', './output/falcon2_avx2', './output/falcon5_avx2'], 'TM_VF_falcon.png', 'Falcon Versions'],
    [['./output/sphincs128_ref', './output/sphincs192_ref', './output/sphincs256_ref', './output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2'], 'TM_VF_sphincs.png', 'Sphincs+ Versions'],
    [['./output/rsa_128_sha256', './output/rsa_128_sha512', './output/rsa_192_sha256', './output/rsa_192_sha512', './output/rsa_256_sha256', './output/rsa_256_sha512'], 'TM_VF_rsa.png', 'RSA Versions'],
    # WITH SHA-256
    [['./output/dilithium2_sha256_ref', './output/dilithium3_sha256_ref', './output/dilithium5_sha256_ref', './output/dilithium2_sha256_avx2', './output/dilithium3_sha256_avx2', './output/dilithium5_sha256_avx2'], 'deprecated/TM_VF_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
    [['./output/falcon2_ref_sha256', './output/falcon5_ref_sha256', './output/falcon2_avx2_sha256', './output/falcon5_avx2_sha256'], 'deprecated/TM_VF_falcon_sha256.png', 'Falcon Versions with SHA-256'],
    [['./output/sphincs128_sha256_ref', './output/sphincs192_sha256_ref', './output/sphincs256_sha256_ref', './output/sphincs128_sha256_avx2', './output/sphincs192_sha256_avx2', './output/sphincs256_sha256_avx2'], 'deprecated/TM_VF_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
    [['./output/rsa_128_sha256', './output/rsa_192_sha256', './output/rsa_256_sha256'], 'deprecated/TM_VF_rsa_sha256.png', 'RSA Versions with SHA-256'],
    # WITH SHA-512
    [['./output/dilithium2_sha512_ref', './output/dilithium3_sha512_ref', './output/dilithium5_sha512_ref', './output/dilithium2_sha512_avx2', './output/dilithium3_sha512_avx2', './output/dilithium5_sha512_avx2'], 'deprecated/TM_VF_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
    [['./output/falcon2_ref_sha512', './output/falcon5_ref_sha512', './output/falcon2_avx2_sha512', './output/falcon5_avx2_sha512'], 'deprecated/TM_VF_falcon_sha512.png', 'Falcon Versions with SHA-512'],
    [['./output/sphincs128_sha512_ref', './output/sphincs192_sha512_ref', './output/sphincs256_sha512_ref', './output/sphincs128_sha512_avx2', './output/sphincs192_sha512_avx2', './output/sphincs256_sha512_avx2'], 'deprecated/TM_VF_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
    [['./output/rsa_128_sha512', './output/rsa_192_sha512', './output/rsa_256_sha512'], 'deprecated/TM_VF_rsa_sha512.png', 'RSA Versions with SHA-512'],
    # ONLY DILITHIUM 2,3,5
    [['./output/dilithium2_ref', './output/dilithium2_sha256_ref', './output/dilithium2_sha512_ref', './output/dilithium2_avx2', './output/dilithium2_sha256_avx2', './output/dilithium2_sha512_avx2'], 'TM_VF_dilithium_2_All.png', 'Dilithium 2 Versions vs SHA'],
    [['./output/dilithium3_ref', './output/dilithium3_sha256_ref', './output/dilithium3_sha512_ref', './output/dilithium3_avx2', './output/dilithium3_sha256_avx2', './output/dilithium3_sha512_avx2'], 'TM_VF_dilithium_3_All.png', 'Dilithium 3 Versions vs SHA'],
    [['./output/dilithium5_ref', './output/dilithium5_sha256_ref', './output/dilithium5_sha512_ref', './output/dilithium5_avx2', './output/dilithium5_sha256_avx2', './output/dilithium5_sha512_avx2'], 'TM_VF_dilithium_5_All.png', 'Dilithium 5 Versions vs SHA'],
    # ONLY FALCON 512 and 1024
    [['./output/falcon2_ref', './output/falcon2_ref_sha256', './output/falcon2_ref_sha512', './output/falcon2_avx2', './output/falcon2_avx2_sha256', './output/falcon2_avx2_sha512'], 'TM_VF_falcon_2_All.png', 'Falcon 2 Versions vs SHA'],
    [['./output/falcon5_ref', './output/falcon5_ref_sha256', './output/falcon5_ref_sha512', './output/falcon5_avx2', './output/falcon5_avx2_sha256', './output/falcon5_avx2_sha512'], 'TM_VF_falcon_5_All.png', 'Falcon 5 Versions vs SHA'],
    # ONLY SPHINCS+ 128,192,256
    [['./output/sphincs128_ref', './output/sphincs128_sha256_ref', './output/sphincs128_sha512_ref', './output/sphincs128_avx2', './output/sphincs128_sha256_avx2', './output/sphincs128_sha512_avx2'], 'TM_VF_sphincs_128_All.png', 'SPHINCS+ 128 Versions vs SHA'],
    [['./output/sphincs192_ref', './output/sphincs192_sha256_ref', './output/sphincs192_sha512_ref', './output/sphincs192_avx2', './output/sphincs192_sha256_avx2', './output/sphincs192_sha512_avx2'], 'TM_VF_sphincs_192_All.png', 'SPHINCS+ 192 Versions vs SHA'],
    [['./output/sphincs256_ref', './output/sphincs256_sha256_ref', './output/sphincs256_sha512_ref', './output/sphincs256_avx2', './output/sphincs256_sha256_avx2', './output/sphincs256_sha512_avx2'], 'TM_VF_sphincs_256_All.png', 'SPHINCS+ 256 Versions vs SHA'],
    # DIFFERENT SECURITY LEVELS WITH NO SHA
    [['./output/dilithium2_ref', './output/falcon2_ref', './output/sphincs128_ref', './output/dilithium2_avx2', './output/falcon2_avx2', './output/sphincs128_avx2'], 'TM_VF_128bit_security_level.png', 'Security Level 1 & 2'],
    [['./output/dilithium3_ref', './output/sphincs192_ref', './output/dilithium3_avx2', './output/sphincs192_avx2'], 'TM_VF_192bit_security_level.png', 'Security Level 3'],
    [['./output/dilithium5_ref', './output/falcon5_ref', './output/sphincs256_ref', './output/dilithium5_avx2', './output/falcon5_avx2', './output/sphincs256_avx2'], 'TM_VF_256bit_security_level.png', 'Security Level 5'],
    # DIFFERENT SECURITY LEVELS WITH SHA-256
    [['./output/dilithium2_sha256_ref', './output/falcon2_ref_sha256', './output/sphincs128_sha256_ref', './output/dilithium2_sha256_avx2', './output/falcon2_avx2_sha256', './output/sphincs128_sha256_avx2', './output/rsa_128_sha256'], 'deprecated/TM_VF_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
    [['./output/dilithium3_sha256_ref', './output/sphincs192_sha256_ref', './output/dilithium3_sha256_avx2', './output/sphincs192_sha256_avx2', './output/rsa_192_sha256'], 'deprecated/TM_VF_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
    [['./output/dilithium5_sha256_ref', './output/falcon5_ref_sha256', './output/sphincs256_sha256_ref', './output/dilithium5_sha256_avx2', './output/falcon5_avx2_sha256', './output/sphincs256_sha256_avx2', './output/rsa_256_sha256'], 'deprecated/TM_VF_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
    # DIFFERENT SECURITY LEVELS WITH SHA-512
    [['./output/dilithium2_sha512_ref', './output/falcon2_ref_sha512', './output/sphincs128_sha512_ref', './output/dilithium2_sha512_avx2', './output/falcon2_avx2_sha512', './output/sphincs128_sha512_avx2', './output/rsa_128_sha512'], 'deprecated/TM_VF_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
    [['./output/dilithium3_sha512_ref', './output/sphincs192_sha512_ref', './output/dilithium3_sha512_avx2', './output/sphincs192_sha512_avx2', './output/rsa_192_sha512'], 'deprecated/TM_VF_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
    [['./output/dilithium5_sha512_ref', './output/falcon5_ref_sha512', './output/sphincs256_sha512_ref', './output/dilithium5_sha512_avx2', './output/falcon5_avx2_sha512', './output/sphincs256_sha512_avx2', './output/rsa_256_sha512'], 'deprecated/TM_VF_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512'],
    # DOUBLE CHECK
    [['./output/dilithium2_avx2', './output/dilithium3_avx2', './output/dilithium5_avx2', './liboqs_double_check/risultati_Dilithium2_avx2', './liboqs_double_check/risultati_Dilithium3_avx2', './liboqs_double_check/risultati_Dilithium5_avx2'], 'double_check/TM_VF_dilithium.png', 'Dilithium Version - Double Check'],
    [['./output/falcon2_avx2', './output/falcon5_avx2', './liboqs_double_check/risultati_Falcon-512_avx2', './liboqs_double_check/risultati_Falcon-1024_avx2'], 'double_check/TM_VF_falcon.png', 'Falcon Version - Double Check'],
    [['./output/sphincs128_avx2', './output/sphincs192_avx2', './output/sphincs256_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-128f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-192f-simple_avx2', './liboqs_double_check/risultati_SPHINCS+-SHA2-256f-simple_avx2'], 'double_check/TM_VF_sphincs.png', 'Sphincs+ Version - Double Check']
]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Verify Time Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_verify_time_plot(df_all, './plot/Time_Verify/' + file_paths[1], file_paths[2])




### ============================================================
### === TEMPI DI VERIFICA TRA ALGORITMI con SHA - ISTOGRAMMI ===
### ============================================================

# Funzione per creare il grafico a barre con il tempo medio di firma
def create_sign_time_histogram_plot(df_all, output_file, title):
    plt.figure(figsize=(12,7))
    
    # Calcola il tempo medio di firma per ogni combinazione di algoritmo e versione
    avg_sign_times = df_all.groupby(['algorithm', 'version'])['verify_time'].mean().reset_index()
    
    # Crea il grafico a barre
    sns.barplot(x='algorithm', y='verify_time', hue='version', data=avg_sign_times, palette=plot_colors)
    
    plt.xlabel('Algorithm')
    plt.ylabel('Average Verify Time (seconds)')
    plt.title('Average Verify Time by Algorithm and Version - ' + title)
    plt.legend(title='Version')
    plt.grid(True)
    plt.yscale('log')
    save_or_show_plot(output_file)
    plt.close()
    # Aggiorna la progress bar
    pbar.update(1)

# Gruppi di file da confrontare + nome di salvataggio grafo
file_groups = [ # WITH SHA-256
            [['./output/dilithium2_sha256_ref', './output/dilithium3_sha256_ref', './output/dilithium5_sha256_ref', './output/dilithium2_sha256_avx2', './output/dilithium3_sha256_avx2', './output/dilithium5_sha256_avx2'], 'TM_VF_H_dilithium_sha256.png', 'Dilithium Versions with SHA-256'],
            [['./output/falcon2_ref_sha256', './output/falcon5_ref_sha256', './output/falcon2_avx2_sha256', './output/falcon5_avx2_sha256'], 'TM_VF_H_falcon_sha256.png', 'Falcon Versions with SHA-256'],
            [['./output/sphincs128_sha256_ref', './output/sphincs192_sha256_ref', './output/sphincs256_sha256_ref', './output/sphincs128_sha256_avx2', './output/sphincs192_sha256_avx2', './output/sphincs256_sha256_avx2'], 'TM_VF_H_sphincs_sha256.png', 'Sphincs+ Versions with SHA-256'],
            [['./output/rsa_128_sha256', './output/rsa_192_sha256', './output/rsa_256_sha256'], 'TM_VF_H_rsa_sha256.png', 'RSA Versions with SHA-256'],
            # WITH SHA-512
            [['./output/dilithium2_sha512_ref', './output/dilithium3_sha512_ref', './output/dilithium5_sha512_ref', './output/dilithium2_sha512_avx2', './output/dilithium3_sha512_avx2', './output/dilithium5_sha512_avx2'], 'TM_VF_H_dilithium_sha512.png', 'Dilithium Versions with SHA-512'],
            [['./output/falcon2_ref_sha512', './output/falcon5_ref_sha512', './output/falcon2_avx2_sha512', './output/falcon5_avx2_sha512'], 'TM_VF_H_falcon_sha512.png', 'Falcon Versions with SHA-512'],
            [['./output/sphincs128_sha512_ref', './output/sphincs192_sha512_ref', './output/sphincs256_sha512_ref', './output/sphincs128_sha512_avx2', './output/sphincs192_sha512_avx2', './output/sphincs256_sha512_avx2'], 'TM_VF_H_sphincs_sha512.png', 'Sphincs+ Versions with SHA-512'],
            [['./output/rsa_128_sha512', './output/rsa_192_sha512', './output/rsa_256_sha512'], 'TM_VF_H_rsa_sha512.png', 'RSA Versions with SHA-512'],
            # DIFFERENT SECURITY LEVELS WITH SHA-256
            [['./output/dilithium2_sha256_ref', './output/falcon2_ref_sha256', './output/sphincs128_sha256_ref', './output/dilithium2_sha256_avx2', './output/falcon2_avx2_sha256', './output/sphincs128_sha256_avx2', './output/rsa_128_sha256'], 'TM_VF_H_128bit_security_level_sha256.png', 'Security Level 1 & 2 with SHA-256'],
            [['./output/dilithium3_sha256_ref', './output/sphincs192_sha256_ref', './output/dilithium3_sha256_avx2', './output/sphincs192_sha256_avx2', './output/rsa_192_sha256'], 'TM_VF_H_192bit_security_level_sha256.png', 'Security Level 3 with SHA-256'],
            [['./output/dilithium5_sha256_ref', './output/falcon5_ref_sha256', './output/sphincs256_sha256_ref', './output/dilithium5_sha256_avx2', './output/falcon5_avx2_sha256', './output/sphincs256_sha256_avx2', './output/rsa_256_sha256'], 'TM_VF_H_256bit_security_level_sha256.png', 'Security Level 5 with SHA-256'],
            # DIFFERENT SECURITY LEVELS WITH SHA-512
            [['./output/dilithium2_sha512_ref', './output/falcon2_ref_sha512', './output/sphincs128_sha512_ref', './output/dilithium2_sha512_avx2', './output/falcon2_avx2_sha512', './output/sphincs128_sha512_avx2', './output/rsa_128_sha512'], 'TM_VF_H_128bit_security_level_sha512.png', 'Security Level 1 & 2 with SHA-512'],
            [['./output/dilithium3_sha512_ref', './output/sphincs192_sha512_ref', './output/dilithium3_sha512_avx2', './output/sphincs192_sha512_avx2', './output/rsa_192_sha512'], 'TM_VF_H_192bit_security_level_sha512.png', 'Security Level 3 with SHA-512'],
            [['./output/dilithium5_sha512_ref', './output/falcon5_ref_sha512', './output/sphincs256_sha512_ref', './output/dilithium5_sha512_avx2', './output/falcon5_avx2_sha512', './output/sphincs256_sha512_avx2', './output/rsa_256_sha512'], 'TM_VF_H_256bit_security_level_sha512.png', 'Security Level 5 with SHA-512']
            ]

# Aggiungi una progress bar
with tqdm(total=len(file_groups), desc="Generating Verify Time H-Plots", unit="plot") as pbar:
    for file_paths in file_groups:
        # Lettura del gruppo di files
        df_all = read_multiple_files(file_paths[0])
        # Applicazione del mapping ai nomi degli algoritmi
        df_all['algorithm'] = df_all['algorithm'].map(algorithm_name_mapping)
        # Creazione del grafico con simboli diversi per REF e AVX2
        create_sign_time_histogram_plot(df_all, './plot/Time_Verify/' + file_paths[1], file_paths[2])