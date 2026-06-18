import unittest
from app.Services.sistemaAccesso import SistemaAccesso


class TestSistemaAccesso(unittest.TestCase):

    #  reindirizzaPerRuolo

    def test_reindirizza_cliente(self):
        risultato = SistemaAccesso.reindirizzaPerRuolo("cliente")
        self.assertEqual(risultato, "InterfacciaCliente")

    def test_reindirizza_negoziante(self):
        risultato = SistemaAccesso.reindirizzaPerRuolo("negoziante")
        self.assertEqual(risultato, "InterfacciaNegoziante")

    #verificaFormatoEmail

    def test_email_valida(self):
        self.assertTrue(SistemaAccesso.verificaFormatoEmail("utente@esempio.com"))

    def test_email_valida_con_punti(self):
        self.assertTrue(SistemaAccesso.verificaFormatoEmail("nome.cognome@email.it"))

    def test_email_valida_con_numeri(self):
        self.assertTrue(SistemaAccesso.verificaFormatoEmail("user123@mail.org"))

    def test_email_valida_con_underscore(self):
        self.assertTrue(SistemaAccesso.verificaFormatoEmail("nome_cognome@email.com"))

    def test_email_senza_chiocciola(self):
        self.assertFalse(SistemaAccesso.verificaFormatoEmail("utentesenzachiocciola.com"))

    def test_email_senza_dominio(self):
        self.assertFalse(SistemaAccesso.verificaFormatoEmail("utente@"))

    def test_email_senza_estensione(self):
        self.assertFalse(SistemaAccesso.verificaFormatoEmail("utente@dominio"))

    def test_email_vuota(self):
        self.assertFalse(SistemaAccesso.verificaFormatoEmail(""))

    def test_email_con_spazi(self):
        self.assertFalse(SistemaAccesso.verificaFormatoEmail("utente @email.com"))

    def test_email_estensione_corta(self):
        self.assertFalse(SistemaAccesso.verificaFormatoEmail("utente@dominio.x"))


    #Sessione

    def test_imposta_sessione(self):
        SistemaAccesso.impostaSessione("cliente")
        sessione = SistemaAccesso.getSessione()
        self.assertEqual(sessione["ruolo"], "cliente")

    def test_get_sessione_restituisce_copia(self):
        sessione1 = SistemaAccesso.getSessione()
        sessione1["ruolo"] = "modificato"
        sessione2 = SistemaAccesso.getSessione()
        self.assertNotEqual(sessione2["ruolo"], "modificato")


if __name__ == "__main__":
    unittest.main()
