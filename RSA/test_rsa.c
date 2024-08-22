/*
Author: Tomas Lovato
Version: 2
Date: 2024/07/28 16:30
Description: Modificato con lo standard di output delle altre prove
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <openssl/sha.h>
#include "randombytes.c"

#define SHA256LEN 32    // Minima lunghezza dell'hashcode - SHA 256
#define SHA512LEN 64    // Massima lunghezza dell'hashcode - SHA 512
#define MINMLEN 32      // Minima lunghezza messaggio in bytes
#define MAXMLEN 18000000 // Massima lunghezza messaggio in bytes (circa 18MB)
#define VERBOSE_LEVEL 0 // 0 = Stampa del file; 1 = Stampa minima; 2 = Stampa delle chiavi
#define KEYGEN_ITERATIONS 20
long unsigned int MLEN = SHA256LEN; // Message Length in Bytes
double INCREMENT = 2;
long unsigned int ITERATIONS = 100;

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

void test_rsa(int bits, const char* filename1, const char* filename2) 
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
    FILE *file1 = fopen(filename1, "w");
    // Errore di apertura?
    if (file1 == NULL) {
        perror("Errore nell'aprire il file");
        return;
    }

    // Apertura file
    FILE *file2 = fopen(filename2, "w");
    // Errore di apertura?
    if (file2 == NULL) {
        perror("Errore nell'aprire il file");
        fclose(file1);
        return;
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

    // Get keys length
    int priv_len = i2d_RSAPrivateKey(keypair, NULL);
    int pub_len = i2d_RSA_PUBKEY(keypair, NULL);
    printf("\r\n|MLEN|MTOTLEN|PUBLEN|PRVLEN|SIGLEN|KGTM|SIGTM|CHECKTM|HASHSZ|\r\n");

    // Test over different message sizes with SHA256
    for (MLEN = MINMLEN; MLEN <= MAXMLEN; MLEN = (long unsigned int)((double)(MLEN) * INCREMENT)) 
    {
        if(VERBOSE_LEVEL >= 1) printf("=== MESSAGE HASHCODE SIZE: %lu", MLEN);
        // Test multiple times
        unsigned int sig_len;
        for(int round = 0; round < ITERATIONS; round++)
        {
            unsigned char *message = malloc(MLEN);
            unsigned char *hashcode = malloc(SHA256LEN);
            // Generazione del messaggio casuale
            randombytes(message, MLEN);

            // Calcolo dell'hash del messaggio
            SHA256(message, MLEN, hashcode);

            // Sign the message
            unsigned char *sig = malloc(RSA_size(keypair));
            start = clock();
            RSA_sign(NID_sha256, hashcode, SHA256LEN, sig, &sig_len, keypair);
            end = clock();
            if(VERBOSE_LEVEL >= 2) print_time_taken(start, end, "Signing");
            if(VERBOSE_LEVEL >= 2) printf("Signature length: %u\r\n", sig_len);

            // Signature Time management
            signature_cycles[round] = end - start;
            signature_time[round] = ((double) (end - start)) / CLOCKS_PER_SEC;

            // Verify the signature
            start = clock();
            int result = RSA_verify(NID_sha256, hashcode, SHA256LEN, sig, sig_len, keypair);
            end = clock();
            if(VERBOSE_LEVEL >= 2) print_time_taken(start, end, "Verification");

            // Validation Time management
            ok_check_cycles[round] = end - start;
            ok_check_time[round] = ((double) (end - start)) / CLOCKS_PER_SEC;

            if (result == 1) {
                if(VERBOSE_LEVEL >= 2) printf("Signature is valid for message size %lu bytes.\n", MLEN);
            } else {
                printf("Signature is invalid for message size %lu bytes.\n", MLEN);
            }

            free(message);
            free(sig);
        }

        // Print result:
        char output_line[512];
        sprintf(output_line, "|%lu|%u|%d|%d|%d|%f|%f|%f|%d|\r\n", 
            MLEN, sig_len, pub_len, priv_len, sig_len - SHA256LEN, 
            average_double(keygen_time, KEYGEN_ITERATIONS), 
            average_double(signature_time, ITERATIONS),
            average_double(ok_check_time, ITERATIONS), SHA256LEN);
        printf("%s", output_line);

        // Scrittura nel file
        if (fprintf(file1, "%s", output_line) < 0) {
            perror("Errore nella scrittura del file");
            fclose(file1);
            fclose(file2);
            return;
        }
    }

    printf("\r\n|MLEN|MTOTLEN|PUBLEN|PRVLEN|SIGLEN|KGTM|SIGTM|CHECKTM|HASHSZ|\r\n");

    // Test over different message sizes with SHA512
    for (MLEN = MINMLEN; MLEN <= MAXMLEN; MLEN = (long unsigned int)((double)(MLEN) * INCREMENT)) 
    {
        if(VERBOSE_LEVEL >= 1) printf("=== MESSAGE HASHCODE SIZE: %lu", MLEN);
        // Test multiple times
        unsigned int sig_len;
        for(int round = 0; round < ITERATIONS; round++)
        {
            unsigned char *message = malloc(MLEN);
            unsigned char *hashcode = malloc(SHA512LEN);
            // Generazione del messaggio casuale
            randombytes(message, MLEN);

            // Calcolo dell'hash del messaggio
            SHA512(message, MLEN, hashcode);

            // Sign the message
            unsigned char *sig = malloc(RSA_size(keypair));
            start = clock();
            RSA_sign(NID_sha512, hashcode, SHA512LEN, sig, &sig_len, keypair);
            end = clock();
            if(VERBOSE_LEVEL >= 2) print_time_taken(start, end, "Signing");
            if(VERBOSE_LEVEL >= 2) printf("Signature length: %u\r\n", sig_len);

            // Signature Time management
            signature_cycles[round] = end - start;
            signature_time[round] = ((double) (end - start)) / CLOCKS_PER_SEC;

            // Verify the signature
            start = clock();
            int result = RSA_verify(NID_sha512, hashcode, SHA512LEN, sig, sig_len, keypair);
            end = clock();
            if(VERBOSE_LEVEL >= 2) print_time_taken(start, end, "Verification");

            // Validation Time management
            ok_check_cycles[round] = end - start;
            ok_check_time[round] = ((double) (end - start)) / CLOCKS_PER_SEC;

            if (result == 1) {
                if(VERBOSE_LEVEL >= 2) printf("Signature is valid for message size %lu bytes.\n", MLEN);
            } else {
                printf("Signature is invalid for message size %lu bytes.\n", MLEN);
            }

            free(message);
            free(sig);
        }

        // Print result:
        char output_line[512];
        sprintf(output_line, "|%lu|%u|%d|%d|%d|%f|%f|%f|%d|\r\n", 
            MLEN, sig_len, pub_len, priv_len, sig_len - SHA512LEN, 
            average_double(keygen_time, KEYGEN_ITERATIONS), 
            average_double(signature_time, ITERATIONS),
            average_double(ok_check_time, ITERATIONS), SHA512LEN);
        printf("%s", output_line);

        // Scrittura nel file
        if (fprintf(file2, "%s", output_line) < 0) {
            perror("Errore nella scrittura del file");
            fclose(file1);
            fclose(file2);
            return;
        }
    }

    // Chiusura del file:
    if (fclose(file1) != 0) {
        perror("Errore nella chiusura del file");
        fclose(file2);
        return;
    }

    // Chiusura del file:
    if (fclose(file2) != 0) {
        perror("Errore nella chiusura del file");
        return;
    }

    RSA_free(keypair);
    BN_free(e);
}

int main(int argc, char **argv)
{  
    // Update del fattore di scala dei messaggi:
    if(argc > 8)
    {
        printf("=== INCREMENT: %s - ATTENTION: FORCED TO 2! ===\n", argv[8]);
    }

    // Update delle iterazioni su cui fare media:
    if(argc > 7)
    {
        ITERATIONS = (long unsigned int)atoi(argv[7]);
        printf("=== ITERATIONS: %s ===\n", argv[7]);
    }

    // Apertura del file di output:
    const char *filename1 = "out_rsa_80_sha256";
    const char *filename2 = "out_rsa_80_sha512";
    const char *filename3 = "out_rsa_112_sha256";
    const char *filename4 = "out_rsa_112_sha512";
    const char *filename5 = "out_rsa_128_sha256";
    const char *filename6 = "out_rsa_128_sha512";
    const char *filename7 = "out_rsa_192_sha256";
    const char *filename8 = "out_rsa_192_sha512";
    const char *filename9 = "out_rsa_256_sha256";
    const char *filename10 = "out_rsa_256_sha512";
    if(argc > 10)
    {
        filename1 = argv[1];
        printf("=== FILE OUTPUT 1: %s ===\n",filename1);
        filename2 = argv[2];
        printf("=== FILE OUTPUT 2: %s ===\n",filename2);
        filename3 = argv[3];
        printf("=== FILE OUTPUT 3: %s ===\n",filename3);
        filename4 = argv[4];
        printf("=== FILE OUTPUT 4: %s ===\n",filename4);
        filename5 = argv[5];
        printf("=== FILE OUTPUT 5: %s ===\n",filename5);
        filename6 = argv[6];
        printf("=== FILE OUTPUT 6: %s ===\n",filename6);
        filename7 = argv[7];
        printf("=== FILE OUTPUT 7: %s ===\n",filename7);
        filename8 = argv[8];
        printf("=== FILE OUTPUT 8: %s ===\n",filename8);
        filename9 = argv[9];
        printf("=== FILE OUTPUT 9: %s ===\n",filename9);
        filename10 = argv[10];
        printf("=== FILE OUTPUT 10: %s ===\n",filename10);
    }

    
    // La stime per i livelli di sicurezza sono variabili. Secondo il NIST:
    // - key da 1024 bit = livello di sicurezza 80 bit di un protocollo a chiave simmetrica con 80bit di chiave simmetrica
    // - key da 2048 bit = livello di sicurezza 112 bit di un protocollo a chiave simmetrica con 112bit di chiave simmetrica
    // - key da 3072 bit = livello di sicurezza 128 bit di un protocollo a chiave simmetrica come AES128
    // - key da 7680 bit = livello di sicurezza 192 bit di un protocollo a chiave simmetrica come AES192
    // - key da 15360 bit = livello di sicurezza 256 bit di un protocollo a chiave simmetrica come AES256
    int rsa_key_lengths[] = {1024, 2048, 3072, 7680, 15360};

    // Execute all on normal message
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 80, KEY SIZE: %d ===\r\n", rsa_key_lengths[0]);
    test_rsa(rsa_key_lengths[0], filename1, filename2);
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 112, KEY SIZE: %d ===\r\n", rsa_key_lengths[1]);
    test_rsa(rsa_key_lengths[1], filename3, filename4);
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 128, KEY SIZE: %d ===\r\n", rsa_key_lengths[2]);
    test_rsa(rsa_key_lengths[2], filename5, filename6);
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 192, KEY SIZE: %d ===\r\n", rsa_key_lengths[3]);
    test_rsa(rsa_key_lengths[3], filename7, filename8);
    if(VERBOSE_LEVEL >= 1) printf("=== TEST LEVEL 256, KEY SIZE: %d ===\r\n", rsa_key_lengths[4]);
    test_rsa(rsa_key_lengths[4], filename9, filename10);

    return 0;
}
