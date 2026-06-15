
class Offerte:

    def __init__(self, dataInizio, dataFine,ruolo="", id = None):
        self.id = id
        self.dataInizio = dataInizio
        self.dataFine = dataFine
        self.ruolo = ruolo