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

# Definisci la struttura OQS_SIG senza le funzioni
class OQS_SIG(ctypes.Structure):
    pass

# Definisci le funzioni all'interno di una classe separata
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

# Definisci le funzioni C dalla libreria liboqs
liboqs.OQS_SIG_new.restype = ctypes.POINTER(OQS_SIG)
liboqs.OQS_SIG_free.argtypes = [ctypes.POINTER(OQS_SIG)]
liboqs.OQS_SIG_alg_identifier.restype = ctypes.c_char_p
liboqs.OQS_SIG_alg_count.restype = ctypes.c_size_t
liboqs.OQS_SIG_keypair.argtypes = [ctypes.POINTER(OQS_SIG), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
liboqs.OQS_SIG_sign.argtypes = [ctypes.POINTER(OQS_SIG), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte)]
liboqs.OQS_SIG_verify.argtypes = [ctypes.POINTER(OQS_SIG), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte)]

# Verifica gli algoritmi disponibili
num_algs = liboqs.OQS_SIG_alg_count()
available_algs = [liboqs.OQS_SIG_alg_identifier(i).decode('utf-8') for i in range(num_algs)]

print("Algoritmi disponibili:", available_algs)

# Schemi di firma da testare
schemes = [
    "Dilithium2", "Dilithium3", "Dilithium5", 
    "Falcon-512", "Falcon-1024", 
    "SPHINCS+-SHA2-128f-simple",
    "SPHINCS+-SHA2-192f-simple",
    "SPHINCS+-SHA2-256f-simple",
]

# Funzione per misurare i tempi
def measure_times(scheme_name, message_size):
    print(f"Iniziando i test per l'algoritmo {scheme_name} con messaggio di dimensione {message_size} byte.")
    if scheme_name not in available_algs:
        raise ValueError(f"Algoritmo {scheme_name} non trovato")
    
    # Ottenere l'algoritmo
    alg_index = available_algs.index(scheme_name)
    alg = liboqs.OQS_SIG_alg_identifier(alg_index)
    if alg is None:
        raise ValueError(f"Algoritmo {scheme_name} non trovato")
    
    # Creare un'istanza della struttura
    print(f"Creazione della struttura per {scheme_name}.")
    sig = liboqs.OQS_SIG_new(alg)
    if not sig:
        raise ValueError(f"Creazione della struttura SIG fallita per {scheme_name}")

    # Generazione chiavi
    pubkey = (ctypes.c_ubyte * sig.contents.length_public_key)()
    privkey = (ctypes.c_ubyte * sig.contents.length_secret_key)()
    print(f"Generazione delle chiavi per {scheme_name}.")
    start_time = time.time()
    if liboqs.OQS_SIG_keypair(sig, pubkey, privkey) != 0:
        raise ValueError(f"Generazione delle chiavi fallita per {scheme_name}")
    keygen_time = time.time() - start_time
    print(f"Tempo di generazione delle chiavi: {keygen_time:.6f} secondi.")

    # Messaggio
    message = (ctypes.c_ubyte * message_size)(*b'a' * message_size)

    # Firma
    signature = (ctypes.c_ubyte * sig.contents.length_signature)()
    sig_len = ctypes.c_size_t()
    print(f"Firma del messaggio per {scheme_name}.")
    start_time = time.time()
    if liboqs.OQS_SIG_sign(sig, signature, ctypes.byref(sig_len), message, len(message), privkey) != 0:
        raise ValueError(f"Firma fallita per {scheme_name}")
    sign_time = time.time() - start_time
    print(f"Tempo di firma: {sign_time:.6f} secondi.")

    # Verifica
    print(f"Verifica della firma per {scheme_name}.")
    start_time = time.time()
    if liboqs.OQS_SIG_verify(sig, message, len(message), signature, sig_len.value, pubkey) != 0:
        raise ValueError(f"Verifica fallita per {scheme_name}")
    verify_time = time.time() - start_time
    print(f"Tempo di verifica: {verify_time:.6f} secondi.")

    # Libera la memoria
    liboqs.OQS_SIG_free(sig)
    print(f"Test per {scheme_name} completati.")

    return keygen_time, sign_time, verify_time

# Dimensioni dei messaggi da testare
message_sizes = [64, 128, 256, 512, 1024, 2048]

# Numero di iterazioni per ogni test
iterations = 100

# Esegui i test
results = []
for scheme in schemes:
    if scheme not in available_algs:
        print(f"Algoritmo {scheme} non disponibile. Saltando.")
        continue

    for size in message_sizes:
        keygen_times = []
        sign_times = []
        verify_times = []
        for i in range(iterations):
            print(f"Iterazione {i+1}/{iterations} per {scheme} con messaggio di dimensione {size} byte.")
            keygen_time, sign_time, verify_time = measure_times(scheme, size)
            keygen_times.append(keygen_time)
            sign_times.append(sign_time)
            verify_times.append(verify_time)
        
        avg_keygen_time = np.mean(keygen_times)
        avg_sign_time = np.mean(sign_times)
        avg_verify_time = np.mean(verify_times)
        
        results.append({
            'scheme': scheme,
            'message_size': size,
            'avg_keygen_time': avg_keygen_time,
            'avg_sign_time': avg_sign_time,
            'avg_verify_time': avg_verify_time
        })

# Scrivi i risultati su file
output_file = "risultati_tempi_medi.txt"
with open(output_file, "w") as f:
    for result in results:
        f.write(f"Scheme: {result['scheme']}, Message Size: {result['message_size']} bytes\n")
        f.write(f"  Avg Keygen Time: {result['avg_keygen_time']:.6f} seconds\n")
        f.write(f"  Avg Sign Time: {result['avg_sign_time']:.6f} seconds\n")
        f.write(f"  Avg Verify Time: {result['avg_verify_time']:.6f} seconds\n")
        f.write("\n")

print(f"Risultati scritti su {output_file}")
