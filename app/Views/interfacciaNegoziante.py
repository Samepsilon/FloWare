"""
InterfacciaNegoziante - GUI PyQt5 per il sistema negozio

Compatibile con interfacciaCliente.py: stesse convenzioni (file unico,
QMessageBox per errori/conferme, helper mostraErrore/mostraConferma/
mostraMessaggio identici).

NOTA: adatta gli import dei controller (sezione "IMPORT CONTROLLER")
al path reale del tuo progetto se diverso.
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
    QCheckBox,
    QMessageBox,
    QGroupBox,
    QHeaderView,
)


# =====================================================================
# IMPORT CONTROLLER
# =====================================================================
from app.Services.gestoreCatalogo import GestoreCatalogo
from app.Services.gestoreFornitori import GestoreFornitori
from app.Services.gestoreOfferte import GestoreOfferte
from app.Services.gestoreOrari import GestoreOrari
from app.Services.gestoreNotifiche import GestoreNotifiche
from app.Services.gestoreConsegne import GestoreConsegne


# Stati validi per una consegna (dropdown fisso)
STATI_CONSEGNA = ["in attesa", "in consegna", "consegnata", "annullata"]

# Giorni della settimana per orario settimanale
GIORNI_SETTIMANA = [
    "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"
]


# TAB: CATALOGO
class CatalogoNegozianteTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.articolo_selezionato_id = None

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna catalogo")
        self.btn_aggiorna.clicked.connect(self.mostraCatalogo)
        top_bar.addWidget(QLabel("<b>Gestione catalogo</b>"))
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        content = QHBoxLayout()

        self.lista_articoli = QListWidget()
        self.lista_articoli.itemClicked.connect(self.onArticoloSelezionato)
        content.addWidget(self.lista_articoli, 2)

        form_box = QGroupBox("Dettagli / Form articolo")
        form_layout = QFormLayout()

        self.edit_nome = QLineEdit()
        self.edit_descrizione = QTextEdit()
        self.edit_descrizione.setMaximumHeight(70)
        self.edit_prezzo = QLineEdit()
        self.edit_quantita = QLineEdit()
        self.check_disponibile = QCheckBox("Disponibile")
        self.check_disponibile.setChecked(True)
        self.edit_fornitore_id = QLineEdit()
        self.edit_fornitore_id.setPlaceholderText("ID fornitore (opzionale)")
        self.lbl_prezzo_finale = QLabel("-")

        form_layout.addRow("Nome:", self.edit_nome)
        form_layout.addRow("Descrizione:", self.edit_descrizione)
        form_layout.addRow("Prezzo:", self.edit_prezzo)
        form_layout.addRow("Quantità:", self.edit_quantita)
        form_layout.addRow("", self.check_disponibile)
        form_layout.addRow("Fornitore ID:", self.edit_fornitore_id)
        form_layout.addRow("Prezzo finale (con sconto):", self.lbl_prezzo_finale)

        btn_row = QHBoxLayout()
        self.btn_nuovo = QPushButton("Nuovo")
        self.btn_nuovo.clicked.connect(self.mostraFormArticolo)
        self.btn_salva = QPushButton("Salva (aggiungi/modifica)")
        self.btn_salva.clicked.connect(self.salvaArticolo)
        self.btn_elimina = QPushButton("Elimina")
        self.btn_elimina.clicked.connect(self.eliminaArticolo)
        btn_row.addWidget(self.btn_nuovo)
        btn_row.addWidget(self.btn_salva)
        btn_row.addWidget(self.btn_elimina)
        form_layout.addRow(btn_row)

        form_box.setLayout(form_layout)
        content.addWidget(form_box, 1)

        layout.addLayout(content)

        self.mostraCatalogo()

    def mostraCatalogo(self):
        try:
            articoli = GestoreCatalogo.visualizzaCatalogo()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare il catalogo: {e}")
            return

        self.lista_articoli.clear()
        for articolo in articoli:
            nome = getattr(articolo, "nome","")
            prezzo = getattr(articolo, "prezzo", "")
            item = QListWidgetItem(f"{nome} - {prezzo} €")
            item.setData(Qt.UserRole, getattr(articolo, "id", None))
            self.lista_articoli.addItem(item)

    def onArticoloSelezionato(self, item):
        id_articolo = item.data(Qt.UserRole)
        if id_articolo is None:
            return
        try:
            articolo = GestoreCatalogo.getArticolo(id_articolo)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore nel recupero dell'articolo: {e}")
            return

        self.mostraDettagliArticolo(articolo)

    def mostraDettagliArticolo(self, articolo):
        self.articolo_selezionato_id = getattr(articolo, "id", None)
        self.edit_nome.setText(str(getattr(articolo, "nome", "")))
        self.edit_descrizione.setPlainText(str(getattr(articolo, "descrizione", "")))
        self.edit_prezzo.setText(str(getattr(articolo, "prezzo", "")))
        self.edit_quantita.setText(str(getattr(articolo, "quantita", "")))
        self.check_disponibile.setChecked(bool(getattr(articolo, "disponibile", True)))
        fornitore_id = getattr(articolo, "fornitore_id", None)
        self.edit_fornitore_id.setText("" if fornitore_id is None else str(fornitore_id))

        try:
            prezzo_finale = articolo.prezzoFinale()
            percentuale = getattr(articolo, "percentuale", 0.0)
            if percentuale:
                self.lbl_prezzo_finale.setText(f"{prezzo_finale} € (-{percentuale}%)")
            else:
                self.lbl_prezzo_finale.setText(f"{prezzo_finale} €")
        except AttributeError:
            self.lbl_prezzo_finale.setText("-")

    def mostraFormArticolo(self):
        """Pulisce il form per l'inserimento di un nuovo articolo."""
        self.articolo_selezionato_id = None
        self.edit_nome.clear()
        self.edit_descrizione.clear()
        self.edit_prezzo.clear()
        self.edit_quantita.clear()
        self.check_disponibile.setChecked(True)
        self.edit_fornitore_id.clear()
        self.lbl_prezzo_finale.setText("-")

    def _leggiDatiForm(self):
        nome = self.edit_nome.text().strip()
        descrizione = self.edit_descrizione.toPlainText().strip()
        prezzo_text = self.edit_prezzo.text().strip()
        quantita_text = self.edit_quantita.text().strip()
        fornitore_text = self.edit_fornitore_id.text().strip()

        if not nome:
            raise ValueError("Il nome dell'articolo è obbligatorio.")

        try:
            prezzo = float(prezzo_text)
        except ValueError:
            raise ValueError("Il prezzo deve essere un numero valido.")

        try:
            quantita = int(quantita_text) if quantita_text else 0
        except ValueError:
            raise ValueError("La quantità deve essere un numero intero.")

        fornitore_id = None
        if fornitore_text:
            try:
                fornitore_id = int(fornitore_text)
            except ValueError:
                fornitore_id = fornitore_text

        return {
            "nome": nome,
            "descrizione": descrizione,
            "prezzo": prezzo,
            "quantita": quantita,
            "disponibile": self.check_disponibile.isChecked(),
            "fornitore_id": fornitore_id,
        }

    def salvaArticolo(self):
        try:
            dati = self._leggiDatiForm()
        except ValueError as e:
            mostraErrore(self, str(e))
            return

        try:
            if self.articolo_selezionato_id is None:
                GestoreCatalogo.aggiungiArticolo(dati)
                mostraConferma(self, "Articolo aggiunto con successo.")
            else:
                GestoreCatalogo.modificaArticolo(self.articolo_selezionato_id, dati)
                mostraConferma(self, "Articolo modificato con successo.")
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante il salvataggio: {e}")
            return

        self.mostraFormArticolo()
        self.mostraCatalogo()

    def eliminaArticolo(self):
        if self.articolo_selezionato_id is None:
            mostraErrore(self, "Seleziona un articolo da eliminare.")
            return

        conferma = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Vuoi davvero eliminare l'articolo #{self.articolo_selezionato_id}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if conferma != QMessageBox.Yes:
            return

        try:
            GestoreCatalogo.rimuoviArticolo(self.articolo_selezionato_id)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'eliminazione: {e}")
            return

        mostraConferma(self, "Articolo eliminato.")
        self.mostraFormArticolo()
        self.mostraCatalogo()


