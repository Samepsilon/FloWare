import unittest
from app.Models.utente import Utente
from app.Models.cliente import Cliente
from app.Models.negoziante import Negoziante


class TestUtente(unittest.TestCase):

    def setUp(self):
        self.utente = Utente("marco01", "marco@email.com", "Pass123@", ruolo="cliente", id=1)

    def test_username(self):
        self.assertEqual(self.utente.getUsername(), "marco01")

    def test_email(self):
        self.assertEqual(self.utente.getEmail(), "marco@email.com")

    def test_password(self):
        self.assertEqual(self.utente.getPassword(), "Pass123@")

    def test_id(self):
        self.assertEqual(self.utente.id, 1)

    def test_id_default_none(self):
        utente = Utente("user", "user@test.com", "pwd")
        self.assertIsNone(utente.id)

    def test_ruolo_default_vuoto(self):
        utente = Utente("user", "user@test.com", "pwd")
        self.assertEqual(utente.getRuolo(), "")


class TestCliente(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente("luca02", "luca@email.com", "Secret1#", id=5)

    def test_ruolo_cliente(self):
        self.assertEqual(self.cliente.getRuolo(), "cliente")


    def test_is_instance_utente(self):
        self.assertIsInstance(self.cliente, Utente)



class TestNegoziante(unittest.TestCase):

    def setUp(self):
        self.negoziante = Negoziante("anna03", "anna@shop.com", "Shop99$", id=10)

    def test_ruolo_negoziante(self):
        self.assertEqual(self.negoziante.getRuolo(), "negoziante")

    def test_is_instance_utente(self):
        self.assertIsInstance(self.negoziante, Utente)

    def test_ruolo_diverso_da_cliente(self):
        self.assertNotEqual(self.negoziante.getRuolo(), "cliente")


if __name__ == "__main__":
    unittest.main()
