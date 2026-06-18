import csv
import os
from app.Models.orario import Orario

FILE = "data/orari.csv"
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


def salva_orario(orario):
    tutti = leggi()
    if orario.id is None:
        orario.id = max((o.id for o in tutti), default=0) + 1
        tutti.append(orario)
    else:
        tutti = [orario if o.id == orario.id else o for o in tutti]
    scrivi(tutti)
    return orario


def trova_orario(id):
    for o in leggi():
        if o.id == id:
            return o
    return None


def trovaPerId(id):
    return trova_orario(id)


def orari_settimanali():
    """Restituisce tutti gli orari di tipo settimanale"""
    return [o for o in leggi() if o.tipo == "settimanale"]


def orari_speciali():
    """Restituisce tutti gli orari di tipo speciale"""
    return [o for o in leggi() if o.tipo == "speciale"]


def orari_per_giorno(giorno):
    """Restituisce gli orari settimanali per un giorno specifico"""
    return [o for o in leggi() if o.tipo == "settimanale" and o.giorno == giorno]


def orari_per_data(dataSpecifica):
    """Restituisce gli orari speciali per una data specifica"""
    return [o for o in leggi() if o.tipo == "speciale" and o.dataSpecifica == dataSpecifica]


def elimina_orario(id):
    tutti = leggi()
    filtrati = [o for o in tutti if o.id != id]
    scrivi(filtrati)


def elimina_orari_per_giorno(giorno):
    """Elimina tutti gli orari settimanali per un giorno"""
    tutti = leggi()
    filtrati = [o for o in tutti if not (o.tipo == "settimanale" and o.giorno == giorno)]
    scrivi(filtrati)