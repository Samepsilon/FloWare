from app.Repos.catalogoArticoli import CatalogoArticoli

class SistemaCatalogo:
    @classmethod
    def visualizzaCatalogo(cls):
        return CatalogoArticoli.mostraCatalogo()

    @classmethod
    def richiediDettagli(cls, idArticolo):
        articolo = CatalogoArticoli.trovaPerId(idArticolo)
        if articolo is None:
            raise ValueError(f"Articolo con id={idArticolo} non trovato.")
        return articolo
