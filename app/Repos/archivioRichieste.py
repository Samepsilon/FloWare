import csv
import os
from app.Models.richiesta import Richiesta
from app.Models.notifica import Notifica
from app.Repos.notificaRepository import NotificaRepository

class ArchivioRichieste:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "richieste.csv")
    COLONNE = ["id", "tipo", "stato", "data", "ora", "contatti", "descrizione", "clienteId"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
            righe = []
            for r in csv.DictReader(f):
                righe.append(Richiesta(
                    id=int(r["id"]),
                    tipo=r["tipo"],
                    stato=r["stato"],
                    data=r["data"],
                    ora=r["ora"],
                    contatti=r["contatti"],
                    descrizione=r["descrizione"],
                    clienteId=int(r["clienteId"]) if r["clienteId"] else None,
                ))
            return righe

    @classmethod
    def scrivi(cls, richieste):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
            w.writeheader()
            for r in richieste:
                w.writerow({
                    "id": r.id,
                    "tipo": r.tipo,
                    "stato": r.stato,
                    "data": r.data,
                    "ora": r.ora,
                    "contatti": r.contatti,
                    "descrizione": r.descrizione,
                    "clienteId": r.clienteId if r.clienteId is not None else "",
                })

    @classmethod
    def salva(cls, richiesta):
        tutti = cls.leggi()
        if richiesta.id is None:
            richiesta.id = max((r.id for r in tutti), default=0) + 1
            tutti.append(richiesta)
        else:
            tutti = [richiesta if r.id == richiesta.id else r for r in tutti]
        cls.scrivi(tutti)
        return richiesta

    @classmethod
    def trovaPerId(cls, id):
        for r in cls.leggi():
            if r.id == id:
                return r
        return None

    @classmethod
    def trovaPerCliente(cls, clienteId):
        return [r for r in cls.leggi() if r.clienteId == clienteId]

    @classmethod
    def getDettagliConferma(cls, id):
        r = cls.trovaPerId(id)
        if r is None or r.stato != "confermata":
            return None
        return r

    @classmethod
    def findNotificheNonLette(cls):
        return NotificaRepository.notificheNonLette()

    @classmethod
    def verificaAnnullamento(cls, richiesta):
        return richiesta is not None and richiesta.stato == "in attesa"

    @classmethod
    def cercaRichiesta(cls, richiesta):
        for r in cls.leggi():
            if r.id == richiesta.id:
                return r
        return None

    @classmethod
    def aggiornaStatoRichiesta(cls, richiesta, stato):
        if richiesta is None:
            return None
        richiesta.setStato(stato)
        return cls.salva(richiesta)

    @classmethod
    def richiesteInAttesa(cls):
        return [r for r in cls.leggi() if r.stato == "in attesa"]

    @classmethod
    def eliminaRichiesta(cls, id):
        cls.scrivi([r for r in cls.leggi() if r.id != id])