# TAB: FORNITORI
class FornitoriTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fornitore_selezionato_id = None

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna fornitori")
        self.btn_aggiorna.clicked.connect(self.mostraFornitori)
        top_bar.addWidget(QLabel("<b>Gestione fornitori</b>"))
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        content = QHBoxLayout()

        self.lista_fornitori = QListWidget()
        self.lista_fornitori.itemClicked.connect(self.onFornitoreSelezionato)
        content.addWidget(self.lista_fornitori, 2)

        form_box = QGroupBox("Dettagli / Form fornitore")
        form_layout = QFormLayout()

        self.edit_nome = QLineEdit()
        self.edit_contatti = QLineEdit()
        self.edit_tipologia = QLineEdit()
        self.check_servizio_domicilio = QCheckBox("Servizio a domicilio")

        form_layout.addRow("Nome:", self.edit_nome)
        form_layout.addRow("Contatti:", self.edit_contatti)
        form_layout.addRow("Tipologia merce:", self.edit_tipologia)
        form_layout.addRow("", self.check_servizio_domicilio)

        btn_row = QHBoxLayout()
        self.btn_nuovo = QPushButton("Nuovo")
        self.btn_nuovo.clicked.connect(self.mostraFormFornitore)
        self.btn_salva = QPushButton("Salva (aggiungi/modifica)")
        self.btn_salva.clicked.connect(self.salvaFornitore)
        self.btn_elimina = QPushButton("Elimina")
        self.btn_elimina.clicked.connect(self.eliminaFornitore)
        btn_row.addWidget(self.btn_nuovo)
        btn_row.addWidget(self.btn_salva)
        btn_row.addWidget(self.btn_elimina)
        form_layout.addRow(btn_row)

        form_box.setLayout(form_layout)
        content.addWidget(form_box, 1)

        layout.addLayout(content)

        self.mostraFornitori()

    def mostraFornitori(self):
        try:
            fornitori = GestoreFornitori.visualizzaFornitori()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare i fornitori: {e}")
            return

        self.lista_fornitori.clear()
        for fornitore in fornitori:
            nome = getattr(fornitore, "nome", str(fornitore))
            item = QListWidgetItem(nome)
            item.setData(Qt.UserRole, getattr(fornitore, "id", None))
            self.lista_fornitori.addItem(item)

    def onFornitoreSelezionato(self, item):
        id_fornitore = item.data(Qt.UserRole)
        if id_fornitore is None:
            return
        try:
            fornitore = GestoreFornitori.getFornitore(id_fornitore)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore nel recupero del fornitore: {e}")
            return

        self.fornitore_selezionato_id = getattr(fornitore, "id", None)
        self.edit_nome.setText(str(getattr(fornitore, "nome", "")))
        self.edit_contatti.setText(str(getattr(fornitore, "contatti", "")))
        tipologia = getattr(fornitore, "tipologiaMerce", getattr(fornitore, "tipologia", ""))
        self.edit_tipologia.setText(str(tipologia))
        self.check_servizio_domicilio.setChecked(bool(getattr(fornitore, "servizioDomicilio", False)))

    def mostraFormFornitore(self):
        """Pulisce il form per l'inserimento di un nuovo fornitore."""
        self.fornitore_selezionato_id = None
        self.edit_nome.clear()
        self.edit_contatti.clear()
        self.edit_tipologia.clear()
        self.check_servizio_domicilio.setChecked(False)

    def _leggiDatiForm(self):
        return {
            "nome": self.edit_nome.text().strip(),
            "contatti": self.edit_contatti.text().strip(),
            "tipologiaMerce": self.edit_tipologia.text().strip(),
            "servizioDomicilio": self.check_servizio_domicilio.isChecked(),
        }

    def salvaFornitore(self):
        dati = self._leggiDatiForm()

        try:
            if self.fornitore_selezionato_id is None:
                GestoreFornitori.aggiungiFornitore(dati)
                mostraConferma(self, "Fornitore aggiunto con successo.")
            else:
                GestoreFornitori.modificaFornitore(self.fornitore_selezionato_id, dati)
                mostraConferma(self, "Fornitore modificato con successo.")
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante il salvataggio: {e}")
            return

        self.mostraFormFornitore()
        self.mostraFornitori()

    def eliminaFornitore(self):
        if self.fornitore_selezionato_id is None:
            mostraErrore(self, "Seleziona un fornitore da eliminare.")
            return

        conferma = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Vuoi davvero eliminare il fornitore #{self.fornitore_selezionato_id}? "
            "Gli articoli associati perderanno il riferimento al fornitore.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if conferma != QMessageBox.Yes:
            return

        try:
            GestoreFornitori.eliminaFornitore(self.fornitore_selezionato_id)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'eliminazione: {e}")
            return

        mostraConferma(self, "Fornitore eliminato.")
        self.mostraFormFornitore()
        self.mostraFornitori()


