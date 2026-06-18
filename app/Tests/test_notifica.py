import unittest
from app.Models.notifica import Notifica


class TestNotifica(unittest.TestCase):

    def setUp(self):
        self.notifica = Notifica(
            destinatario="negoziante",
            messaggio="Nuova richiesta preventivo",
            letta=False,
            tipo="preventivo",
            richiestaId=10,
            id=1,
        )

    #  Costruttore

    def test_id(self):
        self.assertEqual(self.notifica.id, 1)

    def test_destinatario(self):
        self.assertEqual(self.notifica.destinatario, "negoziante")

    def test_messaggio(self):
        self.assertEqual(self.notifica.messaggio, "Nuova richiesta preventivo")

    def test_letta(self):
        self.assertFalse(self.notifica.letta)

    def test_tipo(self):
        self.assertEqual(self.notifica.tipo, "preventivo")

    def test_richiesta_id(self):
        self.assertEqual(self.notifica.richiestaId, 10)

    #  Valori di default

    def test_default_richiesta_id_none(self):
        n = Notifica(destinatario="cliente", messaggio="Test", letta=False, tipo="generica")
        self.assertIsNone(n.richiestaId)

    def test_default_id_none(self):
        n = Notifica(destinatario="cliente", messaggio="Test", letta=False, tipo="generica")
        self.assertIsNone(n.id)

    #  Letta True

    def test_letta_true(self):
        n = Notifica(destinatario="cliente", messaggio="Letta", letta=True, tipo="info")
        self.assertTrue(n.letta)


if __name__ == "__main__":
    unittest.main()
