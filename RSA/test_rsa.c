/*
Author: Tomas Lovato
Version: 1
Date: 2024/07/21 10:30
Description: full test for RSA (for differenet security levels)
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include "randombytes.c"

#define SHA256LEN 32    // Minima lungehza dell'hashcode - SHA 256
#define SHA512LEN 64    // Massima lunghezza dell0hashcode - SHA 512
#define VERBOSE_LEVEL 0 // 0 = Stampa del file; 1 = Stampa minima; 2 = Stampa delle chiavi
#define KEYGEN_ITERATIONS 5
long unsigned int MLEN = SHA256LEN; // Message Length in Bytes
double INCREMENT = 2;
long unsigned int ITERATIONS = 10;

void print_time_taken(clock_t start, clock_t end, const char *operation) 
{
    double time_taken = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("%s took %f seconds to execute \n", operation, time_taken);
}

static double average_double(double *t, size_t tlen) {
  size_t i;
  double acc=0;

  for(i=0;i<tlen;i++)
    acc += t[i];

  return acc/tlen;
}

void test_rsa(int bits, const char* filename) 
{
    clock_t start, end;
    RSA *keypair = RSA_new();
    BIGNUM *e = BN_new();
    BN_set_word(e, RSA_F4);
    
    double keygen_time[KEYGEN_ITERATIONS];       // Valore dei tempi di keygen
    double signature_time[ITERATIONS];    // Valore dei tempi di firma
    double ok_check_time[ITERATIONS];     // Valore dei tempi di verifica
    long keygen_cycles[KEYGEN_ITERATIONS];
    long signature_cycles[ITERATIONS];
    long ok_check_cycles[ITERATIONS];

    // Apertura file
    FILE *file = fopen(filename, "w");
    // Errore di apertura?
    if (file == NULL) {
        perror("Errore nell'aprire il file");
        return -1;
    }

    // Do key-generation test
    printf("Starting keygen tests: ");
    for(int round = 0; round < KEYGEN_ITERATIONS; round++)
    {        
        printf(" %d,", round);
        fflush(stdout);
        // Key generation
        start = clock();
        RSA_generate_key_ex(keypair, bits, e, NULL);
        end = clock();
        if(VERBOSE_LEVEL >= 2) print_time_taken(start, end, "Key generation");

        // Save private key
        FILE *privkey_file = fopen("private_key.pem", "wb");
        PEM_write_RSAPrivateKey(privkey_file, keypair, NULL, NULL, 0, NULL, NULL);
        fclose(privkey_file);

        // Save public key
        FILE *pubkey_file = fopen("public_key.pem", "wb");
        PEM_write_RSA_PUBKEY(pubkey_file, keypair);
        fclose(pubkey_file);

        // Time management
        keygen_cycles[round] = end - start;
        keygen_time[round] = ((double) (end - start)) / CLOCKS_PER_SEC;
    }

    // Get keys lenght
    int priv_len = i2d_RSAPrivateKey(keypair, NULL);
    int pub_len = i2d_RSA_PUBKEY(keypair, NULL);
	printf("\r\n|MLEN|MTOTLEN|PUBLEN|PRVLEN|SIGLEN|KGTM|SIGTM|CHECKTM|HASHSZ|\r\n");

    // Test over different message sizes
    for (MLEN = SHA256LEN; MLEN <= SHA512LEN; MLEN = (long unsigned int)((double)(MLEN) * INCREMENT)) 
    {
        if(VERBOSE_LEVEL >= 1) printf("=== MESSAGE HASHCODE SIZE: %d", MLEN);
        // Test multiple times
        unsigned int sig_len;
        for(int round = 0; round < ITERATIONS; round++)
        {
            unsigned char *hashcode = malloc(MLEN);
            // Generazione del messaggio --> In questo caso il messaggio è già l'hash del "messaggio originale"
            randombytes(hashcode, MLEN);

            // Sign the message
            unsigned char *sig = malloc(RSA_size(keypair));
            start = clock();
            RSA_sign(NID_sha256, hashcode, MLEN, sig, &sig_len, keypair);
            end = clock();
            if(VERBOSE_LEVEL >= 2) print_time_taken(start, end, "Signing");
            if(VERBOSE_LEVEL >= 2) printf("Signature lenght: %u\r\n", sig_len);

            // Signature Time management
            signature_cycles[round] = end - start;
            signature_time[round] = ((double) (end - start)) / CLOCKS_PER_SEC;

            // Verify the signature
            start = clock();
            int result = RSA_verify(NID_sha256, hashcode, MLEN, sig, sig_len, keypair);
            end = clock();
            if(VERBOSE_LEVEL >= 2) print_time_taken(start, end, "Verification");

            // Validation Time management
            ok_check_cycles[round] = end - start;
            ok_check_time[round] = ((double) (end - start)) / CLOCKS_PER_SEC;

            if (result == 1) {
                if(VERBOSE_LEVEL >= 2) printf("Signature is valid for message size %zu bytes.\n", MLEN);
            } else {
                printf("Signature is invalid for message size %zu bytes.\n", MLEN);
            }

            free(hashcode);
            free(sig);
        }

        // Print result:
        char output_line[512];
        sprintf(output_line, "|%lu|%lu|%d|%d|%d|%f|%f|%f|%lu|\r\n", 
            MLEN, sig_len, pub_len, priv_len, sig_len - MLEN, 
            average_double(keygen_time, KEYGEN_ITERATIONS), 
            average_double(signature_time, ITERATIONS),
            average_double(ok_check_time, ITERATIONS), MLEN);
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

    RSA_free(keypair);
    BN_free(e);
}

int main(int argc, char **argv)
{  
	// Update del fattore di scala dei messaggi:
	if(argc > 5)
	{
		printf("=== INCREMENT: %s - ATTENTION: FORCED TO 2! ===\n", argv[5]);
	}

	// Update delle iterazioni su cui fare media:
	if(argc > 4)
	{
		ITERATIONS = (long unsigned int)atoi(argv[4]);
		printf("=== ITERATIONS: %s ===\n", argv[4]);
	}

	// Apertura del file di output:
	const char *filename1 = "out_rsa_128_hashed";
	const char *filename2 = "out_rsa_192_hashed";
	const char *filename3 = "out_rsa_256_hashed";
	if(argc > 3)
	{
		filename1 = argv[1];
		printf("=== FILE OUTPUT 1: %s ===\n",filename1);
		filename2 = argv[2];
		printf("=== FILE OUTPUT 2: %s ===\n",filename2);
		filename3 = argv[3];
		printf("=== FILE OUTPUT 3: %s ===\n",filename3);
	}

    
    // La stime per i livelli di sicurezza sono variabili. Secondo il NIST:
    // - key da 3072 bit = livello di sicurezza 128 bit di un protocollo a chiave simmetrica come AES128
    // - key da 7680 bit = livello di sicurezza 192 bit di un protocollo a chiave simmetrica come AES192
    // - key da 15360 bit = livello di sicurezza 256 bit di un protocollo a chiave simmetrica come AES256
    int rsa_key_lengths[] = {3072, 7680, 15360};

    // Execute all on normal message
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 128, KEY SIZE: %d ===\r\n", rsa_key_lengths[0]);
    test_rsa(rsa_key_lengths[0], filename1);
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 192, KEY SIZE: %d ===\r\n", rsa_key_lengths[1]);
    test_rsa(rsa_key_lengths[1], filename2);
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 256, KEY SIZE: %d ===\r\n", rsa_key_lengths[2]);
    test_rsa(rsa_key_lengths[2], filename3);

    return 0;
}