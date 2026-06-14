
class SlotOrario:

    def __init__(self, data, fasciaOraria, id=None, disponibile=True):
        self.id = id
        self.data = data
        self.fasciaOraria = fasciaOraria
        self.disponibile = disponibile

    def impostaData(self, data):
        self.data = data
