from app.Models.offerte import Offerte


class Promozione(Offerte):

    def __init__(self, descrizione, dataInizio, dataFine, id=None):
        super().__init__(dataInizio, dataFine, id=id)
        self.descrizione = descrizione
        self.tipo = "promozione"
