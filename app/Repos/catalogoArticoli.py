import csv
import os
from app.Models.articolo import Articolo
from app.Models.promozione import Promozione
BASE_DIR = os.path.abspath("..")
FILE = BASE_DIR + "/Data/articoli.csv"

COLONNE = ["id", "nome", "descrizione", "prezzo", "quantita", "disponibile", "fornitore_id", "percentuale"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            percentuale = r.get("percentuale") or r.get("sconto") or "0"
            righe.append(Articolo(
                id=int(r["id"]),
                nome=r["nome"],
                descrizione=r["descrizione"],
                prezzo=float(r["prezzo"]),
                quantita=int(r["quantita"]) if r.get("quantita") else 0,
                disponibile=r["disponibile"] == "True",
                fornitore_id=int(r["fornitore_id"]) if r.get("fornitore_id") else None,
                percentuale=float(percentuale),
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
                "quantita": a.quantita,
                "disponibile": a.disponibile,
                "fornitore_id": a.fornitore_id if a.fornitore_id is not None else "",
                "percentuale": a.percentuale,
            })


def salva(articolo):
    tutti = leggi()
    if articolo.id is None:
        articolo.id = max((a.id for a in tutti), default=0) + 1
        tutti.append(articolo)
    else:
        tutti = [articolo if a.id == articolo.id else a for a in tutti]
    scrivi(tutti)
    return articolo


def getArticoliDisponibili():
    return [a for a in leggi() if a.disponibile]


def mostraCatalogo():
    return leggi()


def trovaPerId(id):
    for a in leggi():
        if a.id == id:
            return a
    return None


def rimuoviArticolo(id=None):
    if id is None:
        raise ValueError("Specificare l'id dell'articolo da rimuovere.")
    scrivi([a for a in leggi() if a.id != id])


def verificaArticolo(articolo=None):
    if articolo is None:
        return False
    if isinstance(articolo, int):
        return trovaPerId(articolo) is not None
    return bool(articolo.nome and str(articolo.nome).strip() and articolo.prezzo >= 0)


def associaScontoAdArticolo(articolo, sconto, percentuale=None, dataInizio=None, dataFine=None):
    if isinstance(articolo, int):
        articolo = trovaPerId(articolo)
    if articolo is None:
        return None
    articolo.applicaSconto(sconto, percentuale=percentuale, dataInizio=dataInizio, dataFine=dataFine)
    return salva(articolo)


def rimuoviRiferimentoOfferta(articolo, offerta=None):
    if articolo is None:
        return None
    articolo.rimuoviOfferta()
    return salva(articolo)


def verificaProdotti(listaProdottiSelezionati):
    catalogo = {a.id: a for a in leggi()}
    validi = []
    for articolo in listaProdottiSelezionati:
        id_articolo = articolo.id if isinstance(articolo, Articolo) else articolo
        if id_articolo in catalogo and catalogo[id_articolo].disponibile:
            validi.append(catalogo[id_articolo])
    return validi



