from utente import Utente

class Cliente(Utente):

    def __init__(self, username, email, password, id=None):
        super().__init__(username, email, password, ruolo="cliente", id=id)


