# Analisi_di_algoritmi_di_firma_digitale_post-quantum
Il seguente repository contiene il codice necessario all'esecuzione di librerie di firma digitale quantum-safe per l'analisi delle loro performance.
La tesi che coinvolge questo codice non è atta a dimostrare l'effettivà sicurezza di questi algoritmi ma solo a fare confronti di prestazioni per gli algoritmi di generazione delle chiavi, gli algoritmi di firma e di verifica.
Per la "validità" (cioè la quantum-resistance) di tali algoritmi ci si affida agli studi del NIST, difatti gli algoritmi analizzati saranno quelli stanno partecipando alla competizione del NIST inerente al tema ( https://www.nist.gov/news-events/news/2022/07/nist-announces-first-four-quantum-resistant-cryptographic-algorithms ).

Gli algoritmi che verranno analizzati sono:
- CRYSTALS Dilithium
- FALCON
- Sphincs+

Per il test di questi algoritmi verrà utilizzato l'ambiente WSL (Windows Subsystem for Linux) utilizzando le Distro Ubuntu 20.04 e Ubuntu 22.04.
Qualora i test lo rendano necessario, verranno utilizzati diversi hardware per analizzare l'andamento delle prestazioni.

# Raccolta dei dati

## Preparazione dell'ambiente:
Dopo aver preparato l'ambiente WSL con la distro Ubuntu preferita è necessario installare un compilatore C e un Make per poter compilare le librerie dei vari algoritmi:
```sh
sudo apt-get update && sudo apt-get upgrade -y
sudo apt autoremove -y
sudo apt-get install gcc -y
gcc --version
```
Procedere con Make:

Se necessario installare anche Git (per ottenere il codice dei vari repo):
```sh
sudo apt-get install git
git config --global user.name "Username"
git config --global user.email "Email"
apt install make
apt install clang
```

Per poter generare ed elaborare messaggi di grande dimensione (ordine dei MegaBytes) è necessario aumentare lo spazio che i programmi possono utilizzare per lo stack:
```sh
sudo su
ulimit -s 524288
```
Con questo comando lo stack dei programmi può essere esteso fino a 524 MBytes.

## Metriche di performance
Per ogni Signature Scheme (cioè per ognuno delle famiglie di algoritmi provate) le caratteristiche misurate sono le seguenti:
- tempi e numero cicli CPU per l'operazione di generazione delle chiavi (privata e pubblica);
- tempi e numero cicli CPU per l'operazione di firma di un messaggio;
- tempi e numero cicli CPU per l'operazione di verifica della firma con parametri corretti;
- tempi e numero cicli CPU per l'operazione di verifica della firma (corrotta) per un messaggio;
- dimensioni delle chiavi (privata e pubblica)
- dimensioni della firma
Tutti questi valori vengono valutati sullo stesso hardware, nelle condizioni quanto più simili.
Inoltre vengono valutati per diversi valori di lunghezza del messaggio, in generale fatte variare dai 64bytes ai circa 128Megabytes.

## CRYSTAL Dilithium
Il codice di questo progetto è stato ottenuto direttamente dal repository Git associato:
```sh
git clone https://github.com/pq-crystals/dilithium.git
```
Prima di compilare con Make è necessario installare OpenSSL e linkare con delle variabili di ambiente la posizione della libreria nel proprio OS:
```sh
sudo apt install openssl
sudo apt install libssl-dev
export CFLAGS="-I/usr/include/openssl"
export NISTFLAGS="-I/usr/include/openssl"
export LDFLAGS="-L/usr/lib/x86_64-linux-gnu"
```
A questo punto è possibile compilare il codice delle varie cartelle. Nel repository originale sono già presenti degli script di test il cui scopo è verificare le performance e la correttezza degli algoritmi. Prenderò quelli come base per ottenere i risultati secondo le metriche di performance stabilite.

### REF Folder
In questa cartella è presente il codice "classico" di Dilithium, che effettua i calcoli con librerie del kernel sfruttando i FLoating Point, risulta essere più inefficiente della successiva variante analizzata.
Una volta raggiunta questa cartella è sufficiente compilare:
```sh
make
./test/test_dilitium2
mv output.txt output_dilitium2.txt
./test/test_dilitium2aes
mv output.txt output_dilitium2aes.txt
./test/test_dilitium3
mv output.txt output_dilitium3.txt
./test/test_dilitium3aes
mv output.txt output_dilitium3aes.txt
./test/test_dilitium5
mv output.txt output_dilitium5.txt
./test/test_dilitium5aes
mv output.txt output_dilitium5aes.txt
```
Nella cartella test saranno presenti i test inerenti alle "varianti" di Dilithium per:
- generazioni di chiavi
- firma di messaggi
- verifica della firma

### AVX2 Folder
In questa cartella invece è presente il codice con delle ottimizzazioni nel calcolo di operazioni con vettori e matrici, tuttavia è compatibile solo con architettura x64 e x86.
Le prestazioni di questo branch migliorano in tutte e tre le fasi della firma (generazione chiavi, firma e verifica).
Una volta raggiunta questa cartella è sufficiente compilare:
```sh
make
./test/test_dilitium2
mv output.txt output_dilitium2.txt
./test/test_dilitium2aes
mv output.txt output_dilitium2aes.txt
./test/test_dilitium3
mv output.txt output_dilitium3.txt
./test/test_dilitium3aes
mv output.txt output_dilitium3aes.txt
./test/test_dilitium5
mv output.txt output_dilitium5.txt
./test/test_dilitium5aes
mv output.txt output_dilitium5aes.txt
```
Lo script di test è analogo al precedente poichè la firma dei metodi rimane la stessa.

# Analisi dei dati
Per l'analisi dei dati raccolti nella fase precedente e la loro rappresentazione tramite grafici viene utilizzato uno script su python eseguito in ambiente linux. Le librerie necessarie sono Pandas, Seaborn e MatPlotLib.

## Preparazione dell'ambiente
È richiesta l'installazione di Python 3.12 nel proprio OS (Windows, Linux o Mac).
```sh
pip install pandas
pip install matplotlib
pip install seaborn
```
In caso di ambiente Windows, va aggiunto il percorso delle librerie / script Python alle variabili d'ambiente Path (del profilo utente o di sistema).

In alternativa, se si installa Python su ambiente Linux (ad esempio WSL con Distro Ubuntu) i comandi sono i seguenti:
```sh
add-apt-repository ppa:deadsnakes/ppa
apt install python3.12
python3.12 --version
apt install python3-pip
```
Successivamente installare le librerie necessarie come sopra.

## Realizzazione dei grafici
Eseguendo lo script Python presente nella root del progetto verrano generati automaticamente i grafici inerenti alle metriche di performance dei vari algoritmi provati:

### Grafico 1.1
Mette in relazione la lunghezza (in bytes) della chiave privata e pubblica generata in funzione della lunghezza del messaggio da firmare.
Agisce sui risultati del singolo algoritmo.

### Grafico 1.2
Mette in relazione la lunghezza del messaggio originale con la lunghezza del messaggio firmato (unione del messaggio originale e della firma).
Agisce sui risultati del singolo algoritmo.

### Grafico 1.3
Mette in relazione i tempi di generazione delle chiavi, i tempi di firma e di verifica con la lunghezza dei messaggi generati.
Agisce sui risultati del singolo algoritmo.

### Grafico 1.4
Mette in relazione i tempi di generazione delle chiavi con la lunghezza dei messaggi generati.
Agisce sui risultati del singolo algoritmo.

### Grafico 1.5
Mette in relazione i tempi di firma con la lunghezza dei messaggi generati.
Agisce sui risultati del singolo algoritmo.

### Grafico 1.6
Mette in relazione i tempi di verifica della firma con la lunghezza dei messaggi generati.
Agisce sui risultati del singolo algoritmo.

### Grafico 2.1
Mette in relazione la lunghezza (in bytes) della chiave privata e pubblica generata in funzione della lunghezza del messaggio da firmare.
Mette in relazione i risultati d tutti gli algoritmi insieme.

### Grafico 2.2
Mette in relazione la lunghezza del messaggio originale con la lunghezza del messaggio firmato (unione del messaggio originale e della firma).
Mette in relazione i risultati d tutti gli algoritmi insieme.

### Grafico 2.3
Mette in relazione i tempi di generazione delle chiavi, i tempi di firma e di verifica con la lunghezza dei messaggi generati.
Mette in relazione i risultati d tutti gli algoritmi insieme.

### Grafico 2.4
Mette in relazione i tempi di generazione delle chiavi con la lunghezza dei messaggi generati.
Mette in relazione i risultati d tutti gli algoritmi insieme.

### Grafico 2.5
Mette in relazione i tempi di firma con la lunghezza dei messaggi generati.
Mette in relazione i risultati d tutti gli algoritmi insieme.

### Grafico 2.6
Mette in relazione i tempi di verifica della firma con la lunghezza dei messaggi generati.
Mette in relazione i risultati d tutti gli algoritmi insieme.