# TAB: OFFERTE
class OfferteNegozianteTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Gestione offerte</b>"))

        content = QHBoxLayout()

        # --- Sconti ---
        sconti_box = QGroupBox("Sconti")
        sconti_layout = QVBoxLayout()

        self.lista_sconti = QListWidget()
        sconti_layout.addWidget(self.lista_sconti)

        form_sconto = QFormLayout()
        self.combo_sconto_articolo = QComboBox()
        self.edit_sconto_percentuale = QLineEdit()
        self.edit_sconto_data_inizio = QLineEdit()
        self.edit_sconto_data_inizio.setPlaceholderText("YYYY-MM-DD")
        self.edit_sconto_data_fine = QLineEdit()
        self.edit_sconto_data_fine.setPlaceholderText("YYYY-MM-DD")

        form_sconto.addRow("Articolo:", self.combo_sconto_articolo)
        form_sconto.addRow("Percentuale (%):", self.edit_sconto_percentuale)
        form_sconto.addRow("Data inizio:", self.edit_sconto_data_inizio)
        form_sconto.addRow("Data fine:", self.edit_sconto_data_fine)
        sconti_layout.addLayout(form_sconto)

        btn_row_sconti = QHBoxLayout()
        self.btn_nuovo_sconto = QPushButton("Nuovo sconto")
        self.btn_nuovo_sconto.clicked.connect(self.mostraFormSconto)
        self.btn_crea_sconto = QPushButton("Crea sconto")
        self.btn_crea_sconto.clicked.connect(self.creaSconto)
        self.btn_elimina_sconto = QPushButton("Elimina selezionato")
        self.btn_elimina_sconto.clicked.connect(self.eliminaSconto)
        btn_row_sconti.addWidget(self.btn_nuovo_sconto)
        btn_row_sconti.addWidget(self.btn_crea_sconto)
        btn_row_sconti.addWidget(self.btn_elimina_sconto)
        sconti_layout.addLayout(btn_row_sconti)

        sconti_box.setLayout(sconti_layout)
        content.addWidget(sconti_box)

        # --- Promozioni ---
        promo_box = QGroupBox("Promozioni")
        promo_layout = QVBoxLayout()

        self.lista_promozioni = QListWidget()
        promo_layout.addWidget(self.lista_promozioni)

        form_promo = QFormLayout()
        self.edit_promo_descrizione = QTextEdit()
        self.edit_promo_descrizione.setMaximumHeight(60)
        self.edit_promo_data_inizio = QLineEdit()
        self.edit_promo_data_inizio.setPlaceholderText("YYYY-MM-DD")
        self.edit_promo_data_fine = QLineEdit()
        self.edit_promo_data_fine.setPlaceholderText("YYYY-MM-DD")

        form_promo.addRow("Descrizione:", self.edit_promo_descrizione)
        form_promo.addRow("Data inizio:", self.edit_promo_data_inizio)
        form_promo.addRow("Data fine:", self.edit_promo_data_fine)
        promo_layout.addLayout(form_promo)

        btn_row_promo = QHBoxLayout()
        self.btn_nuova_promo = QPushButton("Nuova promozione")
        self.btn_nuova_promo.clicked.connect(self.mostraFormPromozione)
        self.btn_crea_promo = QPushButton("Crea promozione")
        self.btn_crea_promo.clicked.connect(self.creaPromozione)
        self.btn_elimina_promo = QPushButton("Elimina selezionata")
        self.btn_elimina_promo.clicked.connect(self.eliminaPromozione)
        btn_row_promo.addWidget(self.btn_nuova_promo)
        btn_row_promo.addWidget(self.btn_crea_promo)
        btn_row_promo.addWidget(self.btn_elimina_promo)
        promo_layout.addLayout(btn_row_promo)

        promo_box.setLayout(promo_layout)
        content.addWidget(promo_box)

        layout.addLayout(content)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna offerte")
        self.btn_aggiorna.clicked.connect(self.mostraOfferte)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        self.mostraOfferte()

    def mostraOfferte(self):
        try:
            sconti = GestoreOfferte.visualizzaScontiAttivi()
            promozioni = GestoreOfferte.visualizzaOfferteAttive()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare le offerte: {e}")
            sconti = []
            mostraErrore(self, f"Impossibile caricare le promozioni: {e}")
            promozioni = []

        self.lista_sconti.clear()
        for sconto in sconti:
            percentuale = getattr(sconto, "percentuale", "")
            data_inizio = getattr(sconto, "dataInizio", "")
            data_fine = getattr(sconto, "dataFine", "")
            item = QListWidgetItem(f"Sconto {percentuale}% ({data_inizio} - {data_fine})")
            item.setData(Qt.UserRole, getattr(sconto, "id", None))
            self.lista_sconti.addItem(item)

        self.lista_promozioni.clear()
        for promo in promozioni:
            descrizione = getattr(promo, "descrizione", str(promo))
            data_inizio = getattr(promo, "dataInizio", "")
            data_fine = getattr(promo, "dataFine", "")
            item = QListWidgetItem(f"{descrizione} ({data_inizio} - {data_fine})")
            item.setData(Qt.UserRole, getattr(promo, "id", None))
            self.lista_promozioni.addItem(item)

        # Popola la lista a discesa degli articoli
        try:
            articoli = GestoreCatalogo.visualizzaCatalogo()
        except Exception as e:
            articoli = []
            mostraErrore(self, f"Impossibile caricare gli articoli nel menu: {e}")

        self.combo_sconto_articolo.clear()
        self.combo_sconto_articolo.addItem("Seleziona un articolo...", None)
        for art in articoli:
            nome = getattr(art, "nome", "Senza nome")
            art_id = getattr(art, "id", None)
            self.combo_sconto_articolo.addItem(f"{nome} (ID: {art_id})", art_id)

    def mostraFormSconto(self):
        self.combo_sconto_articolo.setCurrentIndex(0)
        self.edit_sconto_percentuale.clear()
        self.edit_sconto_data_inizio.clear()
        self.edit_sconto_data_fine.clear()

    def creaSconto(self):
        articolo_id = self.combo_sconto_articolo.currentData()
        percentuale_text = self.edit_sconto_percentuale.text().strip()
        data_inizio = self.edit_sconto_data_inizio.text().strip()
        data_fine = self.edit_sconto_data_fine.text().strip()

        if articolo_id is None:
            mostraErrore(self, "Seleziona un articolo valido per lo sconto.")
            return

        try:
            percentuale = float(percentuale_text)
        except ValueError:
            mostraErrore(self, "La percentuale deve essere un numero.")
            return

        dati = {
            "articolo_id": articolo_id,
            "percentuale": percentuale,
            "dataInizio": data_inizio,
            "dataFine": data_fine,
        }

        try:
            GestoreOfferte.creaSconto(dati)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante la creazione dello sconto: {e}")
            return

        mostraConferma(self, "Sconto creato con successo.")
        self.mostraFormSconto()
        self.mostraOfferte()

    def eliminaSconto(self):
        item = self.lista_sconti.currentItem()
        if item is None:
            mostraErrore(self, "Seleziona uno sconto da eliminare.")
            return

        id_sconto = item.data(Qt.UserRole)
        conferma = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Vuoi davvero eliminare lo sconto #{id_sconto}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if conferma != QMessageBox.Yes:
            return

        try:
            GestoreOfferte.eliminaOfferta(id_sconto, "sconto")
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'eliminazione: {e}")
            return

        mostraConferma(self, "Sconto eliminato.")
        self.mostraOfferte()

    def mostraFormPromozione(self):
        self.edit_promo_descrizione.clear()
        self.edit_promo_data_inizio.clear()
        self.edit_promo_data_fine.clear()

    def creaPromozione(self):
        descrizione = self.edit_promo_descrizione.toPlainText().strip()
        data_inizio = self.edit_promo_data_inizio.text().strip()
        data_fine = self.edit_promo_data_fine.text().strip()

        dati = {
            "descrizione": descrizione,
            "dataInizio": data_inizio,
            "dataFine": data_fine,
        }

        try:
            GestoreOfferte.creaPromozione(dati)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante la creazione della promozione: {e}")
            return

        mostraConferma(self, "Promozione creata con successo.")
        self.mostraFormPromozione()
        self.mostraOfferte()

    def eliminaPromozione(self):
        item = self.lista_promozioni.currentItem()
        if item is None:
            mostraErrore(self, "Seleziona una promozione da eliminare.")
            return

        id_promo = item.data(Qt.UserRole)
        conferma = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Vuoi davvero eliminare la promozione #{id_promo}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if conferma != QMessageBox.Yes:
            return

        try:
            GestoreOfferte.eliminaOfferta(id_promo, "promozione")
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'eliminazione: {e}")
            return

        mostraConferma(self, "Promozione eliminata.")
        self.mostraOfferte()


