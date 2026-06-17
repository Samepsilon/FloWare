from app.Repos.orarioRepository import OrarioRepository

class SistemaInfoNegozio:
    @classmethod
    def richiediOrari(cls):
        return OrarioRepository.cercaOrari()
