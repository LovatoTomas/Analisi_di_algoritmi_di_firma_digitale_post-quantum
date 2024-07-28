#
#Author: Tomas Lovato
#Version: 2
#Date: 2024/07/28 15:30
#Description: standardizzati i metodi di valutazione e output
#

import ctypes
import os
import time
import numpy as np

# Prova a caricare la libreria dalle directory standard
try:
    liboqs = ctypes.CDLL("liboqs.so")
    print("liboqs.so caricato correttamente.")
except OSError:
    print("liboqs.so non trovata. Assicurati di aver installato correttamente liboqs.")
    exit(1)

# Definisce la struttura OQS_SIG senza le funzioni
class OQS_SIG(ctypes.Structure):
    pass

# Definisce le funzioni all'interno di una classe separata
class OQS_SIG_Functions:
    _fields_ = [
        ("method_name", ctypes.c_char_p),
        ("alg_version", ctypes.c_char_p),
        ("claimed_nist_level", ctypes.c_uint8),
        ("is_euf_cma", ctypes.c_uint8),
        ("length_public_key", ctypes.c_size_t),
        ("length_secret_key", ctypes.c_size_t),
        ("length_signature", ctypes.c_size_t),
        ("keypair", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(OQS_SIG))),
        ("sign", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(OQS_SIG))),
        ("verify", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(OQS_SIG))),
    ]

OQS_SIG._fields_ = OQS_SIG_Functions._fields_

# Definisce le funzioni C dalla libreria liboqs (che a loro volta richiamano quelle delle librerie sottostanti)
liboqs.OQS_SIG_new.restype = ctypes.POINTER(OQS_SIG)
liboqs.OQS_SIG_free.argtypes = [ctypes.POINTER(OQS_SIG)]
liboqs.OQS_SIG_alg_identifier.restype = ctypes.c_char_p
liboqs.OQS_SIG_alg_count.restype = ctypes.c_size_t
liboqs.OQS_SIG_keypair.argtypes = [ctypes.POINTER(OQS_SIG), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
liboqs.OQS_SIG_sign.argtypes = [ctypes.POINTER(OQS_SIG), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte)]
liboqs.OQS_SIG_verify.argtypes = [ctypes.POINTER(OQS_SIG), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte)]

# Verifica gli algoritmi disponibili nell'installazione
num_algs = liboqs.OQS_SIG_alg_count()
available_algs = [liboqs.OQS_SIG_alg_identifier(i).decode('utf-8') for i in range(num_algs)]

print("Algoritmi disponibili:", available_algs)

# Schemi di firma da testare, si testano solo gli AVX2 degli schemi già provati
schemes = [
    "Dilithium2", "Dilithium3", "Dilithium5", 
    "Falcon-512", "Falcon-1024", 
    "SPHINCS+-SHA2-128f-simple",
    "SPHINCS+-SHA2-192f-simple",
    "SPHINCS+-SHA2-256f-simple"
]

# Dimensioni dei messaggi da testare (32 byte a circa 16 MB, con fattore 2)
message_sizes = [2**i for i in range(5, 25)]

# Numero di iterazioni per ogni test, su cui fare la media dei tempi
iterations = 100

# Dizionario per associare i nomi dei file di output a ciascun algoritmo
output_files = {scheme: f"risultati_{scheme}" for scheme in schemes}

