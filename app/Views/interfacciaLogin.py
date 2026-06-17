"""
InterfacciaLogin - GUI PyQt5 per login e registrazione

Implementa le funzioni della classe boundary "InterfacciaLogin":
    - mostraFormLogin
    - mostraFormRegistrazione
    - mostraMessaggio / mostraConferma / mostraErrore (QMessageBox)
    - reindirizzaPerRuolo -> emette segnale loginEffettuato(utente)

Controller utilizzati:
    - sistemaAccesso (login, sessione)
    - sistemaRegistrazione (registrazione nuovo utente)

Dopo il login riuscito, viene emesso il segnale `loginEffettuato` con
l'oggetto utente autenticato. Main.py si occupa di aprire l'interfaccia
corretta (InterfacciaCliente o InterfacciaNegoziante) in base al ruolo.
"""

import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QGroupBox,
)


# =====================================================================
# IMPORT CONTROLLER
# =====================================================================
from app.Services.sistemaAccesso import SistemaAccesso
from app.Services.sistemaRegistrazione import SistemaRegistrazione




# WIDGET: FORM LOGIN
class FormLoginWidget(QWidget):
    """mostraFormLogin()"""

    def __init__(self, finestra_login, parent=None):
        super().__init__(parent)
        self.finestra_login = finestra_login

        layout = QVBoxLayout(self)
        layout.addStretch()

        box = QGroupBox("Accedi")
        form_layout = QFormLayout()

        self.edit_username = QLineEdit()
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Username:", self.edit_username)
        form_layout.addRow("Password:", self.edit_password)

        self.btn_login = QPushButton("Accedi")
        self.btn_login.clicked.connect(self.inviaCredenziali)
        form_layout.addRow(self.btn_login)

        self.btn_vai_registrazione = QPushButton("Non hai un account? Registrati")
        self.btn_vai_registrazione.clicked.connect(self.finestra_login.mostraFormRegistrazione)
        form_layout.addRow(self.btn_vai_registrazione)

        box.setLayout(form_layout)
        layout.addWidget(box)
        layout.addStretch()

        # Permetti login premendo Invio nel campo password
        self.edit_password.returnPressed.connect(self.inviaCredenziali)

    def inviaCredenziali(self):
        username = self.edit_username.text().strip()
        password = self.edit_password.text()

        if not username or not password:
            mostraErrore(self, "Inserisci username e password.")
            return

        try:
            utente = SistemaAccesso.inviaCredenziali(username, password)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante l'accesso: {e}")
            return

        mostraConferma(self, f"Accesso riuscito. Benvenuto, {utente.getUsername()}!")
        self.edit_password.clear()

        self.finestra_login.reindirizzaPerRuolo(utente)


