from offerte import Offerte
class Promozione (Offerte):

    def __init__(self,id,descrizione,dataInizio,dataFine):
      super().__init__(dataInizio, dataFine, ruolo = "promozione", id=id)  
      self.descrizione = descrizione