# Funzione per misurare i tempi di keygen, firma e verifica per ogni schema e lunghezza del messaggio.
def measure_times(scheme_name, message_size):
    print(f"Iniziando i test per l'algoritmo {scheme_name} con messaggio di dimensione {message_size} byte.")
    if scheme_name not in available_algs:
        raise ValueError(f"=== ERR: Algoritmo {scheme_name} non trovato ===")
    
    # Instanziare l'algoritmo a partire dal nome
    alg_index = available_algs.index(scheme_name)
    alg = liboqs.OQS_SIG_alg_identifier(alg_index)
    if alg is None:
        raise ValueError(f"=== ERR: Algoritmo {scheme_name} non trovato ===")
    
    # Creare un'istanza della struttura (contiene tutte le caratteristiche)
    print(f"--- Creazione della struttura per {scheme_name}. ---")
    sig = liboqs.OQS_SIG_new(alg)
    if not sig:
        raise ValueError(f"=== ERR: Creazione della struttura SIG fallita per {scheme_name} ===")

    # Generazione chiavi - Calcolo del tempo
    pubkey = (ctypes.c_ubyte * sig.contents.length_public_key)()
    privkey = (ctypes.c_ubyte * sig.contents.length_secret_key)()
    print(f"--- Generazione delle chiavi per {scheme_name}. ---")
    start_time = time.time()
    if liboqs.OQS_SIG_keypair(sig, pubkey, privkey) != 0:
        raise ValueError(f"=== ERR: Generazione delle chiavi fallita per {scheme_name} ===")
    keygen_time = time.time() - start_time
    print(f"--- Tempo di generazione delle chiavi: {keygen_time:.6f} secondi. ---")

    # Generazione del messaggio abbastanza "stupida"
    message = (ctypes.c_ubyte * message_size)(*b'a' * message_size)

    # Firma del messaggio - Calcolo del tempo
    signature = (ctypes.c_ubyte * sig.contents.length_signature)()
    sig_len = ctypes.c_size_t()
    print(f"--- Firma del messaggio per {scheme_name}. ---")
    start_time = time.time()
    if liboqs.OQS_SIG_sign(sig, signature, ctypes.byref(sig_len), message, len(message), privkey) != 0:
        raise ValueError(f"Firma fallita per {scheme_name}")
    sign_time = time.time() - start_time
    print(f"--- Tempo di firma: {sign_time:.6f} secondi. ---")

    # Verifica del messaggio - Calcolo del tempo
    print(f"--- Verifica della firma per {scheme_name}. ---")
    start_time = time.time()
    if liboqs.OQS_SIG_verify(sig, message, len(message), signature, sig_len.value, pubkey) != 0:
        raise ValueError(f"=== ERR: Verifica fallita per {scheme_name} ===")
    verify_time = time.time() - start_time
    print(f"--- Tempo di verifica: {verify_time:.6f} secondi. ---")

    # Liberazione della memoria occupata dalla struttura
    liboqs.OQS_SIG_free(sig)
    print(f"--- Test per {scheme_name} completati. ---")

    # Ritorna i risultati insieme ai metadati delle chiavi e della firma
    return {
        'message_size': message_size,
        'total_message_size': message_size + sig_len.value,
        'pubkey_size': sig.contents.length_public_key,
        'privkey_size': sig.contents.length_secret_key,
        'sig_size': sig.contents.length_signature,
        'avg_keygen_time': keygen_time,
        'avg_sign_time': sign_time,
        'avg_verify_time': verify_time
    }

# Esegue i test: per ogni schema e lunghezza del messaggio esegue 100 volte il test, calcola la media e memorizza i risultati
for scheme in schemes:
    if scheme not in available_algs:
        print(f"=== ERRORE: Algoritmo {scheme} non disponibile. SKIP ===")
        continue

    # Struttura dati per i risultati di ognuno dei 100 tentativi
    results = []
    for size in message_sizes:
        keygen_times = [] # struttura dati dedicata ai tempi di keygen
        sign_times = [] # struttura dati dedicata ai tempi di firma
        verify_times = [] # struttura dati dedicata ai tempi di verifica
        for i in range(iterations):
            print(f"Iterazione {i+1}/{iterations} per {scheme} con messaggio di dimensione {size} byte.")
            times = measure_times(scheme, size)
            keygen_times.append(times['avg_keygen_time'])
            sign_times.append(times['avg_sign_time'])
            verify_times.append(times['avg_verify_time'])
        
        # Calcolo delle medie
        avg_keygen_time = np.mean(keygen_times)
        avg_sign_time = np.mean(sign_times)
        avg_verify_time = np.mean(verify_times)
        
        results.append({
            'message_size': size,
            'total_message_size': size + times['sig_size'],
            'pubkey_size': times['pubkey_size'],
            'privkey_size': times['privkey_size'],
            'sig_size': times['sig_size'],
            'avg_keygen_time': avg_keygen_time,
            'avg_sign_time': avg_sign_time,
            'avg_verify_time': avg_verify_time,
            'hash_size': size  # Per questo algoritmo, la hashsize coincide con la lunghezza del messagio perchè NON si fa hashing
        })

    # Scrittura risultati su file
    output_file = output_files[scheme]
    with open(output_file, "w") as f:
        for result in results:
            f.write(f"|{result['message_size']}|{result['total_message_size']}|{result['pubkey_size']}|{result['privkey_size']}|{result['sig_size']}|{result['avg_keygen_time']:.6f}|{result['avg_sign_time']:.6f}|{result['avg_verify_time']:.6f}|{result['hash_size']}|\n")

    print(f"Risultati per {scheme} scritti su {output_file}")