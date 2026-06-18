import re
mail_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def confrontaPassword(password , conferma ):
    return password == conferma

def verificatoFormatoEmail(mail):
    return bool(re.match(mail_pattern, mail))