# WIDGET: FORM REGISTRAZIONE
class FormRegistrazioneWidget(QWidget):
    """mostraFormRegistrazione()"""

    def __init__(self, finestra_login, parent=None):
        super().__init__(parent)
        self.finestra_login = finestra_login

        layout = QVBoxLayout(self)
        layout.addStretch()

        box = QGroupBox("Registrazione")
        form_layout = QFormLayout()

        self.edit_username = QLineEdit()
        self.edit_email = QLineEdit()
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_conferma_password = QLineEdit()
        self.edit_conferma_password.setEchoMode(QLineEdit.Password)
        self.combo_ruolo = QComboBox()
        self.combo_ruolo.addItem("Cliente", "cliente")
        #self.combo_ruolo.addItem("Negoziante", "negoziante")

        form_layout.addRow("Username:", self.edit_username)
        form_layout.addRow("Email:", self.edit_email)
        form_layout.addRow("Password:", self.edit_password)
        form_layout.addRow("Conferma password:", self.edit_conferma_password)
        form_layout.addRow("Ruolo:", self.combo_ruolo)

        info_password = QLabel(
            "La password deve contenere 6-20 caratteri, almeno una\n"
            "lettera minuscola, una maiuscola, un numero e uno dei\n"
            "simboli @ $ # %"
        )
        info_password.setWordWrap(True)
        form_layout.addRow(info_password)

        self.btn_registrati = QPushButton("Registrati")
        self.btn_registrati.clicked.connect(self.inviaRegistrazione)
        form_layout.addRow(self.btn_registrati)

        self.btn_vai_login = QPushButton("Hai già un account? Accedi")
        self.btn_vai_login.clicked.connect(self.finestra_login.mostraFormLogin)
        form_layout.addRow(self.btn_vai_login)

        box.setLayout(form_layout)
        layout.addWidget(box)
        layout.addStretch()

    def inviaRegistrazione(self):
        username = self.edit_username.text().strip()
        email = self.edit_email.text().strip()
        password = self.edit_password.text()
        conferma_password = self.edit_conferma_password.text()
        ruolo = self.combo_ruolo.currentData()

        if not username or not email or not password or not conferma_password:
            mostraErrore(self, "Compila tutti i campi.")
            return

        if not SistemaRegistrazione.verificaFormatoEmail(email):
            mostraErrore(self, "Formato email non valido.")
            return

        if not SistemaRegistrazione.confrontaPassword(password, conferma_password):
            mostraErrore(self, "Le password non coincidono.")
            return

        if not SistemaRegistrazione.verificaCriteriPassword(password):
            mostraErrore(
                self,
                "La password non rispetta i criteri richiesti: "
                "6-20 caratteri, almeno una minuscola, una maiuscola, "
                "un numero e uno dei simboli @ $ # %.",
            )
            return

        dati = {
            "username": username,
            "email": email,
            "password": password,
            "ruolo": ruolo,
        }

        try:
            SistemaRegistrazione.inviaRegistrazione(dati)
        except ValueError as e:
            mostraErrore(self, str(e))
            return
        except Exception as e:
            mostraErrore(self, f"Errore durante la registrazione: {e}")
            return

        mostraConferma(self, "Registrazione completata. Ora puoi accedere.")
        self.edit_username.clear()
        self.edit_email.clear()
        self.edit_password.clear()
        self.edit_conferma_password.clear()
        self.combo_ruolo.setCurrentIndex(0)

        self.finestra_login.mostraFormLogin()


# FINESTRA PRINCIPALE: LOGIN
class InterfacciaLogin(QMainWindow):
    """
    mostraFormLogin() / mostraFormRegistrazione()
    mostraMessaggio() / mostraConferma() / mostraErrore()
    reindirizzaPerRuolo(utente) -> emette segnale loginEffettuato
    """

    # Segnale emesso dopo login riuscito, porta l'oggetto utente
    loginEffettuato = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Negozio - Accesso")
        self.resize(420, 380)

        self.stack = QStackedWidget()

        self.form_login = FormLoginWidget(self)
        self.form_registrazione = FormRegistrazioneWidget(self)

        self.stack.addWidget(self.form_login)
        self.stack.addWidget(self.form_registrazione)

        self.setCentralWidget(self.stack)

        self.mostraFormLogin()

    def mostraFormLogin(self):
        self.setWindowTitle("Negozio - Accesso")
        self.stack.setCurrentWidget(self.form_login)

    def mostraFormRegistrazione(self):
        self.setWindowTitle("Negozio - Registrazione")
        self.stack.setCurrentWidget(self.form_registrazione)

    def reindirizzaPerRuolo(self, utente):
        """Emette il segnale loginEffettuato con l'utente autenticato."""
        self.loginEffettuato.emit(utente)



def mostraMessaggio(parent, messaggio):
    QMessageBox.information(parent, "Messaggio", messaggio)


def mostraConferma(parent, messaggio):
    QMessageBox.information(parent, "Conferma", messaggio)


def mostraErrore(parent, messaggio):
    QMessageBox.critical(parent, "Errore", messaggio)


# AVVIO APPLICAZIONE
if __name__ == "__main__":
    app = QApplication(sys.argv)

    finestra = InterfacciaLogin()
    finestra.show()

    sys.exit(app.exec_())