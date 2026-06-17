from app.Models.articolo import Articolo
from app.Repos.catalogoArticoli import CatalogoArticoli
from app.Repos.catalogoFornitori import CatalogoFornitori

class GestoreCatalogo:
    @classmethod
    def aggiungiArticolo(cls, dati):
        if isinstance(dati, Articolo):
            articolo = dati
        else:
            fornitore_id = dati.get("fornitore_id")
            if fornitore_id is not None and CatalogoFornitori.trovaPerId(fornitore_id) is None:
                raise ValueError(f"Fornitore con id={fornitore_id} non esiste.")
            articolo = Articolo(
                nome=dati["nome"],
                descrizione=dati.get("descrizione", ""),
                prezzo=float(dati["prezzo"]),
                quantita=int(dati.get("quantita", 0)),
                disponibile=dati.get("disponibile", True),
                fornitore_id=fornitore_id,
            )
        if not cls.validaArticolo(articolo):
            raise ValueError("Dati articolo non validi.")
        return cls.aggiungiACatalogo(articolo)

    @classmethod
    def validaArticolo(cls, articolo):
        return CatalogoArticoli.verificaArticolo(articolo)

    @classmethod
    def aggiungiACatalogo(cls, articolo):
        return CatalogoArticoli.salva(articolo)

    @classmethod
    def modificaArticolo(cls, id, nuoviDati):
        articolo = CatalogoArticoli.trovaPerId(id)
        if articolo is None:
            raise ValueError(f"Articolo con id={id} non trovato.")
        articolo.setDati(nuoviDati)
        return CatalogoArticoli.salva(articolo)

    @classmethod
    def getArticolo(cls, id):
        articolo = CatalogoArticoli.trovaPerId(id)
        if articolo is None:
            raise ValueError(f"Articolo con id={id} non trovato.")
        return articolo

    @classmethod
    def rimuoviArticolo(cls, id):
        if not CatalogoArticoli.verificaArticolo(id):
            raise ValueError(f"Articolo con id={id} non trovato.")
        CatalogoArticoli.rimuoviArticolo(id)

    @classmethod
    def annullaCreazione(cls):
        return None

    @classmethod
    def visualizzaCatalogo(cls):
        return CatalogoArticoli.mostraCatalogo()
