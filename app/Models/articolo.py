from app.Models.sconto import sconto

class Articolo:

    def __init__(self,id,nome,prezzo,disponibile, descrizione):
        self.id = id
        self.nome = nome
        self.prezzo = prezzo
        self.prezzoNoOfferta = prezzo
        self.disponibile = disponibile
        self.descrizione = descrizione


    def getDettagli(self):
        return {self.descrizione,self.descrizione,self.prezzo}

    def applicataSconto(self,sconto):
        percentuale = sconto.getPercentuale()
        self.prezzo = self.prezzo * (1 - percentuale/100)

    def rimuovieOfferta(self):
        self.prezzo = self.prezzoNoOfferta

