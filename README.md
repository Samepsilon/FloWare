# FioraioSoftware

### Samuel Pasquier / 
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
├── 📂 app/                          # LE MOTEUR (Code source modulaire)
│   ├── data_prep.py                # Pipeline de transformation des données brutes
│   ├── model_utils.py              # Logique d'entraînement, Cross-Val et Optuna
│   ├── metrics.py                  # Définition mathématique du coût métier
│   └── explainability.py           # Moteur d'interprétabilité (SHAP)
│
├── 📂 diagrammiUML/                    # LES EXPÉRIENCES (Notebooks)
│   ├── 01_data_preparation.ipynb   # Exécution du pipeline de nettoyage
│   ├── 02_model_training.ipynb     # Orchestration des entraînements et MLflow
│   ├── 03_explainability.ipynb     # Analyse des décisions du modèle
│   └── 04_mlflow_serving_test.ipynb # Simulation client / test API
│
├── 📂 model/                        # Artefact final
├── 📂 mlruns/                       # Base de données de tracking (Logs)
├── Dockerfile                      # Fichier de mise en place Docker
└── requirements.txt                # Liste des dépendances (pip) 
```
