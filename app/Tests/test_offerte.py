import unittest
from app.Models.offerte import Offerte
from app.Models.sconto import Sconto
from app.Models.promozione import Promozione


class TestOfferte(unittest.TestCase):

    def setUp(self):
        self.offerta = Offerte(dataInizio="2026-06-01", dataFine="2026-06-30", id=1)

    def test_id(self):
        self.assertEqual(self.offerta.id, 1)

    def test_data_inizio(self):
        self.assertEqual(self.offerta.dataInizio, "2026-06-01")

    def test_data_fine(self):
        self.assertEqual(self.offerta.dataFine, "2026-06-30")

    def test_default_id_none(self):
        o = Offerte(dataInizio="2026-01-01", dataFine="2026-01-31")
        self.assertIsNone(o.id)


class TestSconto(unittest.TestCase):

    def setUp(self):
        self.sconto = Sconto(
            evento="Primavera",
            percentuale=20.0,
            dataInizio="2026-03-01",
            dataFine="2026-05-31",
            id=2,
        )

    def test_evento(self):
        self.assertEqual(self.sconto.evento, "Primavera")

    def test_percentuale(self):
        self.assertEqual(self.sconto.getPercentuale(), 20.0)

    def test_tipo(self):
        self.assertEqual(self.sconto.tipo, "sconto")

    def test_data_inizio(self):
        self.assertEqual(self.sconto.dataInizio, "2026-03-01")

    def test_data_fine(self):
        self.assertEqual(self.sconto.dataFine, "2026-05-31")

    def test_id(self):
        self.assertEqual(self.sconto.id, 2)

    def test_is_instance_offerte(self):
        self.assertIsInstance(self.sconto, Offerte)

    def test_default_id_none(self):
        s = Sconto(evento="Test", percentuale=10.0, dataInizio="2026-01-01", dataFine="2026-01-31")
        self.assertIsNone(s.id)

    def test_percentuale_zero(self):
        s = Sconto(evento="Zero", percentuale=0.0, dataInizio="2026-01-01", dataFine="2026-01-31")
        self.assertEqual(s.getPercentuale(), 0.0)

    def test_percentuale_alta(self):
        s = Sconto(evento="Super", percentuale=99.9, dataInizio="2026-01-01", dataFine="2026-12-31")
        self.assertEqual(s.getPercentuale(), 99.9)


class TestPromozione(unittest.TestCase):

    def setUp(self):
        self.promo = Promozione(
            descrizione="Saldi estivi",
            dataInizio="2026-07-01",
            dataFine="2026-07-31",
            id=3,
        )

    def test_descrizione(self):
        self.assertEqual(self.promo.descrizione, "Saldi estivi")

    def test_tipo(self):
        self.assertEqual(self.promo.tipo, "promozione")

    def test_data_inizio(self):
        self.assertEqual(self.promo.dataInizio, "2026-07-01")

    def test_data_fine(self):
        self.assertEqual(self.promo.dataFine, "2026-07-31")

    def test_id(self):
        self.assertEqual(self.promo.id, 3)

    def test_is_instance_offerte(self):
        self.assertIsInstance(self.promo, Offerte)

    def test_default_id_none(self):
        p = Promozione(descrizione="Test", dataInizio="2026-01-01", dataFine="2026-01-31")
        self.assertIsNone(p.id)

    def test_tipo_diverso_da_sconto(self):
        self.assertNotEqual(self.promo.tipo, "sconto")


if __name__ == "__main__":
    unittest.main()
