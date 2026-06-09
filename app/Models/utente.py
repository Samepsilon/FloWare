
class Utente:

    def __init__(self, username, email, password, ruolo="", id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.ruolo = ruolo  # "cliente" or "negoziante"

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email





