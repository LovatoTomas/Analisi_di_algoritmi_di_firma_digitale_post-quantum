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
- tempi per l'operazione di generazione delle chiavi (privata e pubblica);
- tempi per l'operazione di firma di un messaggio;
- tempi CPU per l'operazione di verifica della firma;
- dimensioni delle chiavi (privata e pubblica);
- dimensioni della firma;
- dimensioni di eventuali algoritmi di hash applicati sul messaggio;
Tutti questi valori vengono valutati sullo stesso hardware, nelle condizioni quanto più simili.

Inoltre vengono valutati per diversi valori di lunghezza del messaggio, in generale fatte variare dai 64bytes ai circa 16Megabytes.

In realtà non ha molto senso applicare algoritmi di firma e verifica direttamente sui messaggi poichè messaggi grandi portano a grandi tempi di elaborazione, dunque propongo anche una variante molto più realistica, ovvero effettuo un processo di HASH sul messaggio (tramite SHA256 e SHA512) e poi sull'hashcode eseguo la firma.

In questo modo i tempi di firma di grandi file si riducono notevolmente lasciando inalterato l'aspetto di sicurezza del processo di firma.

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
./test/test_dilitium[TIPO_ALGORITMO] [NOMEFILE1] [NOMEFILE2] [NOMEFILE3] [NUMERO_ITERAZIONI] [INCREMENTO]
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
./test/test_dilitium[TIPO_ALGORITMO] [NOMEFILE1] [NOMEFILE2] [NOMEFILE3] [NUMERO_ITERAZIONI] [INCREMENTO]
```
Lo script di test è analogo al precedente poichè la firma dei metodi rimane la stessa.

## FALCON
Il codice di questo progetto è stato ottenuto dal sito web ufficiale: https://falcon-sign.info/
Anche questo Signature Scheme si basa sui reticoli (lattice) tuttavia ha caratteristiche molto diverse da CRYSTALS Dilithium:
- è più leggera in termini di spazio, infatti le chiavi prodotte sono molto più brevi e in generale non richiede più di 30KB di RAM, perciò può essere facilmente eseguita su sistemi embedded
- per via delle chiavi più brevi richiede più tempo di computazione per le fasi di firma e verifica della firma
- in realtà il processo di firma può essere fatto in "diversi modi":
    * Firma senza espansione della chiave: viene utilizzata direttamente la chiave breve prodotta nel keygen e l'algoritmo è hast-to-point non a tempo costante, quindi in base al messaggio i tempi di firma possono essere molto diversi. Questo può creare un problema di sicurezza per qualcuno che cerca di compromettere la chive.
    * Firma senza chiave espansa a tempo costante: viene usato una funzione hash-to-point a tempo costante per rendere il tempo di firma indipendente dal messaggio a parità di lunghezza di esso.
    * Firma con chiave espansa: pre-elabora la chiave privata per velocizzare la firma. E' utile con tante firme successive.
    * Firma con chiave espansa a tempo costante: unisce gli ultimi due vantaggi.
- anche la firma può essere fatta in diversi modi:
    * Verifica classica
    * Verifica a tempo costante: anche in questo caso viene usata una funzione hash-to-point a tempo costante per rendere più difficile compromettere la chiave.

La domanda dunque è: quale di questi tempi utilizzare per i confronti con gli altri algoritmi (ad esempio con CRYSTAL Dilithium)?
La scelta è ricaduta sulle seguenti varianti di firma e verifica:
- Firma senza espansione di chiave a tempo costante: non sempre è possibile pre-elaborare la chiave / conviene farlo (per firme singole), tuttavia bisogna privilegiare la sicurezza usando una funzione hash-to-point a tempo costante.
- Verifica a tempo costante: rende il processo più sicuro.

La compilazione di questa libreria, come per la precedente, permette di scegliere se usare dei costrutti hardware per velocizzare alcuni calcoli, dunque anche di questa libreria sono stati effettuati test per la cosidetta versione "REF" e versione "AVX2".

# Analisi dei dati
Per l'analisi dei dati raccolti nella fase precedente e la loro rappresentazione tramite grafici vengono utilizzati due script in ambiente Linux:
1 - Il primo è uno script C il cui compito è quello di:
    - compilare tutti i codici sorgenti delle varie librerie e test da effettuare;
    - avvia i test con i parametri scelti e redireziona gli output nei file corretti;
    - avvia lo script di analisi (vedi successivo).
2 - Il secondo è uno script in Python per l'analisi dei file di output, contenenti le statistiche sulle dimensioni e i tempi dei vari algoritmi.
Le librerie necessarie alla sua esecuzione sono Pandas, Seaborn e MatPlotLib.

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

## Avvio della fase di Analytics
Per avviare i due script di raccolta informazioni è necessario eseguire le seguenti istruzioni nella root del repository:
```sh
gcc start_analytics.c -o start_analytics
./start_analytics 1 1 1
```
I tre parametri (1 1 1) attivano le seguenti parti dell'algoritmo:
1 - Compilazione e test di CRYSTALS Dilithium;
2 - Compilazione e test di FALCON;
3 - Avvio dello script Python per la produzione dei grafici;

Di conseguenza per produrre i soli grafici è necessario eseguire:
```sh
./start_analytics 0 0 1
```

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
