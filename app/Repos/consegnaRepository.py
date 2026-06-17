import csv
import os
from app.Models.consegna import Consegna

class ConsegnaRepository:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "consegne.csv")
    COLONNE = ["id", "regione", "citta", "via", "civico", "stato", "clienteId"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
            righe = []
            for r in csv.DictReader(f):
                righe.append(Consegna(
                    id=int(r["id"]),
                    regione=r["regione"],
                    citta=r.get("citta") or r.get("città", ""),
                    via=r["via"],
                    civico=r["civico"],
                    stato=r["stato"] if r["stato"] else None,
                    clienteId=int(r["clienteId"]) if r["clienteId"] else None,
                ))
            return righe

    @classmethod
    def scrivi(cls, consegne):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
            w.writeheader()
            for c in consegne:
                w.writerow({
                    "id": c.id,
                    "regione": c.regione,
                    "citta": c.citta,
                    "via": c.via,
                    "civico": c.civico,
                    "stato": c.stato if c.stato is not None else "",
                    "clienteId": c.clienteId if c.clienteId is not None else "",
                })

    @classmethod
    def salva(cls, consegna):
        tutti = cls.leggi()
        if consegna.id is None:
            consegna.id = max((c.id for c in tutti), default=0) + 1
            tutti.append(consegna)
        else:
            tutti = [consegna if c.id == consegna.id else c for c in tutti]
        cls.scrivi(tutti)
        return consegna

    @classmethod
    def trovaPerId(cls, id):
        for c in cls.leggi():
            if c.id == id:
                return c
        return None

    @classmethod
    def cercaConsegne(cls):
        return cls.leggi()

    @classmethod
    def consegneDelCliente(cls, clienteId):
        return [c for c in cls.leggi() if c.clienteId == clienteId]

    @classmethod
    def consegnePerStato(cls, stato, clienteId):
        listConsegna = [c for c in cls.leggi() if c.clienteId == clienteId]
        return [c for c in listConsegna if c.stato == stato]

    @classmethod
    def eliminaConsegna(cls, id):
        cls.scrivi([c for c in cls.leggi() if c.id != id])
