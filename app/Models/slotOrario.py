

class SlotOrario:

    def __init__(self, id, data, fasciaOraria):
        self.id = id
        self.data = data
        self.fasciaOraria = fasciaOraria

    def impostaData(self, data) -> None:
        self.data = data
    
    