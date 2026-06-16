from app.Models.fornitore import Fornitore
from app.Repos import catalogoFornitori as repo
from app.Repos import catalogoArticoli as repoA


def visualizzaFornitori():
    return repo.caricaListaFornitori()


def aggiungiFornitore(dati):
    if not validaDatiFornitore(dati):
        raise ValueError("Dati fornitore non validi.")
    esistenti = [f for f in repo.caricaListaFornitori() if f.nome.lower() == dati["nome"].lower()]
    if esistenti:
        raise ValueError(f"Esiste già un fornitore con nome '{dati['nome']}'.")
    return repo.salvaFornitore(dati)


def validaDatiFornitore(dati):
    nome = dati.get("nome", "")
    contatti = dati.get("contatti", "")
    tipologia = dati.get("tipologiaMerce", dati.get("tipologia", ""))
    return bool(nome.strip() and contatti.strip() and tipologia.strip())


def modificaFornitore(fornitore, nuoviDati):
    if isinstance(fornitore, int):
        fornitore = getFornitore(fornitore)
    fornitore.aggiornaProprietà(nuoviDati)
    return repo.salva_fornitore(fornitore)


def eliminaFornitore(fornitore):
    if isinstance(fornitore, int):
        fornitore = getFornitore(fornitore)
    for articolo in repoA.articoliDelFornitore(fornitore.id):
        articolo.fornitore_id = None
        repoA.salvaArticolo(articolo)
    repo.rimuoviFornitore(fornitore)


def aggiornaListaFornitori():
    return visualizzaListaFornitori()


def visualizzaListaFornitori():
    return repo.caricaListaFornitori()


def getFornitore(fornitore):
    if isinstance(fornitore, int):
        risultato = repo.cercaFornitori(fornitore)
    elif isinstance(fornitore, Fornitore):
        risultato = repo.cercaFornitore(fornitore.id)
    else:
        raise ValueError("Fornitore non valido.")
    if risultato is None:
        raise ValueError("Fornitore non trovato.")
    return risultato
