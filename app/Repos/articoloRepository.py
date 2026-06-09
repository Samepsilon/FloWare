import csv
import os
from app.Models.articolo import Articolo


FILE = "data/articoli.csv"
COLONNE = ["id", "nome", "descrizione", "prezzo", "disponibile", "fornitore_id", "sconto"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            righe.append(Articolo(
                id=int(r["id"]),
                nome=r["nome"],
                descrizione=r["descrizione"],
                prezzo=float(r["prezzo"]),
                disponibile=r["disponibile"] == "True",
                fornitore_id=int(r["fornitore_id"]) if r["fornitore_id"] else None,
                sconto=float(r["sconto"]),
            ))
        return righe

def scrivi(articoli):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for a in articoli:
            w.writerow({
                "id": a.id,
                "nome": a.nome,
                "descrizione": a.descrizione,
                "prezzo": a.prezzo,
                "disponibile": a.disponibile,
                "fornitore_id": a.fornitore_id if a.fornitore_id is not None else "",
                "sconto": a.sconto,
            })

def salva_articolo(articolo):
    tutti = leggi()
    if articolo.id is None:
        articolo.id = max((a.id for a in tutti), default=0) + 1
        tutti.append(articolo)
    else:
        tutti = [articolo if a.id == articolo.id else a for a in tutti]
    scrivi(tutti)
    return articolo

def trova_articolo(id):
    for a in leggi():
        if a.id == id:
            return a
    return None

def articoli_del_fornitore(fornitore_id):
    return [a for a in leggi() if a.fornitore_id == fornitore_id]


def elimina_articolo(id):
    tutti = leggi()
    filtrati = [a for a in tutti if a.id != id]
    scrivi(filtrati)


