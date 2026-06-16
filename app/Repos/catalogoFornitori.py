import csv
import os
from app.Models.fornitore import Fornitore
BASE_DIR = os.path.abspath("..")
FILE = BASE_DIR + "/Data/fornitori.csv"

COLONNE = ["id", "nome", "contatti", "tipologia", "servizioDomicilio"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            righe.append(Fornitore(
                id=int(r["id"]),
                nome=r["nome"],
                contatti=r["contatti"],
                tipologiaMerce=r["tipologia"],
                servizioDomicilio=r["servizioDomicilio"] == "True",
            ))
        return righe


def scrivi(fornitori):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for f_ in fornitori:
            w.writerow({
                "id": f_.id,
                "nome": f_.nome,
                "contatti": f_.contatti,
                "tipologia": f_.tipologiaMerce,
                "servizioDomicilio": f_.servizioDomicilio,
            })


def salvaFornitore(fornitore):
    tutti = leggi()
    if fornitore.id is None:
        fornitore.id = max((f.id for f in tutti), default=0) + 1
        tutti.append(fornitore)
    else:
        tutti = [fornitore if f.id == fornitore.id else f for f in tutti]
    scrivi(tutti)
    return fornitore


def cercaFornitori(id):
    for f in leggi():
        if f.id == id:
            return f
    return None


def caricaListaFornitori():
    return leggi()


def cercaFornitore(Nome):
    for f in leggi():
        if f.nome == Nome:
            return f
    return None


def aggiornaFornitore(id, dati):
    fornitore = cercaFornitori(id)
    if fornitore is None:
        return None
    fornitore.aggiornaProprietà(dati)
    return salvaFornitore(fornitore)


def rimuoviFornitore(fornitore):
    id_fornitore = fornitore if isinstance(fornitore, int) else fornitore.id
    scrivi([f for f in leggi() if f.id != id_fornitore])



