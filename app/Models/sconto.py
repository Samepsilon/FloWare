from offerte import Offerte
class Sconto (Offerte):

    def __init__(self,id,evento,percentuale,dataInizio,dataFine):
      super().__init__(dataInizio, dataFine, ruolo = "sconto", id=id)  
      self.evento = evento
      self.percentuale = percentuale

    def getPercentuale(self):
        return self.percentuale


