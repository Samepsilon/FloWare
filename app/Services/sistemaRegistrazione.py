from app.Models.utente import Utente
from app.Models.negoziante import Negoziante
from app.Models.cliente import Cliente
from app.Repos import utenteRepository as repo

#Regex per verificatoEmail e verificatoCriteriPassword
import re
mail_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password_pattern =  r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$"


def inviaRegistrazione(username, email, password, ruolo):
        if ruolo == "negoziante":
            u = Negoziante(username, email, password, ruolo)
        else :
            u = Cliente(username, email, password, ruolo)
        return repo.salva_utente(u)


def verificatoFormatoEmail(mail):
    return bool(re.match(mail_pattern, mail))

def verificatoCriteriPassword(password):
    """
    La password deve:
    Contenere almeno un numero
    Contenere almeno una lettera maiuscola
    Contenere almeno una lettera minuscola
    Contenere almeno un carattere speciale ($, @, #, %)
    Avere una lunghezza compresa tra 6 e 20 caratteri
    """
    return bool(re.search(password_pattern, password))



def confrontaPassword(password , conferma ):
    return password == conferma
