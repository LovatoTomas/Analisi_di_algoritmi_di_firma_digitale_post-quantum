/*
Author: Tomas Lovato
Version: 2
Date: 2024/07/28 15:30
Description: modifica dei parametri di test
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <openssl/sha.h> // Include OpenSSL for SHA-256
#include "falcon.h"
#include "randombytes.h"

#define SHALEN 64
#define MINMLEN 32 // Minima lunghezza messaggio in bytes
#define MAXMLEN 18000000 // Massima lunghezza messaggio in bytes (circa 18MB)
int INCREMENT = 2;
int ITERATIONS = 100;
long unsigned int MLEN = MINMLEN; // Message Length in Bytes
FILE *file; // File di output

static void * xmalloc(size_t len)
{
	void *buf;

	if (len == 0) {
		return NULL;
	}
	buf = malloc(len);
	if (buf == NULL) {
		fprintf(stderr, "memory allocation error\n");
		exit(EXIT_FAILURE);
	}
	return buf;
}

static void xfree(void *buf)
{
	if (buf != NULL) {
		free(buf);
	}
}

/*
 * Benchmark function takes an opaque context and an iteration count;
 * it returns 0 on success, a negative error code on error.
 */
typedef int (*bench_fun)(void *ctx, unsigned long num);

/*
 * Returned value is the time per iteration in nanoseconds. If the
 * benchmark function reports an error, 0.0 is returned.
 */
static double do_bench(bench_fun bf, void *ctx, unsigned int iterations) {
    unsigned long num;
    double total_time = 0.0;
    int r;

    for (unsigned int i = 0; i < iterations; i++) {
        clock_t begin, end;
        double tt;

        begin = clock();
        r = bf(ctx, 1); // Execute the benchmark function once per iteration
        end = clock();
        if (r != 0) {
            fprintf(stderr, "ERR: %d\n", r);
            return 0.0;
        }
        tt = (double)(end - begin) / (double)CLOCKS_PER_SEC;
        total_time += tt;
    }

    return (total_time / (double)iterations) * 1000000000.0; // Convert to microseconds for consistency
}

typedef struct {
	unsigned logn;
	shake256_context rng;
	uint8_t *tmp;
	size_t tmp_len;
	uint8_t *pk;
	uint8_t *sk;
	uint8_t *esk;
	uint8_t *sig;
	size_t sig_len;
	uint8_t *sigct;
	size_t sigct_len;
	size_t msg_len; 			// Aggiunto per gestire la lunghezza del messaggio variabile
    uint8_t *msg;				// Pointer al messaggio generato
    uint8_t hash[SHALEN]; 	// Hash del messaggio da 32 bytes tramite SHA-256
} bench_context;

static inline size_t maxsz(size_t a, size_t b)
{
	return a > b ? a : b;
}

#define CC(x)   do { \
		int ccr = (x); \
		if (ccr != 0) { \
			return ccr; \
		} \
	} while (0)

static int bench_keygen(void *ctx, unsigned long num)
{
	bench_context *bc;

	bc = ctx;
	while (num -- > 0) {
		CC(falcon_keygen_make(&bc->rng, bc->logn,
			bc->sk, FALCON_PRIVKEY_SIZE(bc->logn),
			bc->pk, FALCON_PUBKEY_SIZE(bc->logn),
			bc->tmp, bc->tmp_len));
	}
	return 0;
}

static int bench_sign_dyn(void *ctx, unsigned long num)
{
	bench_context *bc;

	bc = ctx;
	while (num -- > 0) {
		bc->sig_len = FALCON_SIG_COMPRESSED_MAXSIZE(bc->logn);
		CC(falcon_sign_dyn(&bc->rng,
			bc->sig, &bc->sig_len, FALCON_SIG_COMPRESSED,
			bc->sk, FALCON_PRIVKEY_SIZE(bc->logn),
			bc->hash, SHALEN, bc->tmp, bc->tmp_len)); // Aggiunto il riferimento all'hash messaggio variabile
	}
	return 0;
}

static int bench_sign_dyn_ct(void *ctx, unsigned long num)
{
	bench_context *bc;

	bc = ctx;
	while (num -- > 0) {
		bc->sigct_len = FALCON_SIG_CT_SIZE(bc->logn);
		CC(falcon_sign_dyn(&bc->rng,
			bc->sigct, &bc->sigct_len, FALCON_SIG_CT,
			bc->sk, FALCON_PRIVKEY_SIZE(bc->logn),
			bc->hash, SHALEN, bc->tmp, bc->tmp_len)); // Aggiunto il riferimento all'hash messaggio variabile
	}
	return 0;
}

