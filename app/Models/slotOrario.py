

class slotOrario:

    def __init__(self, id, data, Orario):
        self.id = id
        self.data = data
        self.Orario = Orario

    def impostaData(self, data) -> None:
        self.data = data
    
    def getData(self):
        return self.data