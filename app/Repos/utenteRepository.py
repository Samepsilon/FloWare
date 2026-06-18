import csv
import os
from app.Models.cliente import Cliente
from app.Models.negoziante import Negoziante

class UtenteRepository:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "utenti.csv")
    COLONNE = ["id", "ruolo", "username", "email", "password"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
            utenti = []
            for r in csv.DictReader(f):
                if r["ruolo"] == "cliente":
                    utenti.append(Cliente(
                        id=int(r["id"]),
                        username=r["username"],
                        email=r["email"],
                        password=r["password"],
                    ))
                else:
                    utenti.append(Negoziante(
                        id=int(r["id"]),
                        username=r["username"],
                        email=r["email"],
                        password=r["password"],
                    ))
            return utenti

    @classmethod
    def scrivi(cls, utenti):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
            w.writeheader()
            for u in utenti:
                w.writerow({
                    "id": u.id,
                    "ruolo": u.ruolo,
                    "username": u.username,
                    "email": u.email,
                    "password": u.password,
                })

    @classmethod
    def salva(cls, nuovoCliente):
        """
        save the object Cliente (Utente)(only cliente can be created this way) inside the csv file
        """
        tutti = cls.leggi()
        if nuovoCliente.id is None:
            nuovoCliente.id = max((u.id for u in tutti), default=0) + 1
            tutti.append(nuovoCliente)
        else:
            tutti = [nuovoCliente if u.id == nuovoCliente.id else u for u in tutti]
        cls.scrivi(tutti)
        return nuovoCliente

    @classmethod
    def trovaPerCredenziali(cls, username, password):
        for u in cls.leggi():
            if u.username == username and u.password == password:
                return u
        return None

    @classmethod
    def trovaPerId(cls, id):
        for u in cls.leggi():
            if u.id == id:
                return u
        return None

    @classmethod
    def trovaPerUsername(cls, username):
        for u in cls.leggi():
            if u.username == username:
                return u
        return None

    @classmethod
    def trovaPerEmail(cls, email):
        for u in cls.leggi():
            if u.email == email:
                return u
        return None

    @classmethod
    def tuttiClienti(cls):
        return [u for u in cls.leggi() if u.ruolo == "cliente"]

    @classmethod
    def tuttiNegozianti(cls):
        return [u for u in cls.leggi() if u.ruolo == "negoziante"]

    @classmethod
    def eliminaUtente(cls, id):
        tutti = cls.leggi()
        cls.scrivi([u for u in tutti if u.id != id])
