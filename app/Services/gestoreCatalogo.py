from app.Models.articolo import Articolo
from app.Repos import articoloRepository as repo
from app.Repos import fornitoreRepository as repoF


def aggiungi_articolo(nome, descrizione, prezzo, fornitore_id=None, disponibile=True):
    if fornitore_id is not None and repoF.trova_fornitore(fornitore_id) is None:
        raise ValueError(f"Fornitore con id={fornitore_id} non esiste.")
    a = Articolo(nome=nome, descrizione=descrizione, prezzo=prezzo,
                 disponibile=disponibile, fornitore_id=fornitore_id)
    return repo.salva_articolo(a)


def aggiorna_articolo(id, nome=None, descrizione=None, prezzo=None, disponibile=None, fornitore_id=None):
    a = repo.trova_articolo(id)
    if a is None:
        raise ValueError(f"Articolo con id={id} non trovato.")
    if nome is not None:
        a.nome = nome
    if descrizione is not None:
        a.descrizione = descrizione
    if prezzo is not None:
        a.prezzo = prezzo
    if disponibile is not None:
        a.disponibile = disponibile
    if fornitore_id is not None:
        if repoF.trova_fornitore(fornitore_id) is None:
            raise ValueError(f"Fornitore con id={fornitore_id} non esiste.")
        a.fornitore_id = fornitore_id
    return repo.salva_articolo(a)


def rimuovi_articolo(id):
    if repo.trova_articolo(id) is None:
        raise ValueError(f"Articolo con id={id} non trovato.")
    repo.elimina_articolo(id)


def applica_sconto(id, percentuale):
    a = repo.trova_articolo(id)
    if a is None:
        raise ValueError(f"Articolo con id={id} non trovato.")
    a.sconto = percentuale
    return repo.salva_articolo(a)


def rimuovi_sconto(id):
    return applica_sconto(id, 0.0)


def segna_disponibile(id, disponibile):
    a = repo.trova_articolo(id)
    if a is None:
        raise ValueError(f"Articolo con id={id} non trovato.")
    a.disponibile = disponibile
    return repo.salva_articolo(a)


def get_catalogo():
    return repo.tutti_gli_articoli()


def get_catalogo_disponibile():
    return [a for a in repo.tutti_gli_articoli() if a.disponibile]


def get_articoli_in_sconto():
    return [a for a in repo.tutti_gli_articoli() if a.sconto > 0]


def cerca_per_nome(nome):
    return [a for a in repo.tutti_gli_articoli() if nome.lower() in a.nome.lower()]


def cerca_per_fascia_prezzo(minimo, massimo):
    return [a for a in repo.tutti_gli_articoli() if minimo <= a.prezzo_finale() <= massimo]

