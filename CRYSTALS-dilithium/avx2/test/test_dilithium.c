/*
Author: Tomas Lovato
Version: 2
Date: 2024/07/13 11:30
Description: keygen test for dilithium - reference
*/

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h> // Libreria per la misurazione dei tempi
#include "../randombytes.h"
#include "../sign.h"
#include <math.h> // Per aumentare la dimensione del messaggio

#define MINMLEN 64 // Minima lunghezza messaggio in bytes
#define MAXMLEN 150000000 // Massima lunghezza messaggio in bytes
#define INCREMENT 1.2
#define VERBOSE_LEVEL 0 // 0 = Stampa del file; 1 = Stampa minima; 2 = Stampa delle chiavi
long unsigned int MLEN = MINMLEN; // Message Length in Bytes

// Codice per la stampa delle chiavi private e pubbliche
void print_hex(const uint8_t *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02X", data[i]);
    }
    printf("\n");
}

int main(void)
{
  size_t j;
  int ret;
  size_t mlen, smlen;
  uint8_t b;
  uint8_t m[MAXMLEN + CRYPTO_BYTES];
  uint8_t m2[MAXMLEN + CRYPTO_BYTES];
  uint8_t sm[MAXMLEN + CRYPTO_BYTES];
  uint8_t pk[CRYPTO_PUBLICKEYBYTES];
  uint8_t sk[CRYPTO_SECRETKEYBYTES];
  clock_t start, end;       // Variabili per misurare i tempi di esecuzione di algoritmi
  double keygen_time;       // Valore dei tempi di keygen
  double signature_time;    // Valore dei tempi di firma
  double ok_check_time;     // Valore dei tempi di verifica
  double cr_check_time;     // Valore dei tempi di verifica con messaggio corrotto
  long keygen_cycles;
  long signature_cycles;
  long ok_check_cycles;
  long cr_check_cycles;

  // Apertura del file di output:
  const char *filename = "output.txt";
  FILE *file = fopen(filename, "w");
  // Errore di apertua?
  if (file == NULL) {
    perror("Errore nell'aprire il file");
    return -1;
  }

  for(MLEN = 64; MLEN < MAXMLEN; MLEN = MLEN * INCREMENT) 
  {
    // Generazione del messaggio
    randombytes(m, MLEN);
    if(VERBOSE_LEVEL >= 1)
    {
      printf("Generato messaggio (%ld bytes):\n", MLEN);
      if(VERBOSE_LEVEL >= 2) print_hex(sk, MLEN);
    }

    // AVVIO Misurazione del tempo di generazione delle chiavi
    start = clock();
    crypto_sign_keypair(pk, sk);
    // TERMINE Misurazione del tempo di generazione delle chiavi
    end = clock();
    keygen_cycles = (long)end - start;
    keygen_time = ((double) keygen_cycles) / CLOCKS_PER_SEC;
    // OUTPUT chiavi generate
    if(VERBOSE_LEVEL >= 1)
    {
      printf("Tempo di generazione delle chiavi: %f secondi\n", keygen_time);
      printf("Cicli di clock CPU: %ld\n", keygen_cycles);
      printf("Chiave pubblica (%d bytes):\n", CRYPTO_PUBLICKEYBYTES);
      if(VERBOSE_LEVEL >= 2) print_hex(pk, CRYPTO_PUBLICKEYBYTES);
      printf("Chiave privata (%d bytes):\n\n", CRYPTO_SECRETKEYBYTES);
      if(VERBOSE_LEVEL >= 2) print_hex(sk, CRYPTO_SECRETKEYBYTES);
    }

    // AVVIO Misurazione del tempo di firma di un messaggio
    start = clock();
    crypto_sign(sm, &smlen, m, MLEN, sk);
    // TERMINE Misurazione del tempo di firma di un messaggio
    end = clock();
    signature_cycles = (long)end - start;
    signature_time = ((double) signature_cycles) / CLOCKS_PER_SEC;
    // OUTPUT
    if(VERBOSE_LEVEL >= 1)
    {
      printf("Tempo di firma di un messaggio: %f secondi\n", signature_time);
      printf("Cicli di clock CPU: %ld\n", signature_cycles);
      printf("Lunghezza del messaggio firmato: %zu bytes\n\n", smlen);
      if(VERBOSE_LEVEL >= 2) 
      {
        printf("Messaggio firmato:\n");
        print_hex(sm, smlen);
      }
    }

    // AVVIO Misurazione del tempo di verifica della firma
    start = clock();
    ret = crypto_sign_open(m2, &mlen, sm, smlen, pk);
    // TERMINE Misurazione del tempo di verifica
    end = clock();
    ok_check_cycles = (long)end - start;
    ok_check_time = ((double) ok_check_cycles) / CLOCKS_PER_SEC;
    // OUTPUT
    if(VERBOSE_LEVEL >= 1)
    {
      printf("Tempo di verifica della firma: %f secondi\n", ok_check_time);
      printf("Cicli di clock CPU: %ld\n", ok_check_cycles);
    }
    if(ret) {
      fprintf(stderr, "ERRORE - Verifica fallita\n\n");
      return -1;
    }
    if(smlen != MLEN + CRYPTO_BYTES) {
      fprintf(stderr, "ERRORE - Lunghezza firma del messaggio errata\n\n");
      return -1;
    }
    if(mlen != MLEN) {
      fprintf(stderr, "ERRORE - Lunghezza del messaggio errata\n\n");
      return -1;
    }
    for(j = 0; j < MLEN; ++j) {
      if(m2[j] != m[j]) {
        fprintf(stderr, "INFO - Verifica della firma fallita --> Messaggio danneggiato?\n\n");
        return -1;
      }
    }
    if(VERBOSE_LEVEL >= 1)
    {
      fprintf(stderr, "INFO - Verifica della firma riuscita!\n\n");
    }
    // Corruzione volontaria della firma
    randombytes((uint8_t *)&j, sizeof(j));
    do {
      randombytes(&b, 1);
    } while(!b);
    sm[j % (MLEN + CRYPTO_BYTES)] += b;
    // Nuovo tentativo di verifica con corruzione
    // AVVIO Misurazione del tempo di verifica della firma
    start = clock();
    ret = crypto_sign_open(m2, &mlen, sm, smlen, pk);
    // TERMINE Misurazione del tempo di verifica
    end = clock();
    cr_check_cycles = (long)end - start;
    cr_check_time = ((double) cr_check_cycles) / CLOCKS_PER_SEC;
    // OUTPUT
    if(VERBOSE_LEVEL >= 1)
    {
      printf("Tempo di verifica della firma con messaggio corrotto: %f secondi\n", cr_check_time);
      printf("Cicli di clock CPU: %ld\n", cr_check_cycles);
    }
    if(!ret) {
      fprintf(stderr, "INFO - Verifica riuscita - Rarissimi casi...\n\n");
      return -1;
    }
    if(VERBOSE_LEVEL >= 1)
    {
      printf("INFO - Verifica NON riuscita");
      printf("\n===\n\n");
    }

    char output_line[512];
    sprintf(output_line, "|%lu|%lu|%d|%d|%d|%f|%ld|%f|%ld|%f|%ld|%f|%ld|\r\n", MLEN, smlen, CRYPTO_PUBLICKEYBYTES, CRYPTO_SECRETKEYBYTES, CRYPTO_BYTES, keygen_time, keygen_cycles, signature_time, signature_cycles, ok_check_time, ok_check_cycles, cr_check_time, cr_check_cycles);
    printf("%s", output_line);

    // Scrittura nel file
    if (fprintf(file, "%s", output_line) < 0) {
      perror("Errore nella scrittura del file");
      fclose(file);
      return -1;
    }
  }

  printf("CRYPTO_PUBLICKEYBYTES = %d\n", CRYPTO_PUBLICKEYBYTES);
  printf("CRYPTO_SECRETKEYBYTES = %d\n", CRYPTO_SECRETKEYBYTES);
  printf("CRYPTO_BYTES = %d\n", CRYPTO_BYTES);

  // Chiusura del file:
  if (fclose(file) != 0) {
    perror("Errore nella chiusura del file");
    return -1;
  }

  return 0;
}
