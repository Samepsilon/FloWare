from offerta import offerta
class sconto (offerta):

    def __init__(self,id,evento,percentuale,dataInizio,dataFine):
      super().__init__(dataInizio, dataFine, id=id)  
      self.evento = evento
      self.percentuale = percentuale

    def getPercentuale(self):
        return self.percentuale