static int bench_expand_privkey(void *ctx, unsigned long num)
{
	bench_context *bc;

	bc = ctx;
	while (num -- > 0) {
		CC(falcon_expand_privkey(
			bc->esk, FALCON_EXPANDEDKEY_SIZE(bc->logn),
			bc->sk, FALCON_PRIVKEY_SIZE(bc->logn),
			bc->tmp, bc->tmp_len));
	}
	return 0;
}

static int bench_sign_tree(void *ctx, unsigned long num)
{
	bench_context *bc;

	bc = ctx;
	while (num -- > 0) {
		bc->sig_len = FALCON_SIG_COMPRESSED_MAXSIZE(bc->logn);
		CC(falcon_sign_tree(&bc->rng,
			bc->sig, &bc->sig_len, FALCON_SIG_COMPRESSED,
			bc->esk,
			bc->hash, SHALEN, bc->tmp, bc->tmp_len)); // Aggiunto il riferimento all'hash messaggio variabile
	}
	return 0;
}

static int bench_sign_tree_ct(void *ctx, unsigned long num)
{
	bench_context *bc;

	bc = ctx;
	while (num -- > 0) {
		bc->sigct_len = FALCON_SIG_CT_SIZE(bc->logn);
		CC(falcon_sign_tree(&bc->rng,
			bc->sigct, &bc->sigct_len, FALCON_SIG_CT,
			bc->esk,
			bc->hash, SHALEN, bc->tmp, bc->tmp_len)); // Aggiunto il riferimento all'hash messaggio variabile
	}
	return 0;
}

static int bench_verify(void *ctx, unsigned long num)
{
	bench_context *bc;
	size_t pk_len;

	bc = ctx;
	pk_len = FALCON_PUBKEY_SIZE(bc->logn);
	while (num -- > 0) {
		CC(falcon_verify(
			bc->sig, bc->sig_len, FALCON_SIG_COMPRESSED,
			bc->pk, pk_len,
			bc->hash, SHALEN, bc->tmp, bc->tmp_len)); // Aggiunto il riferimento all'hash messaggio variabile
	}
	return 0;
}

static int bench_verify_ct(void *ctx, unsigned long num)
{
	bench_context *bc;
	size_t pk_len;

	bc = ctx;
	pk_len = FALCON_PUBKEY_SIZE(bc->logn);
	while (num -- > 0) {
		CC(falcon_verify(
			bc->sigct, bc->sigct_len, FALCON_SIG_CT,
			bc->pk, pk_len,
			bc->hash, SHALEN, bc->tmp, bc->tmp_len)); // Aggiunto il riferimento all'hash messaggio variabile
	}
	return 0;
}

