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

## Metriche di performance
Per ogni Signature Scheme (cioè per ognuno delle famiglie di algoritmi provate) le caratteristiche misurate sono le seguenti:
- tempi per l'operazione di generazione delle chiavi (privata e pubblica);
- tempi per l'operazione di firma di un messaggio;
- tempi CPU per l'operazione di verifica della firma;
- dimensioni delle chiavi (privata e pubblica);
- dimensioni della firma;
- dimensioni di eventuali algoritmi di hash applicati sul messaggio;
Tutti questi valori vengono valutati sullo stesso hardware, nelle condizioni quanto più simili.

Inoltre vengono valutati per diversi valori di lunghezza del messaggio, in generale fatte variare dai 32 bytes ai circa 16 Megabytes.

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

## SPHINCS+
Per scaricare il codice della terza submission è sufficiente digitare:
```sh
git clone https://github.com/sphincs/sphincsplus.git
```
Nella root ci sono dei file python che permettono di eseguire test/benchmark per tutte le versioni disponibili dello Signature Scheme, scritte tutte in C e ciascuna con i propri script di test in C.
Anche in questo caso le versioni utilizzate per i test sono state quella di riferimento (REF, che non contiene ottimizzazioni per l'uso specifico di hardware, quindi è compatibile con tutto) e la versione AVX2 (compatibile con hardware x86 e x64 per l'ottimizzazione di operazioni con i vettori).
Per ognuna di queste due sono stati effettuati test per i vari livelli di sicurezza proposti da Sphincs+, rispettivamente 128bit, 192bit e 256bit (compatibili con i livelli di sicurezza offerti da Dilithium2, Dilithium3, Dilithium5, ad esempio).
Per ogni sottocartella si possono avviare i test lanciando:
```sh
make all
./test/spx
```
Dai test si nota una cosa molto particolare:
1 - Le dimensioni delle chiavi sono molto ridotte rispetto ai precedenti
2 - Il tempo di firma è elevato
3 - Il tempo di firma è quasi costante al variare della lunghezza del messaggio, questo implica che Sphincs+ include già al suo interno un meccanismo di Hashing del messaggio che "ammortizza" la dipendenza dal contenuto.
Nonostante ciò le prove effettuate sono sempre state le stesse, quindi:
* firma con messaggio variabile
* firma con hashing del messaggio con SHA-128
* firma con hashing del messaggio con SHA-256
Negli ultimi due tentativi si cerca di ridurre lo sforzo computazione di Sphincs+ nell'hashing dei messaggi lunghi offrendogli già degli hashcode corti.

## RSA
Un'altra idea è quella di confrontare le prestazioni di questi algoritmi quantum-safe con uno degli algoritmi attualmente più utilizzato, cioè RSA.
Per l'esecuzione dei test è sufficiente l'uso della libreria OpenSSL già scaricata per le prove precedenti. La prova consisterà dunque nella scrittura di un solo file di test.
Per l'RSA sono stati evitati i test che provano la firma e verifica direttamente su messaggi lunghi banalmente perchè RSA non supporta la firma di messaggi più lunghi della chiave stessa. Tuttavia al variare della lunghezza del messaggio sono stati trattati i casi di applicazione di SHA256 e SHA512 sul messaggio.
Dunque per i test ci si è basati sugli hashcode dei messaggi, rispettivamente ottenuti con SHA-256 e SHA-512, dunque di dimensioni totali di 32 byte e 64 byte.
Anche per RSA sono stati valutati i vari livelli di sicurezza (128bit, 192bit e 256bit) ottenuti con le chiavi di lunghezza 3072, 7680, 15360 (bits).
Le metriche di performance utilizzate infine sono state le solite.

# Analisi dei dati
Per l'analisi dei dati raccolti nella fase precedente e la loro rappresentazione tramite grafici vengono utilizzati due script in ambiente Linux:
1 - Il primo è uno script C il cui compito è quello di:
    - compilare tutti i codici sorgenti delle varie librerie e test da effettuare;
    - avvia i test con i parametri scelti e redireziona gli output nei file corretti;
    - avvia lo script di analisi (vedi successivo).
2 - Il secondo è uno script in Python per l'analisi dei file di output, contenenti le statistiche sulle dimensioni e i tempi dei vari algoritmi.
Le librerie necessarie alla sua esecuzione sono Pandas, Seaborn e MatPlotLib.
Per rendere il tutto più responsivo si può aggiungere una libreria per il display delle progress-bar (tqdm).

## Preparazione dell'ambiente
È richiesta l'installazione di Python 3.12 nel proprio OS (Windows, Linux o Mac).
```sh
pip install pandas
pip install matplotlib
pip install seaborn
pip install tqdm

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
./start_analytics 1 1 1 1 1
```
I tre parametri (1 1 1) attivano le seguenti parti dell'algoritmo:
1 - Compilazione e test di CRYSTALS Dilithium;
2 - Compilazione e test di FALCON;
3 - Avvio dello script Python per la produzione dei grafici;

Di conseguenza per produrre i soli grafici è necessario eseguire:
```sh
./start_analytics 0 0 0 0 1
```

## Realizzazione dei grafici
Eseguendo lo script Python presente nella root del progetto verrano generati automaticamente i grafici inerenti alle metriche di performance dei vari algoritmi provati:

### Grafico 1.1
Mette in relazione la lunghezza (in bytes) della chiave privata e pubblica generata tra i vari algoritmi selezionati.
Gli algoritmi selezionati sono:
- quelli di una stessa famiglia
- algoritmi di famiglie diverse a parità di livello di sicurezza

### Grafico 1.2
Per ogni algoritmo in input mostra la lunghezza della firma prodotta, indipendentemente dalla lunghezza del messaggio.
Gli algoritmi selezionati sono:
- quelli di una stessa famiglia
- algoritmi di famiglie diverse a parità di livello di sicurezza

### Grafico 1.3
Mette in relazione i tempi di generazione delle chiavi con la lunghezza dei messaggi generati.
Gli algoritmi selezionati sono:
- quelli di una stessa famiglia
- algoritmi di famiglie diverse a parità di livello di sicurezza

### Grafico 1.4
Mette in relazione i tempi di firma con la lunghezza dei messaggi generati.
Gli algoritmi selezionati sono:
- quelli di una stessa famiglia
- quelli di una stessa famiglia e configurazione ma che variano per applicazione di algoritmi di hash (SHA)
- algoritmi di famiglie diverse a parità di livello di sicurezza
- algoritmi di famiglie diverse a parità di livello di sicurezza, che variano per applicazione di algoritmi di hash (SHA)

### Grafico 1.5
Mette in relazione i tempi di firma con la lunghezza dei messaggi generati, ma tramite istogrammi.
Gli algoritmi selezionati sono:
- quelli di una stessa famiglia e configurazione ma che variano per applicazione di algoritmi di hash (SHA)
- algoritmi di famiglie diverse a parità di livello di sicurezza, che variano per applicazione di algoritmi di hash (SHA)

### Grafico 1.6
Mette in relazione i tempi di verifica della firma con la lunghezza dei messaggi generati.
Gli algoritmi selezionati sono:
- quelli di una stessa famiglia
- quelli di una stessa famiglia e configurazione ma che variano per applicazione di algoritmi di hash (SHA)
- algoritmi di famiglie diverse a parità di livello di sicurezza
- algoritmi di famiglie diverse a parità di livello di sicurezza, che variano per applicazione di algoritmi di hash (SHA)

### Grafico 1.7
Mette in relazione i tempi di verifica della firma con la lunghezza dei messaggi generati, ma tramite istogrammi.
Gli algoritmi selezionati sono:
- quelli di una stessa famiglia e configurazione ma che variano per applicazione di algoritmi di hash (SHA)
- algoritmi di famiglie diverse a parità di livello di sicurezza, che variano per applicazione di algoritmi di hash (SHA)

# Verifica dei dati ottenuti
Come in ogni ricerca scientifica che si rispetti, bisogna fare almeno una controprova per essere sicuri di non aver generato dati errati.
Dunque ho deciso di rieffettuare parte dei test (sopratutto quelli legati ai tempi) con una libreria diversa che già incorpora al suo interno implementazioni di CRYSTALS Dilithium, FALCON e SPHINCS+ e che le "interfaccia" in maniera comune.
GLi aspetti che maggiormente mi interessano da queste verifiche, come già anticipato, sono i tempi di keygen, firma e verifica. Le dimensioni delle chiavi e della firma sono già verificate con i dati / report rilasciati dal NIST.

La libreria in questione è liboqs: https://github.com/open-quantum-safe/liboqs/tree/main
Procediamo ad installarla sullo stesso ambiente:
```sh
    sudo apt install astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind
    git clone --recursive https://github.com/open-quantum-safe/liboqs.git
    cd liboqs
    sudo apt-get update
    sudo apt-get install -y cmake gcc libssl-dev make
    mkdir build
    cd build
    cmake -DBUILD_SHARED_LIBS=ON ..
    make
    sudo make install
```
In questo caso installiamo solo la libreria, non ne scarichiamo i sorgenti per modificarli come nei precedenti casi.
Per verificare l'installazione:
```sh
ls /usr/local/lib | grep liboqs
ls /usr/lib | grep liboqs
sudo ldconfig
```

Dentro la cartella "liboqs_double_check" sono stati inseriti due script Python che:
* check_install.py: verifica se liboqs è stata correttamente installata e quali signature scheme sono disponibili
* double_check.py: esegue delle prove e calcola la media dei tempi su più tentativi di keygen/firma/verifica per ciascun algoritmo

Allo stato attuale, i test con questa libreria sono stati fatti sugli stessi algoritmi delle sezioni precedenti MA solo sulle versioni AVX2, quindi con le ottimizzazioni per hardware x64 e x86 per il calcolo di operazioni con vettori o matrici.

Nella stessa cartella sono presenti i file di output con i dati estrapolati dalle prove. Lo script di analytics utilizzato per le fasi precedenti è in grado di elaborare tali dati e generare dei grafici (gli stessi) che mettano in relazione le mie prove con quelle delle libreria.
Si nota che i risultati sono molto simili, quasi sempre sullo stesso ordine di grandezza, questo rende "valide" le mie prove passate.
Le metriche e le tecniche utilizzate per l'estrapolazione di dati sono sempre le stesse.