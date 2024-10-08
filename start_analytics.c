/*
Autore: Tomas Lovato
Data: 2024/07/20 17:30
Descrizione: raccoglie i dati di tutti gli algoritmi richiamando gli algoritmi di test
*/

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int dilithium_do = 1;
    int falcon_do = 1;
    int sphincs_do = 1;
    int rsa_do = 1;
    int phyton_do = 1;
    if(argc > 5)
    {
        printf("=== PARAMETERS: %s %s %s %s %s ===\n", argv[1], argv[2], argv[3], argv[4], argv[5]);
        dilithium_do = atoi(argv[1]);
        falcon_do = atoi(argv[2]);
        sphincs_do = atoi(argv[3]);
        rsa_do = atoi(argv[4]);
        phyton_do = atoi(argv[5]);
    }

    if(dilithium_do)
    {
        // REF DILITHIUM
        system("make -C ./CRYSTALS-dilithium/ref/");
        // SCRIPT + NUMEFILE1NOSHA + NOMEFILE2SHA256 + NOMEFILE3SHA512 + NUM ITER + INCREMENT
        system("./CRYSTALS-dilithium/ref/test/test_dilithium2 ./output/dilithium2_ref ./output/dilithium2_sha256_ref ./output/dilithium2_sha512_ref 100 2");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium3 ./output/dilithium3_ref ./output/dilithium3_sha256_ref ./output/dilithium3_sha512_ref 100 2");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium5 ./output/dilithium5_ref ./output/dilithium5_sha256_ref ./output/dilithium5_sha512_ref 100 2");

        // AVX2 DILITHIUM
        system("make -C ./CRYSTALS-dilithium/avx2/");
        // SCRIPT + NUMEFILE1NOSHA + NOMEFILE2SHA256 + NOMEFILE3SHA512 + NUM ITER + INCREMENT
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium2 ./output/dilithium2_avx2 ./output/dilithium2_sha256_avx2 ./output/dilithium2_sha512_avx2 100 2");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium3 ./output/dilithium3_avx2 ./output/dilithium3_sha256_avx2 ./output/dilithium3_sha512_avx2 100 2");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium5 ./output/dilithium5_avx2 ./output/dilithium5_sha256_avx2 ./output/dilithium5_sha512_avx2 100 2");
    }

    if(falcon_do)
    {
        // REF FALCON
        system("make -C ./FALCON/ref/");
        // SCRIPT + NOMEFILE1 + NOMEFILE2 + NUM ITER + INCREMENT
        system("./FALCON/ref/test_falcon_msg ./output/falcon2_ref ./output/falcon5_ref 100 2");
        system("./FALCON/ref/test_falcon_sha256 ./output/falcon2_ref_sha256 ./output/falcon5_ref_sha256 100 2");
        system("./FALCON/ref/test_falcon_sha512 ./output/falcon2_ref_sha512 ./output/falcon5_ref_sha512 100 2");

        // AVX2 FALCON
        system("make -C ./FALCON/avx2/");
        // SCRIPT + NOMEFILE1 + NOMEFILE2 + NUM ITER + INCREMENT
        system("./FALCON/avx2/test_falcon_msg ./output/falcon2_avx2 ./output/falcon5_avx2 100 2");
        system("./FALCON/avx2/test_falcon_sha256 ./output/falcon2_avx2_sha256 ./output/falcon5_avx2_sha256 100 2");
        system("./FALCON/avx2/test_falcon_sha512 ./output/falcon2_avx2_sha512 ./output/falcon5_avx2_sha512 100 2");
    }

    if(sphincs_do)
    {
        // REF SPHINCS
        system("make -C ./SPHINCS+/ref-sha2-128/ all");
        system("make -C ./SPHINCS+/ref-sha2-192/ all");
        system("make -C ./SPHINCS+/ref-sha2-256/ all");
        // SCRIPT + NUMEFILE1NOSHA + NOMEFILE2SHA256 + NOMEFILE3SHA512 + NUM ITER + INCREMENT
        system("./SPHINCS+/ref-sha2-128/test/spx ./output/sphincs128_ref ./output/sphincs128_sha256_ref ./output/sphincs128_sha512_ref 100 2");
        system("./SPHINCS+/ref-sha2-192/test/spx ./output/sphincs192_ref ./output/sphincs192_sha256_ref ./output/sphincs192_sha512_ref 100 2");
        system("./SPHINCS+/ref-sha2-256/test/spx ./output/sphincs256_ref ./output/sphincs256_sha256_ref ./output/sphincs256_sha512_ref 100 2");

        // AVX2 SPHINCS
        system("make -C ./SPHINCS+/avx2-sha2-128/ all");
        system("make -C ./SPHINCS+/avx2-sha2-192/ all");
        system("make -C ./SPHINCS+/avx2-sha2-256/ all");
        // SCRIPT + NUMEFILE1NOSHA + NOMEFILE2SHA256 + NOMEFILE3SHA512 + NUM ITER + INCREMENT
        system("./SPHINCS+/avx2-sha2-128/test/spx ./output/sphincs128_avx2 ./output/sphincs128_sha256_avx2 ./output/sphincs128_sha512_avx2 100 2");
        system("./SPHINCS+/avx2-sha2-192/test/spx ./output/sphincs192_avx2 ./output/sphincs192_sha256_avx2 ./output/sphincs192_sha512_avx2 100 2");
        system("./SPHINCS+/avx2-sha2-256/test/spx ./output/sphincs256_avx2 ./output/sphincs256_sha256_avx2 ./output/sphincs256_sha512_avx2 100 2");
    }

    if(rsa_do)
    {
        // CLASSIC RSA
        system("gcc ./RSA/test_rsa.c -o ./RSA/test_rsa -lcrypto");
        // SCRIPT + RSA80SHA256 + RSA80SHA512 + RSA112SHA256 + RSA112SHA512 + RSA128SHA256 + RSA128SHA512 + RSA192SHA256 + RSA192SHA512 + RSA256SHA256 + RSA256SHA512 + NUM ITER + INCREMENT
        system("./RSA/test_rsa ./output/rsa_80_sha256 ./output/rsa_80_sha512 ./output/rsa_112_sha256 ./output/rsa_112_sha512 ./output/rsa_128_sha256 ./output/rsa_128_sha512 ./output/rsa_192_sha256 ./output/rsa_192_sha512 ./output/rsa_256_sha256 ./output/rsa_256_sha512 100 2");
    }

    if(phyton_do)
        // PYTHON ANALYTICS
        system("python3 start_performancegraphs.py");

    // Per eseguire un comando sulla stessa shell
    // execl("/bin/sh", "sh", "-c", "./SPHINCS+/ref-sha2-128/test/spx ./output/sphincs128_ref ./output/sphincs128_sha256_ref ./output/sphincs128_sha512_ref 100 2", NULL);
}