# TAB: ORARI
class OrariNegozianteTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna orari")
        self.btn_aggiorna.clicked.connect(self.mostraOrari)
        top_bar.addWidget(QLabel("<b>Gestione orari</b>"))
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

        # --- Form: orario settimanale ---
        settimanale_box = QGroupBox("Orario settimanale")
        settimanale_layout = QFormLayout()

        self.combo_giorno = QComboBox()
        for giorno in GIORNI_SETTIMANA:
            self.combo_giorno.addItem(giorno)
        self.edit_apertura = QLineEdit()
        self.edit_apertura.setPlaceholderText("HH:MM")
        self.edit_chiusura = QLineEdit()
        self.edit_chiusura.setPlaceholderText("HH:MM")

        settimanale_layout.addRow("Giorno:", self.combo_giorno)
        settimanale_layout.addRow("Apertura:", self.edit_apertura)
        settimanale_layout.addRow("Chiusura:", self.edit_chiusura)

        self.btn_salva_settimanale = QPushButton("Aggiorna orario settimanale")
        self.btn_salva_settimanale.clicked.connect(self.aggiornaOrarioSettimanale)
        settimanale_layout.addRow(self.btn_salva_settimanale)

        settimanale_box.setLayout(settimanale_layout)
        layout.addWidget(settimanale_box)

        # --- Form: chiusura straordinaria / orario temporaneo ---
        speciale_box = QGroupBox("Chiusura straordinaria / Orario temporaneo")
        speciale_layout = QFormLayout()

        self.edit_data_speciale = QLineEdit()
        self.edit_data_speciale.setPlaceholderText("YYYY-MM-DD")
        self.edit_apertura_speciale = QLineEdit()
        self.edit_apertura_speciale.setPlaceholderText("HH:MM (vuoto se chiusura)")
        self.edit_chiusura_speciale = QLineEdit()
        self.edit_chiusura_speciale.setPlaceholderText("HH:MM (vuoto se chiusura)")

        speciale_layout.addRow("Data:", self.edit_data_speciale)
        speciale_layout.addRow("Apertura:", self.edit_apertura_speciale)
        speciale_layout.addRow("Chiusura:", self.edit_chiusura_speciale)

        btn_row = QHBoxLayout()
        self.btn_chiusura_straordinaria = QPushButton("Imposta chiusura straordinaria")
        self.btn_chiusura_straordinaria.clicked.connect(self.impostaChiusuraStraordinaria)
        self.btn_orario_temporaneo = QPushButton("Imposta orario temporaneo")
        self.btn_orario_temporaneo.clicked.connect(self.impostaOrarioTemporaneo)
        btn_row.addWidget(self.btn_chiusura_straordinaria)
        btn_row.addWidget(self.btn_orario_temporaneo)
        speciale_layout.addRow(btn_row)

        speciale_box.setLayout(speciale_layout)
        layout.addWidget(speciale_box)

        self.mostraOrari()

    def mostraOrari(self):
        try:
            orari = GestoreOrari.visualizzaOrari()
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

    def mostraFormOrario(self):
        """Pulisce i campi del form orario."""
        self.edit_apertura.clear()
        self.edit_chiusura.clear()
        self.edit_data_speciale.clear()
        self.edit_apertura_speciale.clear()
        self.edit_chiusura_speciale.clear()

    def aggiornaOrarioSettimanale(self):
        giorno = self.combo_giorno.currentText()
        apertura = self.edit_apertura.text().strip()
        chiusura = self.edit_chiusura.text().strip()

        nuovi_orari = {"apertura": apertura, "chiusura": chiusura}

        try:
            GestoreOrari.aggiornaOrarioSettimanale(giorno, nuovi_orari)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'aggiornamento dell'orario: {e}")
            return

        mostraConferma(self, f"Orario di {giorno} aggiornato.")
        self.mostraOrari()

    def impostaChiusuraStraordinaria(self):
        data = self.edit_data_speciale.text().strip()
        if not data:
            mostraErrore(self, "Inserisci una data per la chiusura straordinaria.")
            return

        try:
            GestoreOrari.impostaChiusuraStraordinaria(data)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'impostazione della chiusura: {e}")
            return

        mostraConferma(self, f"Chiusura straordinaria impostata per il {data}.")
        self.mostraFormOrario()
        self.mostraOrari()

    def impostaOrarioTemporaneo(self):
        data = self.edit_data_speciale.text().strip()
        apertura = self.edit_apertura_speciale.text().strip()
        chiusura = self.edit_chiusura_speciale.text().strip()

        if not data:
            mostraErrore(self, "Inserisci una data per l'orario temporaneo.")
            return

        orario = {"apertura": apertura, "chiusura": chiusura}

        try:
            GestoreOrari.impostaOrarioTemporaneo(data, orario)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'impostazione dell'orario temporaneo: {e}")
            return

        mostraConferma(self, f"Orario temporaneo impostato per il {data}.")
        self.mostraFormOrario()
        self.mostraOrari()


