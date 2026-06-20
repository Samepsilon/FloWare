
class Articolo:

    def __init__(self, nome, descrizione, prezzo, quantita=0, disponibile=True,
                 fornitore_id=None, percentuale=0.0, id=None):
        self.id = id
        self.nome = nome
        self.descrizione = descrizione
        self.prezzo = prezzo
        self.quantita = quantita
        self.disponibile = disponibile
        self.fornitore_id = fornitore_id
        self.percentuale = percentuale

    def getDettagli(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descrizione": self.descrizione,
            "prezzo": self.prezzo,
            "quantita": self.quantita,
            "disponibile": self.disponibile,
            "prezzo_finale": self.prezzoFinale(),
        }

    def applicaSconto(self, sconto, percentuale=None, dataInizio=None, dataFine=None):
        if percentuale is not None:
            self.percentuale = percentuale
        elif hasattr(sconto, "getPercentuale"):
            self.percentuale = sconto.getPercentuale()
        elif hasattr(sconto, "percentuale"):
            self.percentuale = sconto.percentuale

    def rimuoviOfferta(self):
        self.percentuale = 0.0

    def setDati(self, nuoviDati):
        for chiave, valore in nuoviDati.items():
            if hasattr(self, chiave):
                setattr(self, chiave, valore)

    def prezzoFinale(self):
        return round(self.prezzo * (1 - (self.percentuale / 100)), 2)

    def __repr__(self):
        return str(self.getDettagli())

