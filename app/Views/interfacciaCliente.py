"""
InterfacciaCliente - GUI PyQt5 per il sistema negozio (lato cliente)

"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QMessageBox,
    QGroupBox,
    QHeaderView,
    QStackedWidget,
)


from app.Services.sistemaRichieste import SistemaRichieste
from app.Services.gestoreConsegne import GestoreConsegne
from app.Services.sistemaInfoNegozio import SistemaInfoNegozio
from app.Services.sistemaCatalogo import SistemaCatalogo
from app.Services.sistemaOfferte import SistemaOfferte



# TAB: CATALOGO
class CatalogoTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna catalogo")
        self.btn_aggiorna.clicked.connect(self.mostraCatalogo)
        top_bar.addWidget(QLabel("<b>Catalogo articoli</b>"))
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        content = QHBoxLayout()

        self.lista_articoli = QListWidget()
        self.lista_articoli.itemClicked.connect(self.onArticoloSelezionato)
        content.addWidget(self.lista_articoli, 2)

        self.dettagli_box = QGroupBox("Dettagli articolo")
        dettagli_layout = QFormLayout()
        self.lbl_nome = QLabel("-")
        self.lbl_descrizione = QLabel("-")
        self.lbl_descrizione.setWordWrap(True)
        self.lbl_prezzo_originale = QLabel("-")
        self.lbl_prezzo = QLabel("-")
        self.lbl_quantita = QLabel("-")
        self.lbl_disponibile = QLabel("-")
        dettagli_layout.addRow("Nome:", self.lbl_nome)
        dettagli_layout.addRow("Descrizione:", self.lbl_descrizione)
        dettagli_layout.addRow("Prezzo Originale:", self.lbl_prezzo)
        dettagli_layout.addRow("Prezzo:", self.lbl_prezzo_originale)
        dettagli_layout.addRow("Quantità:", self.lbl_quantita)
        dettagli_layout.addRow("Disponibile:", self.lbl_disponibile)
        self.dettagli_box.setLayout(dettagli_layout)
        content.addWidget(self.dettagli_box, 1)

        layout.addLayout(content)

        self.mostraCatalogo()

    def mostraCatalogo(self):
        try:
            articoli = SistemaCatalogo.visualizzaCatalogo()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare il catalogo: {e}")
            return

        self.lista_articoli.clear()
        for articolo in articoli:
            nome = getattr(articolo, "nome", str(articolo))
            prezzo = str(SistemaCatalogo.PrezzoF(getattr(articolo, "id", "-")))
            item = QListWidgetItem(f"{nome} - {prezzo} €")
            item.setData(Qt.UserRole, getattr(articolo, "id", None))
            self.lista_articoli.addItem(item)

    def onArticoloSelezionato(self, item):
        id_articolo = item.data(Qt.UserRole)
        if id_articolo is None:
            return
        try:
            articolo = SistemaCatalogo.richiediDettagli(id_articolo)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore nel recupero dei dettagli: {e}")
            return

        self.mostraDettagliArticolo(articolo)

    def mostraDettagliArticolo(self, articolo):
        self.lbl_nome.setText(str(getattr(articolo, "nome", "-")))
        self.lbl_descrizione.setText(str(getattr(articolo, "descrizione", "-")))
        self.lbl_prezzo.setText(str(SistemaCatalogo.PrezzoF(getattr(articolo, "id", "-"))))
        self.lbl_prezzo_originale.setText(str(getattr(articolo, "prezzo", "-")))
        self.lbl_quantita.setText(str(getattr(articolo, "quantita", "-")))
        disponibile = getattr(articolo, "disponibile", None)
        self.lbl_disponibile.setText("Sì" if disponibile else "No")


# TAB: OFFERTE

class OfferteTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna offerte")
        self.btn_aggiorna.clicked.connect(self.mostraOfferte)
        top_bar.addWidget(QLabel("<b>Offerte attive</b>"))
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        self.lista_offerte = QListWidget()
        layout.addWidget(self.lista_offerte)

        self.mostraOfferte()

    def mostraOfferte(self):
        try:
            offerte = SistemaOfferte.visualizzaOfferteAttive()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare le offerte: {e}")
            return

        self.lista_offerte.clear()
        if not offerte:
            self.lista_offerte.addItem("Nessuna offerta attiva al momento.")
            return

        for offerta in offerte:
            descrizione = getattr(offerta, "descrizione", str(offerta))
            data_inizio = getattr(offerta, "dataInizio", "")
            data_fine = getattr(offerta, "dataFine", "")
            testo = f"{descrizione}"
            if data_inizio or data_fine:
                testo += f"  (dal {data_inizio} al {data_fine})"
            self.lista_offerte.addItem(testo)


# TAB: ORARI
class OrariTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna orari")
        self.btn_aggiorna.clicked.connect(self.mostraTabellaOrari)
        top_bar.addWidget(QLabel("<b>Orari del negozio</b>"))
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        self.tabella = QTableWidget()
        self.tabella.setColumnCount(4)
        self.tabella.setHorizontalHeaderLabels(
            ["Giorno", "Apertura", "Chiusura", "Tipo / Data specifica"]
        )
        self.tabella.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabella.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabella)

        self.mostraTabellaOrari()

    def mostraTabellaOrari(self):
        try:
            orari = SistemaInfoNegozio.richiediOrari()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare gli orari: {e}")
            return

        self.tabella.setRowCount(len(orari))
        for row, orario in enumerate(orari):
            giorno = getattr(orario, "giorno", "")
            apertura = getattr(orario, "apertura", "")
            chiusura = getattr(orario, "chiusura", "")
            tipo = getattr(orario, "tipo", "")
            data_specifica = getattr(orario, "dataSpecifica", "")

            ultima_colonna = tipo
            if data_specifica:
                ultima_colonna = f"{tipo} ({data_specifica})"

            self.tabella.setItem(row, 0, QTableWidgetItem(str(giorno)))
            self.tabella.setItem(row, 1, QTableWidgetItem(str(apertura)))
            self.tabella.setItem(row, 2, QTableWidgetItem(str(chiusura)))
            self.tabella.setItem(row, 3, QTableWidgetItem(str(ultima_colonna)))


# TAB: RICHIESTE
class RichiesteTab(QWidget):

    def __init__(self, cliente_id, parent=None):
        super().__init__(parent)
        self.cliente_id = cliente_id

        layout = QVBoxLayout(self)

        # --- Sezione: nuova richiesta ---
        nuova_box = QGroupBox("Nuova richiesta")
        form_layout = QFormLayout()

        self.combo_tipo = QComboBox()
        try:
            for tipo in SistemaRichieste.richiediOpzioni():
                self.combo_tipo.addItem(tipo)
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare i tipi di richiesta: {e}")
        self.combo_tipo.currentTextChanged.connect(self.mostraCampi)

        self.edit_descrizione = QTextEdit()
        self.edit_descrizione.setMaximumHeight(80)
        self.edit_contatti = QLineEdit()

        # Campi specifici per "appuntamento" (slot calendario)
        self.combo_data = QComboBox()
        self.combo_fascia = QComboBox()
        self.combo_data.currentTextChanged.connect(self.aggiornaFasceOrarie)
        self.btn_carica_date = QPushButton("Carica date disponibili")
        self.btn_carica_date.clicked.connect(self.caricaDateDisponibili)

        self.label_data = QLabel("Data:")
        self.label_fascia = QLabel("Fascia oraria:")

        form_layout.addRow("Tipo richiesta:", self.combo_tipo)
        form_layout.addRow("Descrizione:", self.edit_descrizione)
        form_layout.addRow("Contatti:", self.edit_contatti)
        form_layout.addRow(self.btn_carica_date)
        form_layout.addRow(self.label_data, self.combo_data)
        form_layout.addRow(self.label_fascia, self.combo_fascia)

        self.btn_invia = QPushButton("Invia richiesta")
        self.btn_invia.clicked.connect(self.inviaRichiesta)
        form_layout.addRow(self.btn_invia)

        nuova_box.setLayout(form_layout)
        layout.addWidget(nuova_box)

        # --- Sezione: elenco richieste ---
        elenco_box = QGroupBox("Le mie richieste")
        elenco_layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.btn_aggiorna_richieste = QPushButton("Aggiorna elenco")
        self.btn_aggiorna_richieste.clicked.connect(self.mostraElencoRichieste)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna_richieste)
        elenco_layout.addLayout(top_bar)

        self.tabella_richieste = QTableWidget()
        self.tabella_richieste.setColumnCount(5)
        self.tabella_richieste.setHorizontalHeaderLabels(
            ["ID", "Tipo", "Stato", "Data/Ora", "Descrizione"]
        )
        self.tabella_richieste.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabella_richieste.setEditTriggers(QTableWidget.NoEditTriggers)
        elenco_layout.addWidget(self.tabella_richieste)

        self.btn_annulla = QPushButton("Annulla richiesta selezionata")
        self.btn_annulla.clicked.connect(self.annullaRichiesta)
        elenco_layout.addWidget(self.btn_annulla)

        elenco_box.setLayout(elenco_layout)
        layout.addWidget(elenco_box)

        self.mostraCampi(self.combo_tipo.currentText())
        self.mostraElencoRichieste()

    def mostraCampi(self, tipo):
        """Mostra/nasconde i campi calendario in base al tipo selezionato."""
        is_appuntamento = (tipo == "appuntamento")
        self.btn_carica_date.setVisible(is_appuntamento)
        self.label_data.setVisible(is_appuntamento)
        self.combo_data.setVisible(is_appuntamento)
        self.label_fascia.setVisible(is_appuntamento)
        self.combo_fascia.setVisible(is_appuntamento)

    def caricaDateDisponibili(self):
        try:
            date = SistemaRichieste.recuperaDateDisponibili()
        except Exception as e:
            mostraErrore(self, f"Impossibile recuperare le date disponibili: {e}")
            return

        self.combo_data.clear()
        for data in date:
            self.combo_data.addItem(str(data))

    def aggiornaFasceOrarie(self, data):
        if not data:
            self.combo_fascia.clear()
            return
        try:
            fasce = SistemaRichieste.recuperaFasceOrarie(data)
        except Exception as e:
            mostraErrore(self, f"Impossibile recuperare le fasce orarie: {e}")
            return

        self.combo_fascia.clear()
        for fascia in fasce:
            self.combo_fascia.addItem(str(fascia))

    def inviaRichiesta(self):
        tipo = self.combo_tipo.currentText()
        descrizione = self.edit_descrizione.toPlainText().strip()
        contatti = self.edit_contatti.text().strip()

        data = ""
        ora = ""
        if tipo == "appuntamento":
            data = self.combo_data.currentText()
            ora = self.combo_fascia.currentText()

        dati_richiesta = {
            "tipo": tipo,
            "descrizione": descrizione,
            "contatti": contatti,
            "data": data,
            "ora": ora,
            "clienteId": self.cliente_id,
        }

        try:
            # Se è un appuntamento e sono stati scelti data/ora, conferma lo slot
            if tipo == "appuntamento" and data and ora:
                SistemaRichieste.confermaScelta(data, ora)
            richiesta = SistemaRichieste.inviaRichiesta(dati_richiesta)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'invio della richiesta: {e}")
            return

        mostraConferma(self, "Richiesta inviata con successo.")
        self.edit_descrizione.clear()
        self.edit_contatti.clear()
        self.mostraElencoRichieste()

    def mostraElencoRichieste(self):
        try:
            richieste = SistemaRichieste.recuperaRichieste(self.cliente_id)
        except Exception as e:
            mostraErrore(self, f"Impossibile recuperare le richieste: {e}")
            return

        self.tabella_richieste.setRowCount(len(richieste))
        for row, richiesta in enumerate(richieste):
            id_r = getattr(richiesta, "id", "")
            tipo = getattr(richiesta, "tipo", "")
            stato = getattr(richiesta, "stato", "")
            try:
                data_ora = richiesta.getDataOra()
            except AttributeError:
                data_ora = ""
            descrizione = getattr(richiesta, "descrizione", "")

            self.tabella_richieste.setItem(row, 0, QTableWidgetItem(str(id_r)))
            self.tabella_richieste.setItem(row, 1, QTableWidgetItem(str(tipo)))
            self.tabella_richieste.setItem(row, 2, QTableWidgetItem(str(stato)))
            self.tabella_richieste.setItem(row, 3, QTableWidgetItem(str(data_ora)))
            self.tabella_richieste.setItem(row, 4, QTableWidgetItem(str(descrizione)))

    def annullaRichiesta(self):
        row = self.tabella_richieste.currentRow()
        if row < 0:
            mostraErrore(self, "Seleziona una richiesta da annullare.")
            return

        id_item = self.tabella_richieste.item(row, 0)
        if id_item is None:
            return
        id_richiesta = id_item.text()

        conferma = QMessageBox.question(
            self,
            "Conferma annullamento",
            f"Vuoi davvero annullare la richiesta #{id_richiesta}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if conferma != QMessageBox.Yes:
            return

        try:
            # id_richiesta è recuperato come stringa dalla tabella: convertilo se necessario
            try:
                id_richiesta_val = int(id_richiesta)
            except ValueError:
                id_richiesta_val = id_richiesta

            SistemaRichieste.annullaRichiesta(id_richiesta_val)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'annullamento: {e}")
            return

        mostraConferma(self, "Richiesta annullata.")
        self.mostraElencoRichieste()


# TAB: CONSEGNE

class ConsegneTab(QWidget):

    def __init__(self, cliente_id, parent=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.ultima_consegna_id = None

        layout = QVBoxLayout(self)

        # --- Sezione: nuova richiesta di consegna ---
        nuova_box = QGroupBox("Richiedi consegna a domicilio")
        form_layout = QFormLayout()

        self.edit_regione = QLineEdit()
        self.edit_citta = QLineEdit()
        self.edit_via = QLineEdit()
        self.edit_civico = QLineEdit()

        form_layout.addRow("Regione:", self.edit_regione)
        form_layout.addRow("Città:", self.edit_citta)
        form_layout.addRow("Via:", self.edit_via)
        form_layout.addRow("Civico:", self.edit_civico)

        self.btn_richiedi = QPushButton("Invia richiesta di consegna")
        self.btn_richiedi.clicked.connect(self.richiediConsegna)
        form_layout.addRow(self.btn_richiedi)

        nuova_box.setLayout(form_layout)
        layout.addWidget(nuova_box)

        # --- Sezione: stato consegna ---
        stato_box = QGroupBox("Stato consegna")
        stato_layout = QFormLayout()

        self.edit_id_consegna = QLineEdit()
        self.btn_verifica_stato = QPushButton("Verifica stato")
        self.btn_verifica_stato.clicked.connect(self.verificaStatoConsegna)

        self.lbl_stato_consegna = QLabel("-")
        self.lbl_indirizzo_consegna = QLabel("-")

        stato_layout.addRow("ID consegna:", self.edit_id_consegna)
        stato_layout.addRow(self.btn_verifica_stato)
        stato_layout.addRow("Stato:", self.lbl_stato_consegna)
        stato_layout.addRow("Indirizzo:", self.lbl_indirizzo_consegna)

        stato_box.setLayout(stato_layout)
        layout.addWidget(stato_box)

        layout.addStretch()

    def richiediConsegna(self):
        dati = {
            "clienteId": self.cliente_id,
            "regione": self.edit_regione.text().strip(),
            "citta": self.edit_citta.text().strip(),
            "via": self.edit_via.text().strip(),
            "civico": self.edit_civico.text().strip(),
        }

        if not dati["regione"] or not dati["via"] or not dati["civico"]:
            mostraErrore(self, "Compila tutti i campi obbligatori (regione, via, civico).")
            return

        try:
            consegna = GestoreConsegne.confermaRichiesta(dati)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante la richiesta di consegna: {e}")
            return

        id_consegna = getattr(consegna, "id", None)
        self.ultima_consegna_id = id_consegna

        mostraConferma(
            self,
            f"Richiesta di consegna inviata con successo."
            + (f"\nID consegna: {id_consegna}" if id_consegna is not None else ""),
        )

        self.edit_regione.clear()
        self.edit_citta.clear()
        self.edit_via.clear()
        self.edit_civico.clear()

        if id_consegna is not None:
            self.edit_id_consegna.setText(str(id_consegna))

    def verificaStatoConsegna(self):
        id_text = self.edit_id_consegna.text().strip()
        if not id_text:
            mostraErrore(self, "Inserisci l'ID della consegna.")
            return

        try:
            id_consegna = int(id_text)
        except ValueError:
            id_consegna = id_text

        try:
            consegna = GestoreConsegne.trovaPerId(id_consegna)
        except Exception as e:
            mostraErrore(self, f"Errore durante la verifica: {e}")
            return

        if consegna is None:
            mostraErrore(self, f"Nessuna consegna trovata con id={id_consegna}.")
            self.lbl_stato_consegna.setText("-")
            self.lbl_indirizzo_consegna.setText("-")
            return

        try:
            stato = consegna.getStato()
        except AttributeError:
            stato = getattr(consegna, "stato", "-")

        regione = getattr(consegna, "regione", "")
        citta = getattr(consegna, "citta", "")
        via = getattr(consegna, "via", "")
        civico = getattr(consegna, "civico", "")
        indirizzo = f"{via} {civico}, {citta} ({regione})"

        self.lbl_stato_consegna.setText(str(stato))
        self.lbl_indirizzo_consegna.setText(indirizzo)


class SessionControlWidget(QWidget):
    """
    A widget containing a Disconnect button (to return to the login screen)
    and a Quit button (to exit the application).
    """

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Keep a reference to the active QMainWindow

        # Horizontal layout to align buttons to the right
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 10)

        # Buttons definition
        self.btn_disconnetti = QPushButton("Disconnetti")
        self.btn_esci = QPushButton("Esci")

        # Optional: Add clear style differentiation
        self.btn_disconnetti.setStyleSheet(
            "background-color: #D78521; color: white; font-weight: bold; padding: 6px 12px;")
        self.btn_esci.setStyleSheet("background-color: #DE1A1A; color: white; font-weight: bold; padding: 6px 12px;")

        # Connect actions
        self.btn_disconnetti.clicked.connect(self.handle_disconnetti)
        self.btn_esci.clicked.connect(self.handle_esci)

        layout.addStretch()
        layout.addWidget(self.btn_disconnetti)
        layout.addWidget(self.btn_esci)

    def handle_disconnetti(self):
        # 1. Clear session variables
        from app.Services.sistemaAccesso import SistemaAccesso
        SistemaAccesso.sessione["utente"] = None
        SistemaAccesso.sessione["ruolo"] = None

        # 2. Instantiate and show the Login window again
        from app.Views.interfacciaLogin import InterfacciaLogin
        self.finestra_login = InterfacciaLogin()
        self.finestra_login.show()

        # 3. Close the current main window (Negoziante or Cliente)
        self.main_window.close()

    def handle_esci(self):
        # Exit the application cleanly
        QApplication.quit()

# FINESTRA PRINCIPALE
class InterfacciaCliente(QMainWindow):


    def __init__(self, cliente_id, parent=None):
        super().__init__(parent)
        self.cliente_id = cliente_id

        self.setWindowTitle("Negozio - Area Cliente")
        self.resize(900, 650)

        self.mostraDashboardCliente()

    def mostraDashboardCliente(self):
        # Main container layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(CatalogoTab(self), "Catalogo")
        tabs.addTab(OfferteTab(self), "Offerte")
        tabs.addTab(OrariTab(self), "Orari")
        tabs.addTab(RichiesteTab(self.cliente_id, self), "Richieste")
        tabs.addTab(ConsegneTab(self.cliente_id, self), "Consegne")
        # Session control panel at the bottom
        self.session_control = SessionControlWidget(self)

        main_layout.addWidget(tabs)
        main_layout.addWidget(self.session_control)
        self.setCentralWidget(container)


def mostraMessaggio(parent, messaggio):
    QMessageBox.information(parent, "Messaggio", messaggio)


def mostraConferma(parent, messaggio):
    QMessageBox.information(parent, "Conferma", messaggio)


def mostraErrore(parent, messaggio):
    QMessageBox.critical(parent, "Errore", messaggio)


# AVVIO APPLICAZIONE (esempio)
def start(CLIENTE_ID):
    finestra = InterfacciaCliente(cliente_id=CLIENTE_ID)
    return finestra


if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = start(CLIENTE_ID=1)
    finestra.show()
    sys.exit(app.exec_())