# TAB: NOTIFICHE / RICHIESTE
class NotificheTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna notifiche")
        self.btn_aggiorna.clicked.connect(self.mostraNotifiche)
        top_bar.addWidget(QLabel("<b>Notifiche</b>"))
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        self.tabella = QTableWidget()
        self.tabella.setColumnCount(5)
        self.tabella.setHorizontalHeaderLabels(
            ["ID", "Destinatario", "Tipo", "Messaggio", "Richiesta ID"]
        )
        self.tabella.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabella.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabella)

        btn_row = QHBoxLayout()
        self.btn_conferma_preventivo = QPushButton("Conferma preventivo")
        self.btn_conferma_preventivo.clicked.connect(self.confermaPreventivo)
        self.btn_conferma_appuntamento = QPushButton("Conferma appuntamento")
        self.btn_conferma_appuntamento.clicked.connect(self.confermaAppuntamento)
        btn_row.addWidget(self.btn_conferma_preventivo)
        btn_row.addWidget(self.btn_conferma_appuntamento)
        layout.addLayout(btn_row)

        self.mostraNotifiche()

    def mostraNotifiche(self):
        try:
            notifiche = GestoreNotifiche.visualizzaNotifiche()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare le notifiche: {e}")
            return

        self.tabella.setRowCount(len(notifiche))
        for row, notifica in enumerate(notifiche):
            id_n = getattr(notifica, "id", "")
            destinatario = getattr(notifica, "destinatario", "")
            tipo = getattr(notifica, "tipo", "")
            messaggio = getattr(notifica, "messaggio", "")
            richiesta_id = getattr(notifica, "richiestaId", "")

            self.tabella.setItem(row, 0, QTableWidgetItem(str(id_n)))
            self.tabella.setItem(row, 1, QTableWidgetItem(str(destinatario)))
            self.tabella.setItem(row, 2, QTableWidgetItem(str(tipo)))
            self.tabella.setItem(row, 3, QTableWidgetItem(str(messaggio)))
            self.tabella.setItem(row, 4, QTableWidgetItem(str(richiesta_id)))

    def _getRichiestaIdSelezionata(self):
        row = self.tabella.currentRow()
        if row < 0:
            mostraErrore(self, "Seleziona una notifica relativa a una richiesta.")
            return None

        item = self.tabella.item(row, 4)
        if item is None or not item.text():
            mostraErrore(self, "La notifica selezionata non è associata a una richiesta.")
            return None

        richiesta_id_text = item.text()
        try:
            return int(richiesta_id_text)
        except ValueError:
            return richiesta_id_text

    def confermaPreventivo(self):
        richiesta_id = self._getRichiestaIdSelezionata()
        if richiesta_id is None:
            return

        try:
            GestoreNotifiche.confermaPreventivo(richiesta_id)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante la conferma: {e}")
            return

        mostraConferma(self, "Preventivo confermato.")
        self.mostraNotifiche()

    def confermaAppuntamento(self):
        richiesta_id = self._getRichiestaIdSelezionata()
        if richiesta_id is None:
            return

        try:
            GestoreNotifiche.confermaAppuntamento(richiesta_id)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante la conferma: {e}")
            return

        mostraConferma(self, "Appuntamento confermato.")
        self.mostraNotifiche()


