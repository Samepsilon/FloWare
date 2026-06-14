from app.Models.articolo import Articolo
from app.Repos import catalogoArticoli as repo
from app.Repos import catalogoFornitori as repoF


def aggiungiArticolo(dati):
    if isinstance(dati, Articolo):
        articolo = dati
    else:
        fornitore_id = dati.get("fornitore_id")
        if fornitore_id is not None and repoF.trovaPerId(fornitore_id) is None:
            raise ValueError(f"Fornitore con id={fornitore_id} non esiste.")
        articolo = Articolo(
            nome=dati["nome"],
            descrizione=dati.get("descrizione", ""),
            prezzo=float(dati["prezzo"]),
            quantita=int(dati.get("quantita", 0)),
            disponibile=dati.get("disponibile", True),
            fornitore_id=fornitore_id,
        )
    if not validaArticolo(articolo):
        raise ValueError("Dati articolo non validi.")
    return aggiungiACatalogo(articolo)


def validaArticolo(articolo):
    return repo.verificaArticolo(articolo)


def aggiungiACatalogo(articolo):
    return repo.salvaArticolo(articolo)


def modificaArticolo(id, nuoviDati):
    articolo = repo.trovaPerId(id)
    if articolo is None:
        raise ValueError(f"Articolo con id={id} non trovato.")
    articolo.setDati(nuoviDati)
    return repo.salvaArticolo(articolo)


def getArticolo(id):
    articolo = repo.trovaPerId(id)
    if articolo is None:
        raise ValueError(f"Articolo con id={id} non trovato.")
    return articolo


def rimuoviArticolo(id):
    if not repo.verificaArticolo(id):
        raise ValueError(f"Articolo con id={id} non trovato.")
    repo.rimuoviArticolo(id)


def aggiornaCatalogo():
    return repo.aggiornaCatalogo()


def annullaCreazione():
    return None


def visualizzaCatalogo():
    return repo.mostraCatalogo()
