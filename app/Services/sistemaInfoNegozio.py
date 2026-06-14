from app.Repos import orarioRepository as repo


def richiediOrari():
    return repo.cercaOrari()
