import csv
import os
from app.Models.articolo import Articolo
from app.Models.promozione import Promozione

class CatalogoArticoli:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "articoli.csv")
    COLONNE = ["id", "nome", "descrizione", "prezzo", "quantita", "disponibile", "fornitore_id", "percentuale"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
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

    @classmethod
    def scrivi(cls, articoli):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
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

    @classmethod
    def salva(cls, articolo):
        tutti = cls.leggi()
        if articolo.id is None:
            articolo.id = max((a.id for a in tutti), default=0) + 1
            tutti.append(articolo)
        else:
            tutti = [articolo if a.id == articolo.id else a for a in tutti]
        cls.scrivi(tutti)
        return articolo

    @classmethod
    def salvaArticolo(cls, articolo):
        return cls.salva(articolo)

    @classmethod
    def getArticoliDisponibili(cls):
        return [a for a in cls.leggi() if a.disponibile]

    @classmethod
    def mostraCatalogo(cls):
        return cls.leggi()
    @classmethod
    def getPrezzoFinale(cls, articoli):
        return articoli.prezzoFinale()

    @classmethod
    def trovaPerId(cls, id):
        for a in cls.leggi():
            if a.id == id:
                return a
        return None

    @classmethod
    def rimuoviArticolo(cls, id=None):
        if id is None:
            raise ValueError("Specificare l'id dell'articolo da rimuovere.")
        cls.scrivi([a for a in cls.leggi() if a.id != id])

    @classmethod
    def verificaArticolo(cls, articolo=None):
        if articolo is None:
            return False
        if isinstance(articolo, int):
            return cls.trovaPerId(articolo) is not None
        return bool(articolo.nome and str(articolo.nome).strip() and articolo.prezzo >= 0)

    @classmethod
    def associaScontoAdArticolo(cls, articolo, sconto, percentuale=None, dataInizio=None, dataFine=None):
        if isinstance(articolo, int):
            articolo = cls.trovaPerId(articolo)
        if articolo is None:
            return None
        articolo.applicaSconto(sconto, percentuale=percentuale, dataInizio=dataInizio, dataFine=dataFine)
        return cls.salva(articolo)

    @classmethod
    def rimuoviRiferimentoOfferta(cls, articolo, offerta=None):
        if articolo is None:
            return None
        articolo.rimuoviOfferta()
        return cls.salva(articolo)

    @classmethod
    def verificaProdotti(cls, listaProdottiSelezionati):
        catalogo = {a.id: a for a in cls.leggi()}
        validi = []
        for articolo in listaProdottiSelezionati:
            id_articolo = articolo.id if isinstance(articolo, Articolo) else articolo
            if id_articolo in catalogo and catalogo[id_articolo].disponibile:
                validi.append(catalogo[id_articolo])
        return validi

    @classmethod
    def articoliDelFornitore(cls, fornitore_id):
        return [a for a in cls.leggi() if a.fornitore_id == fornitore_id]
