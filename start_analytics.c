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

    // PYTHON ANALYTICS
    system("python 20240713_performancegraphs.py");
}