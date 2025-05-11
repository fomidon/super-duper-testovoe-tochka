import unittest
from run import check_capacity


class TestCheckCapacity(unittest.TestCase):
    def test_no_guests(self):
        # Нет гостей -> всегда поместятся
        self.assertTrue(check_capacity(5, []))

    def test_zero_capacity_no_guests(self):
        # Вместимость 0 + нет гостей -> помещаются
        self.assertTrue(check_capacity(0, []))

    def test_zero_capacity_with_guest(self):
        # Вместимость 0 + есть гость -> не помещаются
        guests = [{"name": "A", "check-in": "2021-01-01", "check-out": "2021-01-02"}]
        self.assertFalse(check_capacity(0, guests))

    def test_single_guest(self):
        # Просто один гость + вместимость >= 1
        guests = [{"name": "A", "check-in": "2021-01-01", "check-out": "2021-01-02"}]
        self.assertTrue(check_capacity(1, guests))

    def test_non_overlapping_guests(self):
        # Гости с непересекающимися периодами
        guests = [
            {"name": "A", "check-in": "2021-01-01", "check-out": "2021-01-03"},
            {"name": "B", "check-in": "2021-01-03", "check-out": "2021-01-05"},
        ]
        self.assertTrue(check_capacity(1, guests))

    def test_exact_capacity(self):
        # Двое перекрываются + третий заезжает в день выезда первого + вместимость = 2
        guests = [
            {"name": "A", "check-in": "2021-01-10", "check-out": "2021-01-15"},
            {"name": "B", "check-in": "2021-01-12", "check-out": "2021-01-20"},
            {"name": "C", "check-in": "2021-01-15", "check-out": "2021-01-21"},
        ]
        self.assertTrue(check_capacity(2, guests))

    def test_exceed_capacity(self):
        # Три гостя пересекаются в один день + вместимость = 2 -> не помещаются
        guests = [
            {"name": "A", "check-in": "2021-01-10", "check-out": "2021-01-16"},
            {"name": "B", "check-in": "2021-01-12", "check-out": "2021-01-20"},
            {"name": "C", "check-in": "2021-01-15", "check-out": "2021-01-21"},
        ]
        self.assertFalse(check_capacity(2, guests))

    def test_back_to_back_stays(self):
        # Один гость выезжает + другой заезжает в тот же день -> занимают один слот
        guests = [
            {"name": "A", "check-in": "2021-05-01", "check-out": "2021-05-05"},
            {"name": "B", "check-in": "2021-05-05", "check-out": "2021-05-10"},
        ]
        self.assertTrue(check_capacity(1, guests))

    def test_multiple_same_day_events(self):
        # Несколько выселений и заселений в один день
        guests = [
            {"name": "A", "check-in": "2021-06-01", "check-out": "2021-06-05"},
            {"name": "B", "check-in": "2021-06-05", "check-out": "2021-06-10"},
            {"name": "C", "check-in": "2021-06-05", "check-out": "2021-06-08"},
        ]
        # В дату 2021-06-05: A выезжает, B и C заезжают -> требуется вместимость 2
        self.assertTrue(check_capacity(2, guests))
        self.assertFalse(check_capacity(1, guests))

    def test_invalid_dates(self):
        # Некорректные даты: выезд раньше заезда -> не помещаются
        guests = [{"name": "A", "check-in": "2021-01-05", "check-out": "2021-01-03"}]
        self.assertFalse(check_capacity(1, guests))


if __name__ == "__main__":
    unittest.main()
