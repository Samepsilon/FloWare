import csv
import os
from app.Models.orario import Orario

class OrarioRepository:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "orari.csv")
    COLONNE = ["id", "giorno", "apertura", "chiusura", "tipo", "dataSpecifica"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
            righe = []
            for r in csv.DictReader(f):
                righe.append(Orario(
                    id=int(r["id"]),
                    giorno=r["giorno"] if r["giorno"] else None,
                    apertura=r["apertura"] if r["apertura"] else None,
                    chiusura=r["chiusura"] if r["chiusura"] else None,
                    tipo=r["tipo"],
                    dataSpecifica=r["dataSpecifica"] if r["dataSpecifica"] else None,
                ))
            return righe

    @classmethod
    def scrivi(cls, orari):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
            w.writeheader()
            for o in orari:
                w.writerow({
                    "id": o.id,
                    "giorno": o.giorno if o.giorno is not None else "",
                    "apertura": o.apertura if o.apertura is not None else "",
                    "chiusura": o.chiusura if o.chiusura is not None else "",
                    "tipo": o.tipo,
                    "dataSpecifica": o.dataSpecifica if o.dataSpecifica is not None else "",
                })

    @classmethod
    def salvaOrario(cls, orario):
        tutti = cls.leggi()
        if orario.id is None:
            orario.id = max((o.id for o in tutti), default=0) + 1
            tutti.append(orario)
        else:
            tutti = [orario if o.id == orario.id else o for o in tutti]
        cls.scrivi(tutti)
        return orario

    @classmethod
    def getOrariSettimanali(cls):
        return [o for o in cls.leggi() if o.tipo == "settimanale"]

    @classmethod
    def cercaOrari(cls):
        return cls.leggi()

    @classmethod
    def cercaOrarioPerGiorno(cls, giorno, tipo="settimanale"):
        for o in cls.leggi():
            if o.giorno == giorno and o.tipo == tipo:
                return o
        return None

    @classmethod
    def cercaOrarioPerData(cls, data):
        for o in cls.leggi():
            if o.tipo == "speciale" and str(o.dataSpecifica) == str(data):
                return o
        return None

    @classmethod
    def nuovoOrario(cls, giorno, nuoviOrari, tipo="settimanale"):
        dati = nuoviOrari if isinstance(nuoviOrari, dict) else {}
        orario = Orario(
            giorno=giorno,
            apertura=dati.get("apertura"),
            chiusura=dati.get("chiusura"),
            tipo=tipo,
            dataSpecifica=dati.get("dataSpecifica"),
        )
        return cls.salvaOrario(orario)

    @classmethod
    def aggiornaOrario(cls, id, nuoviOrari):
        orario = cls.trovaPerId(id)
        if orario is None:
            return None
        dati = nuoviOrari if isinstance(nuoviOrari, dict) else {}
        orario.aggiornaOrario(
            nuovaApertura=dati.get("apertura"),
            nuovaChiusura=dati.get("chiusura"),
        )
        if "giorno" in dati:
            orario.giorno = dati["giorno"]
        if "tipo" in dati:
            orario.tipo = dati["tipo"]
        if "dataSpecifica" in dati:
            orario.dataSpecifica = dati["dataSpecifica"]
        return cls.salvaOrario(orario)

    @classmethod
    def trovaPerId(cls, id):
        for o in cls.leggi():
            if o.id == id:
                return o
        return None

    @classmethod
    def eliminaOrario(cls, id):
        cls.scrivi([o for o in cls.leggi() if o.id != id])
