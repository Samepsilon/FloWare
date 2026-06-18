import csv
import os
from app.Models.articolo import Articolo
from app.Models.sconto import Sconto


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

def salvaArticolo(articolo):
    tutti = leggi()
    if articolo.id is None:
        articolo.id = max((a.id for a in tutti), default=0) + 1
        tutti.append(articolo)
    else:
        tutti = [articolo if a.id == articolo.id else a for a in tutti]
    scrivi(tutti)
    return articolo

def trovaArticolo(id):
    for a in leggi():
        if a.id == id:
            return a
    return None

def articoliDelFornitore(fornitore_id):
    return [a for a in leggi() if a.fornitore_id == fornitore_id]


def rimuoviArticolo(id):
    tutti = leggi()
    filtrati = [a for a in tutti if a.id != id]
    scrivi(filtrati)
def getArticoliDisponibili():
    tutti = leggi()

def mostraCatalogo():


def verificaArticolo():

def associaScontoAdArticolo(articolo, sconto)

def rimuoviRiferimentoArticolo(articolo):
    

