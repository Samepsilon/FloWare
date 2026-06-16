import csv
import os
from app.Models.orario import Orario
BASE_DIR = os.path.abspath("..")
FILE = BASE_DIR + "/Data/orari.csv"

COLONNE = ["id", "giorno", "apertura", "chiusura", "tipo", "dataSpecifica"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
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


def scrivi(orari):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
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


def salvaOrario(orario):
    tutti = leggi()
    if orario.id is None:
        orario.id = max((o.id for o in tutti), default=0) + 1
        tutti.append(orario)
    else:
        tutti = [orario if o.id == orario.id else o for o in tutti]
    scrivi(tutti)
    return orario


def getOrariSettimanali():
    return [o for o in leggi() if o.tipo == "settimanale"]


def cercaOrari():
    return leggi()


def cercaOrarioPerGiorno(giorno, tipo="settimanale"):
    for o in leggi():
        if o.giorno == giorno and o.tipo == tipo:
            return o
    return None


def cercaOrarioPerData(data):
    for o in leggi():
        if o.tipo == "speciale" and str(o.dataSpecifica) == str(data):
            return o
    return None


def nuovoOrario(giorno, nuoviOrari, tipo="settimanale"):
    dati = nuoviOrari if isinstance(nuoviOrari, dict) else {}
    orario = Orario(
        giorno=giorno,
        apertura=dati.get("apertura"),
        chiusura=dati.get("chiusura"),
        tipo=tipo,
        dataSpecifica=dati.get("dataSpecifica"),
    )
    return salvaOrario(orario)


def aggiornaOrario(id, nuoviOrari):
    orario = trovaPerId(id)
    if orario is None:
        return None
    dati = nuoviOrari if isinstance(nuoviOrari, dict) else {}
    orario.impostaNuoviOrari(dati)
    orario.aggiornaOrario()
    if "giorno" in dati:
        orario.giorno = dati["giorno"]
    if "tipo" in dati:
        orario.tipo = dati["tipo"]
    if "dataSpecifica" in dati:
        orario.dataSpecifica = dati["dataSpecifica"]
    return salvaOrario(orario)


def trovaPerId(id):
    for o in leggi():
        if o.id == id:
            return o
    return None


def eliminaOrario(id):
    scrivi([o for o in leggi() if o.id != id])
