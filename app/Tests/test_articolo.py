import unittest
from app.Models.articolo import Articolo
from app.Models.sconto import Sconto


class TestArticolo(unittest.TestCase):

    def setUp(self):
        self.articolo = Articolo(
            nome="Rosa Rossa",
            descrizione="Rosa rossa a gambo lungo",
            prezzo=5.50,
            quantita=100,
            disponibile=True,
            fornitore_id=3,
            percentuale=10.0,
            id=1,
        )

    def test_nome(self):
        self.assertEqual(self.articolo.nome, "Rosa Rossa")

    def test_descrizione(self):
        self.assertEqual(self.articolo.descrizione, "Rosa rossa a gambo lungo")

    def test_prezzo(self):
        self.assertEqual(self.articolo.prezzo, 5.50)

    def test_quantita(self):
        self.assertEqual(self.articolo.quantita, 100)

    def test_disponibile(self):
        self.assertTrue(self.articolo.disponibile)

    def test_fornitore_id(self):
        self.assertEqual(self.articolo.fornitore_id, 3)

    def test_percentuale(self):
        self.assertEqual(self.articolo.percentuale, 10.0)

    def test_id(self):
        self.assertEqual(self.articolo.id, 1)

    def test_prezzo_finale_con_sconto(self):
        # prezzo=5.50, percentuale=10 -> 5.50 * 0.90 = 4.95
        self.assertEqual(self.articolo.prezzoFinale(), 4.95)

    def test_prezzo_finale_senza_sconto(self):
        a = Articolo(nome="Giglio", descrizione="", prezzo=10.0)
        self.assertEqual(a.prezzoFinale(), 10.0)


    # applicaSconto

    def test_applica_sconto_con_percentuale_diretta(self):
        a = Articolo(nome="Giglio", descrizione="", prezzo=10.0)
        a.applicaSconto(None, percentuale=20.0)
        self.assertEqual(a.percentuale, 20.0)
        self.assertEqual(a.prezzoFinale(), 8.0)

    def test_applica_sconto_con_oggetto_sconto(self):
        a = Articolo(nome="Giglio", descrizione="", prezzo=10.0)
        sconto = Sconto(evento="Estate", percentuale=15.0, dataInizio="2026-06-01", dataFine="2026-08-31")
        a.applicaSconto(sconto)
        self.assertEqual(a.percentuale, 15.0)

    #  rimuoviOfferta

    def test_rimuovi_offerta(self):
        self.articolo.rimuoviOfferta()
        self.assertEqual(self.articolo.percentuale, 0.0)
        self.assertEqual(self.articolo.prezzoFinale(), 5.50)

    #  setDati

    def test_set_dati_modifica_nome(self):
        self.articolo.setDati({"nome": "Rosa Bianca"})
        self.assertEqual(self.articolo.nome, "Rosa Bianca")

    def test_set_dati_modifica_prezzo(self):
        self.articolo.setDati({"prezzo": 7.00})
        self.assertEqual(self.articolo.prezzo, 7.00)

    def test_set_dati_multipli(self):
        self.articolo.setDati({"nome": "Orchidea", "prezzo": 12.0, "quantita": 50})
        self.assertEqual(self.articolo.nome, "Orchidea")
        self.assertEqual(self.articolo.prezzo, 12.0)
        self.assertEqual(self.articolo.quantita, 50)

    #  getDettagli

    def test_get_dettagli_chiavi(self):
        dettagli = self.articolo.getDettagli()
        chiavi_attese = {"id", "nome", "descrizione", "prezzo", "quantita", "disponibile", "prezzo_finale"}
        self.assertEqual(set(dettagli.keys()), chiavi_attese)

    def test_get_dettagli_valori(self):
        dettagli = self.articolo.getDettagli()
        self.assertEqual(dettagli["nome"], "Rosa Rossa")
        self.assertEqual(dettagli["prezzo"], 5.50)
        self.assertEqual(dettagli["prezzo_finale"], 4.95)


if __name__ == "__main__":
    unittest.main()
