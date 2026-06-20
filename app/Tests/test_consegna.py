import unittest
from app.Models.consegna import Consegna


class TestConsegna(unittest.TestCase):

    def setUp(self):
        self.consegna = Consegna(
            regione="Lombardia",
            citta="Milano",
            via="Via Roma",
            civico="10",
            stato="in attesa",
            clienteId=5,
            id=1,
        )

    #  Costruttore

    def test_id(self):
        self.assertEqual(self.consegna.id, 1)

    def test_regione(self):
        self.assertEqual(self.consegna.regione, "Lombardia")

    def test_citta(self):
        self.assertEqual(self.consegna.citta, "Milano")

    def test_via(self):
        self.assertEqual(self.consegna.via, "Via Roma")

    def test_civico(self):
        self.assertEqual(self.consegna.civico, "10")

    def test_stato(self):
        self.assertEqual(self.consegna.getStato(), "in attesa")

    def test_cliente_id(self):
        self.assertEqual(self.consegna.getClienteId(), 5)

    #  setStato

    def test_set_stato(self):
        self.consegna.setStato("consegnata")
        self.assertEqual(self.consegna.getStato(), "consegnata")

    def test_set_stato_none(self):
        self.consegna.setStato(None)
        self.assertIsNone(self.consegna.getStato())

    def test_set_stato_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self.consegna.setStato(123)

    #  __repr__

    def test_repr_contiene_regione(self):
        rappresentazione = repr(self.consegna)
        self.assertIn("Lombardia", rappresentazione)

    def test_repr_contiene_citta(self):
        rappresentazione = repr(self.consegna)
        self.assertIn("Milano", rappresentazione)

    def test_repr_contiene_via(self):
        rappresentazione = repr(self.consegna)
        self.assertIn("Via Roma", rappresentazione)


if __name__ == "__main__":
    unittest.main()
