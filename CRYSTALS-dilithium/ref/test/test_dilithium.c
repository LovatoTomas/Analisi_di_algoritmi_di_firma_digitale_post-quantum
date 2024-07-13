/*
Author: Tomas Lovato
Version: 1
Date: 2024/07/13 11:00
Description: keygen test for dilithium - reference
*/

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include "../randombytes.h"
#include "../sign.h"

void print_hex(const uint8_t *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02X", data[i]);
    }
    printf("\n");
}

int main(void) {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    clock_t start, end;
    double cpu_time_used;

    // Misurazione del tempo di generazione delle chiavi
    start = clock();
    if (crypto_sign_keypair(pk, sk) != 0) {
        fprintf(stderr, "Errore nella generazione delle chiavi\n");
        return 1;
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    printf("Tempo di generazione delle chiavi: %f secondi\n", cpu_time_used);
    printf("Chiave pubblica (%d bytes):\n", CRYPTO_PUBLICKEYBYTES);
    print_hex(pk, CRYPTO_PUBLICKEYBYTES);
    printf("Chiave privata (%d bytes):\n", CRYPTO_SECRETKEYBYTES);
    print_hex(sk, CRYPTO_SECRETKEYBYTES);

    return 0;
}

