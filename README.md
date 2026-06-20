# FloWare

### Samuel Pasquier / Raffaele Presutto / Federica Mozzorecchia / Valentino Tiberio
Il software gestisce la prenotazione di appuntamenti/preventivi e 
consegne per un fioraio, con visualizzazione di catalogo, promozioni e orari da 
parte del cliente. Gestione di notifiche, fornitori e configurazioni da parte del negoziante. 

Per installare il pacchetto richiesto, esegui questo comando:

`pip install -r .\requirements.txt`

Per eseguire il programma, avvia main.py oppure esegui questo comando

`python main.py`

```
fioraioSoftware/
│
├── 📂 app/                         # IL MOTORE (Codice sorgente modulare)
│   ├── 📂 Data/                    # Persistenza dati (File CSV per la simulazione del database)
│   ├── 📂 Models/                  # Classi di dominio / Modelli (Articolo, Cliente, Utente, ecc.)
│   ├── 📂 Repos/                   # Repository per il caricamento/salvataggio dei dati CSV
│   ├── 📂 Services/                # Logica applicativa / Servizi (Gestori e sistemi)
│   ├── 📂 Tests/                   # Unit test per la verifica dei componenti
│   └── 📂 Views/                   # Interfacce grafiche utente (PyQt5) e stile globale
│
├── 📂 diagrammiUML/                # PROGETTAZIONE (Modelli e analisi visiva)
│   ├── 📂 diagramma delle classi progettazione e analisi/ # Diagrammi delle classi UML
│   ├── 📂 diagrammi casi d'uso/    # Diagrammi dei casi d'uso (.puml)
│   ├── 📂 diagrammi di attività/   # Flussi di attività UML
│   └── 📂 diagrammi di sequenza/   # Interazioni dinamiche tra componenti
│
├── Main.py                      # Punto di ingresso dell'applicazione (avvio GUI PyQt5)
├── README.md                    # Documentazione del progetto
└── requirements.txt             # Elenco delle dipendenze Python (pip)
```

