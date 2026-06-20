"""
Main.py - Punto di ingresso dell'applicazione

Crea la QApplication, mostra InterfacciaLogin e, dopo il login
riuscito, apre l'interfaccia corretta (Cliente o Negoziante)
in base al ruolo dell'utente autenticato.
"""

import sys

from PyQt5.QtWidgets import QApplication

from app.Services.sistemaAccesso import SistemaAccesso
from app.Views.interfacciaLogin import InterfacciaLogin, mostraErrore
from app.Views import interfacciaCliente, interfacciaNegoziante
from app.Views.configStile import carica_stile, applica_stile_globale



class Applicazione:
    """Orchestratore principale: gestisce il flusso login -> interfaccia ruolo."""

    def __init__(self):
        self.app = QApplication(sys.argv)

        # Riferimenti alle finestre, mantenuti per evitare il garbage collector
        self.finestra_login = None
        self.finestra_principale = None

    def avvia(self):
        """Mostra la finestra di login e avvia il loop degli eventi."""
        carica_stile()
        applica_stile_globale()
        self.finestra_login = InterfacciaLogin()
        self.finestra_login.loginEffettuato.connect(self._dopo_login)
        self.finestra_login.show()

        sys.exit(self.app.exec_())

    def _dopo_login(self, utente):
        """Slot chiamato dopo login riuscito: apre l'interfaccia corretta."""
        ruolo = utente.getRuolo()

        try:
            destinazione = SistemaAccesso.reindirizzaPerRuolo(ruolo)
        except ValueError as e:
            mostraErrore(self.finestra_login, str(e))
            return

        if destinazione == "InterfacciaCliente":
            cliente_id = getattr(utente, "id", None)
            self.finestra_principale = interfacciaCliente.start(CLIENTE_ID=cliente_id)
        elif destinazione == "InterfacciaNegoziante":
            negoziante_id = getattr(utente, "id", None)
            self.finestra_principale = interfacciaNegoziante.start(negoziante_id=negoziante_id)
        else:
            mostraErrore(self.finestra_login, f"Interfaccia non riconosciuta: {destinazione}")
            return

        self.finestra_principale.show()
        self.finestra_login.close()


if __name__ == "__main__":
    applicazione = Applicazione()
    applicazione.avvia()
