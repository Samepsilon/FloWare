class sconto:

    def __init__(self,id,evento,percentuale,dataInizio,dataFine):
        self.id = id
        self.evento = evento
        self.percentuale = percentuale
        self.dataInizio = dataInizio
        self.dataFine = dataFine


    def getPercentuale(self):
        return self.percentuale


