from app.Models.fornitore import Fornitore
from app.Repos import fornitoreRepository as repo
from app.Repos import articoloRepository as repoA




def visualizzaFornitori():
    return repo.caricaListaForniori()

def getFornitore(id):
    f = repo.trova_fornitore(id)
    if f is None:
        raise ValueError(f"Fornitore con id={id} non trovato.")
    return f

def validaDatiFornitore(nome, contatti, tipologia):
    if not nome or not nome.strip():
        raise ValueError("Il nome del fornitore non può essere vuoto.")
    if not contatti or not contatti.strip():
        raise ValueError("I contatti non possono essere vuoti.")
    if not tipologia or not tipologia.strip():
        raise ValueError("La tipologia merce non può essere vuota.")


def aggiungiFornitore(nome, contatti, tipologia, servizioDomicilio=False):
    esistenti = [f for f in repo.caricaListaForniori() if f.nome.lower() == nome.lower()]
    if esistenti:
        raise ValueError(f"Esiste già un fornitore con nome '{nome}'.")
    f = Fornitore(nome=nome, contatti=contatti, tipologia=tipologia, servizioDomicilio=servizioDomicilio)
    return repo.salva_fornitore(f)

def modificaFornitore(id, nome=None, contatti=None, tipologia=None, domicilio=None):
    f = getFornitore(id)
    if nome is not None:
        f.nome = nome
    if contatti is not None:
        f.contatti = contatti
    if tipologia is not None:
        f.tipologia = tipologia
    if domicilio is not None:
        f.domicilio = domicilio
    return repo.salva_fornitore(f)

def eliminaFornitore(id):
    getFornitore(id)
    for a in repoA.articoli_del_fornitore(id):
        a.fornitore_id = None
        repoA.salva_articolo(a)
    repo.rimuoviFornitore(id)



