/*
Author: Tomas Lovato
Version: 5
Date: 2024/07/14 16:30
Description: performance test per Dilithium, rimosso la misurazione del tempo per la firma non corretta (messaggio corrotto).
*/

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h> // Libreria per la misurazione dei tempi
#include "../randombytes.h"
#include "../sign.h"

#define MINMLEN 64 // Minima lunghezza messaggio in bytes
#define MAXMLEN 18000000 // Massima lunghezza messaggio in bytes (circa 18MB)
#define INCREMENT 1.2
#define VERBOSE_LEVEL 0 // 0 = Stampa del file; 1 = Stampa minima; 2 = Stampa delle chiavi
long unsigned int MLEN = MINMLEN; // Message Length in Bytes
int ITERATIONS = 10;

// Codice per la stampa delle chiavi private e pubbliche
void print_hex(const uint8_t *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02X", data[i]);
    }
    printf("\n");
}

static double average_double(double *t, size_t tlen) {
  size_t i;
  double acc=0;

  for(i=0;i<tlen;i++)
    acc += t[i];

  return acc/tlen;
}
static long average_long_int(long *t, size_t tlen) {
  size_t i;
  long acc=0;

  for(i=0;i<tlen;i++)
    acc += t[i];

  return acc/tlen;
}

int main(int argc, char **argv)
{
  size_t i, j;
  int ret;
  size_t mlen, smlen;
  uint8_t b;
  uint8_t m[MAXMLEN + CRYPTO_BYTES];
  uint8_t m2[MAXMLEN + CRYPTO_BYTES];
  uint8_t sm[MAXMLEN + CRYPTO_BYTES];
  uint8_t pk[CRYPTO_PUBLICKEYBYTES];
  uint8_t sk[CRYPTO_SECRETKEYBYTES];
  clock_t start, end;                   // Variabili per misurare i tempi di esecuzione di algoritmi
  double keygen_time[ITERATIONS];       // Valore dei tempi di keygen
  double signature_time[ITERATIONS];    // Valore dei tempi di firma
  double ok_check_time[ITERATIONS];     // Valore dei tempi di verifica
  long keygen_cycles[ITERATIONS];
  long signature_cycles[ITERATIONS];
  long ok_check_cycles[ITERATIONS];

  // Update numero iterazioni:
  if(argc > 2)
  {
    ITERATIONS = atoi(argv[2]);
  }

  // Apertura del file di output:
  const char *filename = "output.txt";
  if(argc > 1)
  {
    filename = argv[1];
    printf("=== FILE OUTPUT: %s ===\n",filename);
  }
  FILE *file = fopen(filename, "w");
  // Errore di apertura?
  if (file == NULL) {
    perror("Errore nell'aprire il file");
    return -1;
  }

  for(MLEN = 64; MLEN < MAXMLEN; MLEN = MLEN * INCREMENT) 
  {
    for(i = 0; i < ITERATIONS; i++)
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
      keygen_cycles[i] = (long)end - start;
      keygen_time[i] = ((double) keygen_cycles[i]) / CLOCKS_PER_SEC;
      // OUTPUT chiavi generate
      if(VERBOSE_LEVEL >= 1)
      {
        printf("Tempo di generazione delle chiavi: %f secondi\n", keygen_time[i]);
        printf("Cicli di clock CPU: %ld\n", keygen_cycles[i]);
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
      signature_cycles[i] = (long)end - start;
      signature_time[i] = ((double) signature_cycles[i]) / CLOCKS_PER_SEC;
      // OUTPUT
      if(VERBOSE_LEVEL >= 1)
      {
        printf("Tempo di firma di un messaggio: %f secondi\n", signature_time[i]);
        printf("Cicli di clock CPU: %ld\n", signature_cycles[i]);
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
      ok_check_cycles[i] = (long)end - start;
      ok_check_time[i] = ((double) ok_check_cycles[i]) / CLOCKS_PER_SEC;
      // OUTPUT
      if(VERBOSE_LEVEL >= 1)
      {
        printf("Tempo di verifica della firma: %f secondi\n", ok_check_time[i]);
        printf("Cicli di clock CPU: %ld\n", ok_check_cycles[i]);
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
    }

    char output_line[512];
    sprintf(output_line, "|%lu|%lu|%d|%d|%d|%f|%ld|%f|%ld|%f|%ld|\r\n", 
      MLEN, smlen, CRYPTO_PUBLICKEYBYTES, CRYPTO_SECRETKEYBYTES, CRYPTO_BYTES, 
      average_double(keygen_time, ITERATIONS), average_long_int(keygen_cycles, ITERATIONS),
      average_double(signature_time, ITERATIONS), average_long_int(signature_cycles, ITERATIONS),
      average_double(ok_check_time, ITERATIONS), average_long_int(ok_check_cycles, ITERATIONS));
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