static void test_speed_falcon(unsigned logn, double threshold, size_t msg_len)
{
	bench_context bc;
	size_t len;

	printf("%4u:", 1u << logn);
	fflush(stdout);

	bc.logn = logn;
	// Questo IF si assicura che l'OS sia in grado di generare numeri 
	// veramente casuali. Questi saranno usati durante il keygen e la firma.
	// Ad esempio nella firma permette di generare firme uniche ogni volta
	// che lo stesso messaggio viene firmato.
	// Il numero casuale usato per la firma farà parte della firma, dunque durante
	// la verifica "sarà possibile estrapolarlo" per convalidare il messaggio.
	// Non è esattamente il numero casuale a essere memorizzato nella firma ma delle
	// informazioni aggiuntive che permettono di procedere nonostante il cambio
	// firma a parità di file e chiavi.
	if (shake256_init_prng_from_system(&bc.rng) != 0) {
		fprintf(stderr, "random seeding failed\n");
		exit(EXIT_FAILURE);
	}
	len = FALCON_TMPSIZE_KEYGEN(logn);
	len = maxsz(len, FALCON_TMPSIZE_SIGNDYN(logn));
	len = maxsz(len, FALCON_TMPSIZE_SIGNTREE(logn));
	len = maxsz(len, FALCON_TMPSIZE_EXPANDPRIV(logn));
	len = maxsz(len, FALCON_TMPSIZE_VERIFY(logn));
	bc.tmp = xmalloc(len);
	bc.tmp_len = len;
	bc.pk = xmalloc(FALCON_PUBKEY_SIZE(logn));
	bc.sk = xmalloc(FALCON_PRIVKEY_SIZE(logn));
	bc.esk = xmalloc(FALCON_EXPANDEDKEY_SIZE(logn));
	bc.sig = xmalloc(FALCON_SIG_COMPRESSED_MAXSIZE(logn));
	bc.sig_len = 0;
	bc.sigct = xmalloc(FALCON_SIG_CT_SIZE(logn));
	bc.sigct_len = 0;
    bc.msg_len = msg_len;
    bc.msg = xmalloc(msg_len);

	// Genero il messaggio
	randombytes(bc.msg, bc.msg_len);
	// Calcolo HASH SHA512 del messaggio:
	SHA512(bc.msg, bc.msg_len, bc.hash);

	double kg = do_bench(&bench_keygen, &bc, threshold) / 1000000000.0;
	double ek = do_bench(&bench_expand_privkey, &bc, threshold) / 1000000000.0;
	double sd = do_bench(&bench_sign_dyn, &bc, threshold) / 1000000000.0;
	double sdc = do_bench(&bench_sign_dyn_ct, &bc, threshold) / 1000000000.0;
	double st = do_bench(&bench_sign_tree, &bc, threshold) / 1000000000.0;
	double stc = do_bench(&bench_sign_tree_ct, &bc, threshold) / 1000000000.0;
	double vv = do_bench(&bench_verify, &bc, threshold) / 1000000000.0;
	double vvc = do_bench(&bench_verify_ct, &bc, threshold) / 1000000000.0;

    char output_line[512];
	sprintf(output_line, "|%zu|%zu|%u|%u|%zu|%f|%f|%f|%d|\r\n",
		bc.msg_len, bc.msg_len + bc.sig_len, FALCON_PUBKEY_SIZE(bc.logn),
		FALCON_PRIVKEY_SIZE(bc.logn), bc.sig_len, kg, sdc, vvc, SHALEN);
	printf("%s", output_line);
	// Scrittura nel file
    if (fprintf(file, "%s", output_line) < 0) {
      perror("Errore nella scrittura del file");
    }

	xfree(bc.tmp);
	xfree(bc.pk);
	xfree(bc.sk);
	xfree(bc.esk);
	xfree(bc.sig);
	xfree(bc.sigct);
	xfree(bc.msg); // Libero il buffer del messaggio
}

int
main(int argc, char *argv[])
{
	// Update del fattore di scala dei messaggi:
	if(argc > 4)
	{
		INCREMENT = atoi(argv[4]);
		printf("=== INCREMENT: %s ===\n", argv[4]);
	}

	// Update delle iterazioni su cui fare media:
	if(argc > 3)
	{
		ITERATIONS = atoi(argv[3]);
		printf("=== ITERATIONS: %s ===\n", argv[3]);
	}

	// Apertura del file di output:
	const char *filename1 = "out_falcon2_sha512";
	const char *filename2 = "out_falcon5_sha512";
	if(argc > 2)
	{
		filename1 = argv[1];
		printf("=== FILE OUTPUT 1: %s ===\n",filename1);
		filename2 = argv[2];
		printf("=== FILE OUTPUT 2: %s ===\n",filename2);
	}
	
	// Apertura del file
	file = fopen(filename1, "w");
	// Errore di apertura?
	if (file == NULL) {
		perror("Errore nell'aprire il file");
		return -1;
	}
	printf("|MLEN|MTOTLEN|PUBLEN|PRVLEN|SIGLEN|KGTM|SIGTM|CHECKTM|HASHSZ|\r\n");
	for(MLEN = MINMLEN; MLEN < MAXMLEN; MLEN = MLEN * INCREMENT) 
	{
		test_speed_falcon(9, ITERATIONS, MLEN); 
		// 9 --> 2^9 = 256 bit di chiave --> equivale a un livello di sicurezza classico a 128bit
	}
	// Chiusura del file:
	if (fclose(file) != 0) {
		perror("Errore nella chiusura del file");
		return -1;
	}

	// Apertura del file
	file = fopen(filename2, "w");
	// Errore di apertura?
	if (file == NULL) {
		perror("Errore nell'aprire il file");
		return -1;
	}
	printf("|MLEN|MTOTLEN|PUBLEN|PRVLEN|SIGLEN|KGTM|SIGTM|CHECKTM|HASHSZ|\r\n");
	for(MLEN = MINMLEN; MLEN < MAXMLEN; MLEN = MLEN * INCREMENT) 
	{
		test_speed_falcon(10, ITERATIONS, MLEN); 
		// 10 --> 2^10 = 512 bit di chiave --> equivale a un livello di sicurezza classico a 256bit
	}
	// Chiusura del file:
	if (fclose(file) != 0) {
		perror("Errore nella chiusura del file");
		return -1;
	}

	// Chiusura
	return 0;
}