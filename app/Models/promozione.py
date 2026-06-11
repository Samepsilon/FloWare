from offerta import offerta
class promozione (offerta):

    def __init__(self,id,descrizione,dataInizio,dataFine):
      super().__init__(dataInizio, dataFine, id=id)  
      self.descrizione = descrizione