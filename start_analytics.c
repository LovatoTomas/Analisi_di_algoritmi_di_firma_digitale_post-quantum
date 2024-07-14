/*
Autore: Tomas Lovato
Data: 2024/07/13 21:30
Descrizione: raccoglie i dati di tutti gli algoritmi richiamando gli algoritmi di test
*/

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    // ENVIRONEMNT
    system("ulimit -s 524288");

    int dilithium_do = 1;
    int falcon_do = 1;
    int phyton_do = 1;
    if(argc > 3)
    {
        printf("=== PARAMETERS: %s %s %s ===\n", argv[1], argv[2], argv[3]);
        dilithium_do = atoi(argv[1]);
        falcon_do = atoi(argv[2]);
        phyton_do = atoi(argv[3]);
    }

    if(dilithium_do)
    {
        // REF DILITHIUM
        system("make -C ./CRYSTALS-dilithium/ref/");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium2 20240713_output_dilithium2.txt");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium2aes 20240713_output_dilithium2aes.txt");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium3 20240713_output_dilithium3.txt");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium3 20240713_output_dilithium3aes.txt");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium5 20240713_output_dilithium5.txt");
        system("./CRYSTALS-dilithium/ref/test/test_dilithium5 20240713_output_dilithium5aes.txt");

        // AVX2 DILITHIUM
        system("make -C ./CRYSTALS-dilithium/avx2/");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium2 20240713_output_dilithium2.txt");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium2aes 20240713_output_dilithium2aes.txt");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium3 20240713_output_dilithium3.txt");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium3 20240713_output_dilithium3aes.txt");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium5 20240713_output_dilithium5.txt");
        system("./CRYSTALS-dilithium/avx2/test/test_dilithium5 20240713_output_dilithium5aes.txt");
    }

    if(falcon_do)
    {
        // REF FALCON
        system("make -C ./FALCON/ref/");
        // SCRIPT + NOMEFILE1 + NOMEFILE2 + NUM ITER + INCREMENT
        system("./FALCON/ref/test_falcon_msg ./output/falcon2_ref ./output/falcon5_ref 100 2");
        system("./FALCON/ref/test_falcon_sha256 ./output/falcon2_ref_sha256 ./output/falcon5_ref_sha256 100 2");
        system("./FALCON/ref/test_falcon_sha512 ./output/falcon5_ref_sha512 ./output/falcon5_ref_sha512 100 2");

        // AVX2 FALCON
        system("make -C ./FALCON/avx2/");
        // SCRIPT + NOMEFILE1 + NOMEFILE2 + NUM ITER + INCREMENT
        system("./FALCON/avx2/test_falcon_msg ./output/falcon2_avx2 ./output/falcon5_avx2 100 2");
        system("./FALCON/avx2/test_falcon_sha256 ./output/falcon2_avx2_sha256 ./output/falcon5_avx2_sha256 100 2");
        system("./FALCON/avx2/test_falcon_sha512 ./output/falcon5_avx2_sha512 ./output/falcon5_avx2_sha512 100 2");
    }

    if(phyton_do)
        // PYTHON ANALYTICS
        system("python 20240713_performancegraphs.py");
}