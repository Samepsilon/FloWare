from app.Models.offerte import Offerte


class Sconto(Offerte):

    def __init__(self, evento, percentuale, dataInizio, dataFine, id=None):
        super().__init__(dataInizio, dataFine, id=id)
        self.evento = evento
        self.percentuale = percentuale
        self.tipo = "sconto"

    def getPercentuale(self):
        return self.percentuale
