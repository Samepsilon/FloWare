from app.Repos import catalogoArticoli as repo


def visualizzaCatalogo():
    return repo.mostraCatalogo()


def richiediDettagli(idArticolo):
    articolo = repo.trovaPerId(idArticolo)
    if articolo is None:
        raise ValueError(f"Articolo con id={idArticolo} non trovato.")
    return articolo
