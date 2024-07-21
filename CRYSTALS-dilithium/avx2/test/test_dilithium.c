/*
Author: Tomas Lovato
Version: 8
Date: 2024/07/21 10:30
Description: performance test per Dilithium con
                          - messaggio originale
                          - hash messaggio sha256
                          - hash messaggio sha512
*/

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h> // Libreria per la misurazione dei tempi
#include <openssl/sha.h> // Include OpenSSL for SHA-256
#include "../randombytes.h"
#include "../sign.h"

#define SHA256LEN 32
#define SHA512LEN 64
#define MINMLEN 64 // Minima lunghezza messaggio in bytes
#define MAXMLEN 18000000 // Massima lunghezza messaggio in bytes (circa 18MB)
#define VERBOSE_LEVEL 0 // 0 = Stampa del file; 1 = Stampa minima; 2 = Stampa delle chiavi
long unsigned int MLEN = MINMLEN; // Message Length in Bytes
int INCREMENT = 2;
long unsigned int ITERATIONS = 10;

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

int loop(const char* filename, int sha256, int sha512)
{
  size_t i, j;
  int ret;
  size_t mlen, smlen;
  uint8_t* m = malloc(MAXMLEN + CRYPTO_BYTES);
  uint8_t* m2= malloc(MAXMLEN + CRYPTO_BYTES);
  uint8_t* sm= malloc(MAXMLEN + CRYPTO_BYTES);
  uint8_t pk[CRYPTO_PUBLICKEYBYTES];
  uint8_t sk[CRYPTO_SECRETKEYBYTES];
  clock_t start, end;                   // Variabili per misurare i tempi di esecuzione di algoritmi
  double keygen_time[ITERATIONS];       // Valore dei tempi di keygen
  double signature_time[ITERATIONS];    // Valore dei tempi di firma
  double ok_check_time[ITERATIONS];     // Valore dei tempi di verifica
  long keygen_cycles[ITERATIONS];
  long signature_cycles[ITERATIONS];
  long ok_check_cycles[ITERATIONS];
  uint8_t hash256[SHA256LEN];
  uint8_t hash512[SHA512LEN];

  // ====== AVVIO CICLO PER MESSAGGIO COMPLETO ======
  FILE *file = fopen(filename, "w");
  // Errore di apertura?
  if (file == NULL) {
    perror("Errore nell'aprire il file");
    return -1;
  }
	printf("|MLEN|MTOTLEN|PUBLEN|PRVLEN|SIGLEN|KGTM|SIGTM|CHECKTM|HASHSZ|\r\n");

  for(MLEN = 64; MLEN < MAXMLEN; MLEN = MLEN * INCREMENT) 
  {
    for(i = 0; i < ITERATIONS; i++)
    {
      // Generazione del messaggio
      randombytes(m, MLEN);
      // Calcolo HASH SHA256 del messaggio:
      SHA256(m, MLEN, hash256);
      // Calcolo HASH SHA512 del messaggio:
      SHA512(m, MLEN, hash512);
      if(VERBOSE_LEVEL >= 1)
      {
        printf("Generato messaggio (%ld bytes):\n", MLEN);
        if(VERBOSE_LEVEL >= 2) print_hex(m, MLEN);
        printf("Generato HASH256 (%d bytes):\n", SHA256LEN);
        if(VERBOSE_LEVEL >= 2) print_hex(hash256, SHA256LEN);
        printf("Generato HASH512 (%d bytes):\n", SHA512LEN);
        if(VERBOSE_LEVEL >= 2) print_hex(hash512, SHA512LEN);
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

      // AVVIO e TERMINE Misurazione del tempo di firma di un messaggio
      if(sha256)
      {
        start = clock();
        crypto_sign(sm, &smlen, hash256, SHA256LEN, sk);
        end = clock();
      }
      else if(sha512)
      {
        start = clock();
        crypto_sign(sm, &smlen, hash512, SHA512LEN, sk);
        end = clock();
      }
      else
      {
        start = clock();
        crypto_sign(sm, &smlen, m, MLEN, sk);
        end = clock();
      }
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
      if( (!sha256 && !sha512 && smlen != MLEN + CRYPTO_BYTES) || 
          (sha256 && smlen != SHA256LEN + CRYPTO_BYTES) || 
          (sha512 && smlen != SHA512LEN + CRYPTO_BYTES) ) 
      {
        fprintf(stderr, "ERRORE - Lunghezza firma del messaggio errata\n\n");
        return -1;
      }
      if( (!sha256 && !sha512 && mlen != MLEN) || 
          (sha256 && mlen != SHA256LEN) || 
          (sha512 && mlen != SHA512LEN) ) {
        fprintf(stderr, "ERRORE - Lunghezza del messaggio errata\n\n");
        return -1;
      }
      for(j = 0; j < mlen; ++j) {
        if( (!sha256 && !sha512 && m2[j] != m[j]) ||
          (sha256 && m2[j] != hash256[j]) || 
          (sha512 && m2[j] != hash512[j])) {
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
    sprintf(output_line, "|%lu|%lu|%d|%d|%d|%f|%f|%f|%lu|\r\n", 
      MLEN, smlen, CRYPTO_PUBLICKEYBYTES, CRYPTO_SECRETKEYBYTES, CRYPTO_BYTES, 
      average_double(keygen_time, ITERATIONS), 
      average_double(signature_time, ITERATIONS),
      average_double(ok_check_time, ITERATIONS), mlen);
    printf("%s", output_line);

    // Scrittura nel file
    if (fprintf(file, "%s", output_line) < 0) {
      perror("Errore nella scrittura del file");
      fclose(file);
      return -1;
    }
  }

  // Chiusura del file:
  if (fclose(file) != 0) {
    perror("Errore nella chiusura del file");
    return -1;
  }

  // Libero la memoria
  free(m);
  free(m2);
  free(sm);

  printf("CRYPTO_PUBLICKEYBYTES = %d\n", CRYPTO_PUBLICKEYBYTES);
  printf("CRYPTO_SECRETKEYBYTES = %d\n", CRYPTO_SECRETKEYBYTES);
  printf("CRYPTO_BYTES = %d\n", CRYPTO_BYTES);

  return 0;
}
int main(int argc, char **argv)
{  
	// Update del fattore di scala dei messaggi:
	if(argc > 5)
	{
		INCREMENT = atoi(argv[5]);
		printf("=== INCREMENT: %s ===\n", argv[5]);
	}

	// Update delle iterazioni su cui fare media:
	if(argc > 4)
	{
		ITERATIONS = (long unsigned int)atoi(argv[4]);
		printf("=== ITERATIONS: %s ===\n", argv[4]);
	}

	// Apertura del file di output:
	const char *filename1 = "out_dilithium";
	const char *filename2 = "out_dilithium_sha256";
	const char *filename3 = "out_dilithium_sha512";
	if(argc > 3)
	{
		filename1 = argv[1];
		printf("=== FILE OUTPUT 1: %s ===\n",filename1);
		filename2 = argv[2];
		printf("=== FILE OUTPUT 2: %s ===\n",filename2);
		filename3 = argv[3];
		printf("=== FILE OUTPUT 3: %s ===\n",filename3);
	}

  // Execute all on normal message
  loop(filename1, 0, 0);
  // Execute all on hash (sha256)
  loop(filename2, 1, 0);
  // Execute all on hash (sha512)
  loop(filename3, 0, 1);

  return 0;
}