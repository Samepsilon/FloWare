import unittest
from app.Services.sistemaRegistrazione import SistemaRegistrazione


class TestSistemaRegistrazione(unittest.TestCase):


    def test_email_valida(self):
        self.assertTrue(SistemaRegistrazione.verificaFormatoEmail("test@email.com"))

    def test_email_valida_complessa(self):
        self.assertTrue(SistemaRegistrazione.verificaFormatoEmail("nome.cognome+tag@dominio.co.uk"))

    def test_email_invalida_senza_chiocciola(self):
        self.assertFalse(SistemaRegistrazione.verificaFormatoEmail("testEmail.com"))

    def test_email_invalida_senza_dominio(self):
        self.assertFalse(SistemaRegistrazione.verificaFormatoEmail("test@.com"))

    def test_email_vuota(self):
        self.assertFalse(SistemaRegistrazione.verificaFormatoEmail(""))

    # min 6 car, max 20, almeno 1 minuscola, 1 maiuscola, 1 digit, 1 simbolo tra @$#%

    def test_password_valida(self):
        self.assertTrue(SistemaRegistrazione.verificaCriteriPassword("Abcde1@"))

    def test_password_valida_lunga(self):
        self.assertTrue(SistemaRegistrazione.verificaCriteriPassword("Abcdefgh1234@aaa"))

    def test_password_senza_maiuscola(self):
        self.assertFalse(SistemaRegistrazione.verificaCriteriPassword("abcde1@"))

    def test_password_senza_minuscola(self):
        self.assertFalse(SistemaRegistrazione.verificaCriteriPassword("ABCDE1@"))

    def test_password_senza_digit(self):
        self.assertFalse(SistemaRegistrazione.verificaCriteriPassword("Abcdef@"))

    def test_password_senza_simbolo(self):
        self.assertFalse(SistemaRegistrazione.verificaCriteriPassword("Abcdef1"))

    def test_password_troppo_corta(self):
        self.assertFalse(SistemaRegistrazione.verificaCriteriPassword("Ab1@"))

    def test_password_troppo_lunga(self):
        self.assertFalse(SistemaRegistrazione.verificaCriteriPassword("A" * 15 + "bcdef1@"))

    def test_password_con_dollaro(self):
        self.assertTrue(SistemaRegistrazione.verificaCriteriPassword("Test1$x"))

    def test_password_con_cancelletto(self):
        self.assertTrue(SistemaRegistrazione.verificaCriteriPassword("Test1#x"))

    def test_password_con_percentuale(self):
        self.assertTrue(SistemaRegistrazione.verificaCriteriPassword("Test1%x"))

    # PAssword

    def test_confronta_password_uguali(self):
        self.assertTrue(SistemaRegistrazione.confrontaPassword("Pass1@", "Pass1@"))

    def test_confronta_password_diverse(self):
        self.assertFalse(SistemaRegistrazione.confrontaPassword("Pass1@", "Pass2@"))

    def test_confronta_password_case_sensitive(self):
        self.assertFalse(SistemaRegistrazione.confrontaPassword("Pass1@", "pass1@"))

    def test_confronta_password_vuote(self):
        self.assertTrue(SistemaRegistrazione.confrontaPassword("", ""))


if __name__ == "__main__":
    unittest.main()
