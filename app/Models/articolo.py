from app.Models.sconto import Sconto

class Articolo:

    def __init__(self, nome, descrizione, prezzo, disponibile=True, fornitore_id=None, percentuale=0.0, id=None):
        self.id = id
        self.nome = nome
        self.descrizione = descrizione
        self.prezzo = prezzo
        self.disponibile = disponibile
        self.fornitore_id = fornitore_id
        self.percentuale = percentuale  # percentage, e.g. 15.0 means 15%

    def __repr__(self):
        stato = "disponibile" if self.disponibile else "non disponibile"
        sconto_str = f", sconto {self.sconto}%" if self.sconto else ""
        return f"[{self.id}] {self.nome} — €{self.prezzo}{sconto_str} (finale: €{self.prezzo_finale()}) [{stato}]"


    def applicataSconto(self,sconto):
        percentuale = sconto.getPercentuale()
        self.percentuale = percentuale

    def rimuovieOfferta(self):
        self.percentuale = 0.0

    def getPrezzo(self):
        return round(self.prezzo * (1 - (self.percentuale / 100)), 2)


