#
#Author: Tomas Lovato
#Version: 1
#Date: 2024/07/28 10:30
#Description: verifica installazione liboqs
#

import ctypes

liboqs = ctypes.CDLL("liboqs.so")

liboqs.OQS_SIG_alg_identifier.restype = ctypes.c_char_p
liboqs.OQS_SIG_alg_count.restype = ctypes.c_size_t

num_algs = liboqs.OQS_SIG_alg_count()
algs = [liboqs.OQS_SIG_alg_identifier(i).decode('utf-8') for i in range(num_algs)]

print("Available algorithms:")
for alg in algs:
    print(alg)
