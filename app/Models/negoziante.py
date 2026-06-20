from app.Models.utente import Utente


class Negoziante(Utente):

    def __init__(self, username, email, password, id=None):
        super().__init__(username, email, password, ruolo="negoziante", id=id)
