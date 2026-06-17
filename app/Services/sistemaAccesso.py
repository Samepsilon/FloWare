import re
from app.Repos.utenteRepository import UtenteRepository

class SistemaAccesso:
    mail_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    sessione = {"utente": None, "ruolo": None}

    @classmethod
    def inviaCredenziali(cls, username, password):
        utente = UtenteRepository.trovaPerCredenziali(username, password)
        if utente is None:
            raise ValueError("Credenziali non valide.")
        cls.impostaSessione(utente.getRuolo())
        cls.sessione["utente"] = utente
        return utente

    @classmethod
    def impostaSessione(cls, ruolo):
        cls.sessione["ruolo"] = ruolo

    @classmethod
    def reindirizzaPerRuolo(cls, ruolo):
        if ruolo == "cliente":
            return "InterfacciaCliente"
        if ruolo == "negoziante":
            return "InterfacciaNegoziante"
        raise ValueError(f"Ruolo non riconosciuto: {ruolo}")

    @classmethod
    def getSessione(cls):
        return cls.sessione.copy()

    @classmethod
    def verificaFormatoEmail(cls, email):
        return bool(re.match(cls.mail_pattern, email))

    @classmethod
    def confrontaPassword(cls, password, conferma):
        return password == conferma
