"""
Questo modulo fornisce ai clienti le informazioni relative al negozio,
quali ad esempio gli orari di apertura e chiusura.
"""

from app.Repos.orarioRepository import OrarioRepository

class SistemaInfoNegozio:
    @classmethod
    def richiediOrari(cls):
        return OrarioRepository.cercaOrari()
