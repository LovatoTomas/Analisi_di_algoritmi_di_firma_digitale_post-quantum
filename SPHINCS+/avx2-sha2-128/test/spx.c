/*
Autore: Tomas Lovato
Data: 2024/07/28 15:30
Versione: 2
Descrizione: modifica dei parametri di test
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <openssl/sha.h> // Include OpenSSL for SHA-256 and SHA-512

#include "../api.h"
#include "../params.h"
#include "../randombytes.h"

#define SHA256LEN 32
#define SHA512LEN 64
#define MINMLEN 32 // Minima lunghezza messaggio in bytes
#define MAXMLEN 18000000 // Massima lunghezza messaggio in bytes (circa 18MB)
#define VERBOSE_LEVEL 0 // 0 = Stampa del file; 1 = Stampa minima; 2 = Stampa delle chiavi
long unsigned int MLEN = MINMLEN; // Message Length in Bytes
double INCREMENT = 2;
int ITERATIONS = 100;

void print_time_taken(const char *operation, clock_t start, clock_t end) {
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("%s time: %f seconds\n", operation, time_spent);
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
    int ret = 0;    // Gestione errori delle funzioni di firma e validazione

    // VARS
    unsigned char pk[SPX_PK_BYTES];
    unsigned char sk[SPX_SK_BYTES];
    unsigned char *m;
    unsigned char *sm;
    unsigned char *mout;
    unsigned long long smlen;
    unsigned long long mlen;

    // Apertura file di output
    FILE *file = fopen(filename, "w");
    // Errore di apertura?
    if (file == NULL) {
        perror("Errore nell'aprire il file");
        return -1;
    }

    // Intestazione:
    printf("|MLEN|MTOTLEN|PUBLEN|PRVLEN|SIGLEN|KGTM|SIGTM|CHECKTM|HASHSZ|\r\n");

    // Avvio i test al variare delle dimensioni del messaggio
    for (MLEN = MINMLEN; MLEN <= MAXMLEN; MLEN = (size_t)(MLEN * INCREMENT)) 
    {
        double keygen_time[ITERATIONS];       // Valore dei tempi di keygen
        double signature_time[ITERATIONS];    // Valore dei tempi di firma
        double ok_check_time[ITERATIONS];     // Valore dei tempi di verifica
        long keygen_cycles[ITERATIONS];
        long signature_cycles[ITERATIONS];
        long ok_check_cycles[ITERATIONS];
        uint8_t hash256[SHA256LEN];             // Messaggio sottoposto a hashing 256
        uint8_t hash512[SHA512LEN];             // Messaggio sottoposto a hashing 512

        // Effettuo 10 iterazioni per ogni dimensione e poi faccio la media dei tempi per operazione
        for(int round = 0; round < ITERATIONS; round++)
        {
            // Generazione delle chiavi
            if(VERBOSE_LEVEL >= 2) printf("Generating keypair..\n");
            clock_t start = clock();
            if (crypto_sign_keypair(pk, sk)) {
                printf("failed!\n");
                return -1;
            }
            clock_t end = clock();
            if(VERBOSE_LEVEL >= 1) print_time_taken("Key pair generation", start, end);
            // Gestione tempo keygen
            keygen_cycles[round] = end - start;
            keygen_time[round] = (double)(keygen_cycles[round]) / CLOCKS_PER_SEC;
       
            if(sha512 && MLEN < SHA512LEN)
            {
                m = malloc(SHA512LEN);
                sm = malloc(SPX_BYTES + SHA512LEN);
                mout = malloc(SPX_BYTES + SHA512LEN);
            }
            else
            {
                m = malloc(MLEN);
                sm = malloc(SPX_BYTES + MLEN);
                mout = malloc(SPX_BYTES + MLEN);
            }
            // Generazione di un messaggio random     
            randombytes(m, MLEN);
            // Calcolo HASH SHA256 del messaggio:
            SHA256(m, MLEN, hash256);
            // Calcolo HASH SHA512 del messaggio:
            SHA512(m, MLEN, hash512);

            // Firma del messaggio
            if(VERBOSE_LEVEL >= 2) printf("Testing signature with message length %zu bytes..\n", MLEN);
            if(sha256)
            {
                // Messaggio con hash256
                start = clock();
                crypto_sign(sm, &smlen, hash256, SHA256LEN, sk);
                end = clock();
            }
            else if(sha512)
            {
                // Messaggio con hash512
                start = clock();
                crypto_sign(sm, &smlen, hash512, SHA512LEN, sk);
                end = clock();
            }
            else
            {
                // Messaggio senza hash
                start = clock();
                crypto_sign(sm, &smlen, m, MLEN, sk);
                end = clock();
            }
            if(VERBOSE_LEVEL >= 1) print_time_taken("Signing", start, end);
            // Gestione tempo firma
            signature_cycles[round] = end - start;
            signature_time[round] = (double)(signature_cycles[round]) / CLOCKS_PER_SEC;

            // Verifca della firma del messaggio
            start = clock();
            if (crypto_sign_open(mout, &mlen, sm, smlen, pk)) {
                printf("  X verification failed!\n");
                ret = -1;
            } else if(VERBOSE_LEVEL >= 2){
                printf("  Verification succeeded.\n");
            }
            end = clock();
            if(VERBOSE_LEVEL >= 1) print_time_taken("Verification", start, end);
            // Gestione tempo verifica
            ok_check_cycles[round] = end - start;
            ok_check_time[round] = (double)(ok_check_cycles[round]) / CLOCKS_PER_SEC;

            /* Test if the correct message was recovered. */
            if ( (!sha256 && !sha512 && mlen != MLEN) || 
                (sha256 && mlen != SHA256LEN) || 
                (sha512 && mlen != SHA512LEN) ) {
                printf("  X mlen incorrect [%llu != %zu]!\n", mlen, MLEN);
                ret = -1;
            } else  if(VERBOSE_LEVEL >= 2){
                printf("  mlen as expected [%llu].\n", mlen);
            }
            if ( (!sha256 && !sha512 && memcmp(m, mout, MLEN)) || 
                (sha256 && memcmp(hash256, mout, SHA256LEN)) || 
                (sha512 && memcmp(hash512, mout, SHA512LEN)) ) {
                printf("  X output message incorrect!\n");
                ret = -1;
            } else if(VERBOSE_LEVEL >= 2){
                printf("  Output message as expected.\n");
            }

            // Libero la memoria
            free(m);
            free(sm);
            free(mout);
        }      
        
        // Calcolo delle medie:
        double keygen_average_time = average_double(keygen_time, ITERATIONS);
        double signature_average_time = average_double(signature_time, ITERATIONS);
        double validation_average_time = average_double(ok_check_time, ITERATIONS);
        if(VERBOSE_LEVEL >= 1)
        {
            fprintf(stderr, "=== MLEN=%lu | AVG_KG=%f | AVG_SIGN=%f | AVG_VAL=%f ===\n", MLEN, keygen_average_time, signature_average_time, validation_average_time);
        }

        // Stampa risultato finale:     
        long long unsigned int diff = smlen - MLEN;
        if(sha256) diff = smlen - SHA256LEN;
        if(sha512) diff = smlen - SHA512LEN;
        char output_line[512];
        sprintf(output_line, "|%lu|%llu|%u|%u|%llu|%f|%f|%f|%llu|\r\n",
                MLEN, smlen, SPX_PK_BYTES, SPX_SK_BYTES, diff,
                keygen_average_time, signature_average_time, validation_average_time, mlen);
        printf("%s",output_line);
        // Scrittura nel file
        if (fprintf(file, "%s", output_line) < 0) 
        {
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

    // Return dell'errore o codice OK
    return ret;
}

int main(int argc, char *argv[]) 
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
	const char *filename1 = "out_sphincs+";
	const char *filename2 = "out_sphincs+_sha256";
	const char *filename3 = "out_sphincs+_sha512";
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
    int ret = loop(filename1, 0, 0);
    // Execute all on hash (sha256)
    ret += loop(filename2, 1, 0);
    // Execute all on hash (sha512)
    ret += loop(filename3, 0, 1);

    return ret;
}