# TAB: CONSEGNE
class ConsegneNegozianteTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna consegne")
        self.btn_aggiorna.clicked.connect(self.mostraConsegne)
        top_bar.addWidget(QLabel("<b>Gestione consegne</b>"))
        top_bar.addStretch()
        top_bar.addWidget(self.btn_aggiorna)
        layout.addLayout(top_bar)

        self.tabella = QTableWidget()
        self.tabella.setColumnCount(6)
        self.tabella.setHorizontalHeaderLabels(
            ["ID", "Cliente ID", "Regione", "Città", "Indirizzo", "Stato"]
        )
        self.tabella.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabella.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabella.itemSelectionChanged.connect(self.onConsegnaSelezionata)
        layout.addWidget(self.tabella)

        form_box = QGroupBox("Aggiorna stato consegna")
        form_layout = QFormLayout()

        self.combo_stato = QComboBox()
        for stato in STATI_CONSEGNA:
            self.combo_stato.addItem(stato)

        form_layout.addRow("Nuovo stato:", self.combo_stato)

        self.btn_aggiorna_stato = QPushButton("Aggiorna stato")
        self.btn_aggiorna_stato.clicked.connect(self.aggiornaStatoConsegna)
        form_layout.addRow(self.btn_aggiorna_stato)

        form_box.setLayout(form_layout)
        layout.addWidget(form_box)

        self.mostraConsegne()

    def mostraConsegne(self):
        try:
            consegne = GestoreConsegne.cercaConsegne()
        except Exception as e:
            mostraErrore(self, f"Impossibile caricare le consegne: {e}")
            return

        self.tabella.setRowCount(len(consegne))
        for row, consegna in enumerate(consegne):
            id_c = getattr(consegna, "id", "")
            cliente_id = getattr(consegna, "clienteId", "")
            try:
                cliente_id = consegna.getClienteId()
            except AttributeError:
                pass
            regione = getattr(consegna, "regione", "")
            citta = getattr(consegna, "citta", "")
            via = getattr(consegna, "via", "")
            civico = getattr(consegna, "civico", "")
            indirizzo = f"{via} {civico}"
            try:
                stato = consegna.getStato()
            except AttributeError:
                stato = getattr(consegna, "stato", "")

            self.tabella.setItem(row, 0, QTableWidgetItem(str(id_c)))
            self.tabella.setItem(row, 1, QTableWidgetItem(str(cliente_id)))
            self.tabella.setItem(row, 2, QTableWidgetItem(str(regione)))
            self.tabella.setItem(row, 3, QTableWidgetItem(str(citta)))
            self.tabella.setItem(row, 4, QTableWidgetItem(str(indirizzo)))
            self.tabella.setItem(row, 5, QTableWidgetItem(str(stato)))

    def onConsegnaSelezionata(self):
        """mostraFormStatoConsegna: preseleziona lo stato attuale della consegna."""
        row = self.tabella.currentRow()
        if row < 0:
            return
        item_stato = self.tabella.item(row, 5)
        if item_stato is None:
            return
        stato_attuale = item_stato.text()
        index = self.combo_stato.findText(stato_attuale)
        if index >= 0:
            self.combo_stato.setCurrentIndex(index)

    def aggiornaStatoConsegna(self):
        row = self.tabella.currentRow()
        if row < 0:
            mostraErrore(self, "Seleziona una consegna da aggiornare.")
            return

        id_item = self.tabella.item(row, 0)
        if id_item is None:
            return
        id_text = id_item.text()
        try:
            id_consegna = int(id_text)
        except ValueError:
            id_consegna = id_text

        nuovo_stato = self.combo_stato.currentText()

        try:
            GestoreConsegne.aggiornaStatoConsegna(id_consegna, nuovo_stato)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'aggiornamento dello stato: {e}")
            return

        mostraConferma(self, f"Stato della consegna #{id_consegna} aggiornato a '{nuovo_stato}'.")
        self.mostraConsegne()

class SessionControlWidget(QWidget):

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
class InterfacciaNegoziante(QMainWindow):

    def __init__(self, negoziante_id=None, parent=None):
        super().__init__(parent)
        self.negoziante_id = negoziante_id

        self.setWindowTitle("Negozio - Area Negoziante")
        self.resize(1000, 700)

        self.mostraDashboardNegoziante()

    def mostraDashboardNegoziante(self):
        # Main container layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(CatalogoNegozianteTab(self), "Catalogo")
        tabs.addTab(FornitoriTab(self), "Fornitori")
        tabs.addTab(OfferteNegozianteTab(self), "Offerte")
        tabs.addTab(OrariNegozianteTab(self), "Orari")
        tabs.addTab(NotificheTab(self), "Notifiche")
        tabs.addTab(ConsegneNegozianteTab(self), "Consegne")

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


def start(negoziante_id=None):
    finestra = InterfacciaNegoziante(negoziante_id=negoziante_id)
    return finestra


if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = start()
    finestra.show()
    sys.exit(app.exec_())