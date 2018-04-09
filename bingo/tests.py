import unittest

from bingo.shuffler import Cards

class TestCards(unittest.TestCase):
    def setUp(self):
        self.cards = Cards().shuffle(13000)

    def test_no_repeated_numbers_in_card(self):
        for card in self.cards:
            numbers = []
            for k in card['card'].keys():
                for n in card['card'][k]:
                    numbers.append(n)
            self.assertEqual(len(numbers), len(set(numbers)))

    def test_unique_rows_in_set(self):
        rows = []
        for card in self.cards:
            for k in card['card'].keys():
                rows.append(sorted(card['card'][k]))
        unique_rows = []
        for row in rows:
            if not row in unique_rows:
                unique_rows.append(row)
        self.assertEqual(len(rows), len(unique_rows))

    def test_unique_cards_in_set(self):
        cards = []
        for card in self.cards:
            _card = []
            for k in card['card'].keys():
                _card = _card + card['card'][k]
            _card = sorted(_card)
        unique_cards = []
        for card in cards:
            if card not in unique_cards:
                unique_cards.append(card)
        self.assertEqual(len(cards), len(unique_cards))

if __name__ == '__main__':
    unittest.main()