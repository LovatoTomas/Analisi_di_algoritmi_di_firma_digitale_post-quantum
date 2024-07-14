# Autore: Tomas Lovato
# Data: 2024/07/13 18:00
# Analisi dei dati raccolti dagli algoritmi

import pandas as pd
import matplotlib.pyplot as plt

# Funzione per leggere i dati dal file
def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    #for riga in lines:
        # Fai qualcosa con la riga
        #print(riga.strip())

    data = []
    for line in lines:
        line = line.strip()
        if line:
            fields = line.split('|')
            data.append([int(fields[1]), int(fields[2]), int(fields[3]), int(fields[4]), int(fields[5]), float(fields[6]), int(fields[7]), float(fields[8]), int(fields[9]), float(fields[10]), int(fields[11]), float(fields[12]), int(fields[13])])

    columns = ['msg_len', 'signed_msg_len', 'pub_key_size', 'priv_key_size', 'signature_size', 'keygen_time', 'keygen_cycles', 'sign_time', 'sign_cycles', 'verify_time_correct', 'verify_cycles_correct', 'verify_time_corrupt', 'verify_cycles_corrupt']

    df = pd.DataFrame(data, columns=columns)
    return df

# Leggere il file caricato
file_path = './CRYSTALS-dilithium/ref/20240713_output_dilithium2.txt'
df = read_data(file_path)

# Grafico della dimensione delle chiavi al variare della lunghezza del messaggio
plt.figure(figsize=(10, 6))
plt.plot(df['msg_len'], df['pub_key_size'], label='Public Key Size')
plt.plot(df['msg_len'], df['priv_key_size'], label='Private Key Size')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Key Size (bytes)')
plt.title('Key Sizes vs Message Length')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

# Grafico della dimensione del messaggio originale e firmato al variare della lunghezza del messaggio
plt.figure(figsize=(10, 6))
plt.plot(df['msg_len'], df['msg_len'], label='Original Message Length')
plt.plot(df['msg_len'], df['signed_msg_len'], label='Signed Message Length')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Length (bytes)')
plt.title('Original and Signed Message Length vs Message Length')
plt.legend()
plt.grid(True)
plt.xscale('log')  # Usare scala logaritmica per gestire un ampio intervallo di valori
plt.yscale('log')
plt.show()

# Grafico dei tempi di keygen, firma e verifica al variare della lunghezza del messaggio
plt.figure(figsize=(10, 6))
plt.plot(df['msg_len'], df['keygen_time'], label='Keygen Time')
plt.plot(df['msg_len'], df['sign_time'], label='Sign Time')
plt.plot(df['msg_len'], df['verify_time_correct'], label='Verify Time (Correct)')
plt.plot(df['msg_len'], df['verify_time_corrupt'], label='Verify Time (Corrupt)')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Time (seconds)')
plt.title('Keygen, Sign, and Verify Times vs Message Length')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df['msg_len'], df['keygen_time'], label='Keygen Time')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Time (seconds)')
plt.title('Keygen Time vs Message Length')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df['msg_len'], df['sign_time'], label='Sign Time')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Time (seconds)')
plt.title('Sign Time vs Message Length')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df['msg_len'], df['verify_time_correct'], label='Verify Time (Correct)')
plt.plot(df['msg_len'], df['verify_time_corrupt'], label='Verify Time (Corrupt)')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Time (seconds)')
plt.title('Verify Time vs Message Length')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

# Funzione per leggere e unire i dati da più file
def read_multiple_files(filenames):
    dataframes = [read_data(file) for file in filenames]
    for df, file in zip(dataframes, filenames):
        df['algorithm'] = file.split('_')[2].split('.')[0]  # estrai il nome dell'algoritmo dal nome del file
    return pd.concat(dataframes, ignore_index=True)

# Leggere i file di esempio (sostituire con i nomi reali dei file)
file_paths = ['./CRYSTALS-dilithium/ref/20240713_output_dilithium2.txt', './CRYSTALS-dilithium/ref/20240713_output_dilithium3.txt', './CRYSTALS-dilithium/ref/20240713_output_dilithium5.txt']
df_all = read_multiple_files(file_paths)

# Grafici di confronto tra algoritmi
import seaborn as sns

# 2.1 Confronto della dimensione delle chiavi tra algoritmi
plt.figure(figsize=(10, 6))
sns.lineplot(x='msg_len', y='pub_key_size', hue='algorithm', data=df_all, marker='o')
sns.lineplot(x='msg_len', y='priv_key_size', hue='algorithm', data=df_all, marker='o')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Key Size (bytes)')
plt.title('Key Sizes vs Message Length (Comparison)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

# 2.2 Confronto della dimensione del messaggio firmato tra algoritmi, mostrando anche il messaggio originale
plt.figure(figsize=(10, 6))
sns.lineplot(x='msg_len', y='msg_len', hue='algorithm', data=df_all, marker='o', legend='full')
sns.lineplot(x='msg_len', y='signed_msg_len', hue='algorithm', data=df_all, marker='o', legend='full')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Length (bytes)')
plt.title('Original and Signed Message Length vs Message Length (Comparison)')
plt.legend()
plt.grid(True)
plt.xscale('log')  # Usare scala logaritmica per gestire un ampio intervallo di valori
plt.yscale('log')
plt.show()

# 2.3 Confronto dei tempi di keygen, firma e verifica tra algoritmi
plt.figure(figsize=(10, 6))
sns.lineplot(x='msg_len', y='keygen_time', hue='algorithm', data=df_all, marker='o')
sns.lineplot(x='msg_len', y='sign_time', hue='algorithm', data=df_all, marker='o')
sns.lineplot(x='msg_len', y='verify_time_correct', hue='algorithm', data=df_all, marker='o')
sns.lineplot(x='msg_len', y='verify_time_corrupt', hue='algorithm', data=df_all, marker='o')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Time (seconds)')
plt.title('Keygen, Sign, and Verify Times vs Message Length (Comparison)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

plt.figure(figsize=(10, 6))
sns.lineplot(x='msg_len', y='keygen_time', hue='algorithm', data=df_all, marker='o')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Keygen Time (seconds)')
plt.title('Keygen Time vs Message Length (Comparison)')
plt.legend(title='Algorithm')
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

plt.figure(figsize=(10, 6))
sns.lineplot(x='msg_len', y='sign_time', hue='algorithm', data=df_all, marker='o')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Sign Time (seconds)')
plt.title('Sign Time vs Message Length (Comparison)')
plt.legend(title='Algorithm')
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()

plt.figure(figsize=(10, 6))
sns.lineplot(x='msg_len', y='sign_time', hue='algorithm', data=df_all, marker='o')
plt.xlabel('Message Length (bytes)')
plt.ylabel('Sign Time (seconds)')
plt.title('Sign Time vs Message Length (Comparison)')
plt.legend(title='Algorithm')
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.show()