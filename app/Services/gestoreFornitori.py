"""
Questo modulo si occupa della gestione dei fornitori associati al negozio,
consentendo la visualizzazione, l'inserimento, la modifica e la rimozione dei fornitori.
"""

from app.Models.fornitore import Fornitore
from app.Repos.catalogoFornitori import CatalogoFornitori
from app.Repos.catalogoArticoli import CatalogoArticoli

class GestoreFornitori:
    @classmethod
    def visualizzaFornitori(cls):
        return CatalogoFornitori.caricaListaFornitori()

    @classmethod
    def aggiungiFornitore(cls, dati):
        if not cls.validaDatiFornitore(dati):
            raise ValueError("Dati fornitore non validi.")
        esistenti = [f for f in CatalogoFornitori.caricaListaFornitori() if f.nome.lower() == dati["nome"].lower()]
        if esistenti:
            raise ValueError(f"Esiste già un fornitore con nome '{dati['nome']}'.")
        fornitore = Fornitore(
            nome=dati["nome"],
            contatti=dati["contatti"],
            tipologiaMerce=dati.get("tipologiaMerce", dati.get("tipologia", "")),
            servizioDomicilio=dati.get("servizioDomicilio", False),
        )
        return CatalogoFornitori.salvaFornitore(fornitore)

    @classmethod
    def validaDatiFornitore(cls, dati):
        nome = dati.get("nome", "")
        contatti = dati.get("contatti", "")
        tipologia = dati.get("tipologiaMerce", dati.get("tipologia", ""))
        return bool(nome.strip() and contatti.strip() and tipologia.strip())

    @classmethod
    def modificaFornitore(cls, fornitore, nuoviDati):
        if isinstance(fornitore, int):
            fornitore = cls.getFornitore(fornitore)
        fornitore.aggiornaProprieta(nuoviDati)
        return CatalogoFornitori.salvaFornitore(fornitore)

    @classmethod
    def eliminaFornitore(cls, fornitore):
        if isinstance(fornitore, int):
            fornitore = cls.getFornitore(fornitore)
        for articolo in CatalogoArticoli.articoliDelFornitore(fornitore.id):
            articolo.fornitore_id = None
            CatalogoArticoli.salvaArticolo(articolo)
        CatalogoFornitori.rimuoviFornitore(fornitore)

    @classmethod
    def aggiornaListaFornitori(cls):
        return cls.visualizzaListaFornitori()

    @classmethod
    def visualizzaListaFornitori(cls):
        return CatalogoFornitori.caricaListaFornitori()

    @classmethod
    def getFornitore(cls, fornitore):
        if isinstance(fornitore, int):
            risultato = CatalogoFornitori.cercaFornitori(fornitore)
        elif isinstance(fornitore, Fornitore):
            risultato = CatalogoFornitori.cercaFornitori(fornitore.id)
        else:
            raise ValueError("Fornitore non valido.")
        if risultato is None:
            raise ValueError("Fornitore non trovato.")
        return risultato
