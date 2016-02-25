#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, click

class Cards(object):
    def __init__(self, context = None):
        self.context = context

    def shuffle(self, cards=6, minNum=1, maxNum=90, rows=3, numbersPerRow=5):
        _cards = []
        _shuffled_rows = []
        _shuffled_cards = []
        label = click.style('Generating Data', fg='yellow')
        with click.progressbar(length=int(cards), label=label, show_eta=True) as bar:
            while (len(_cards) < cards):
                _shuffled = []
                _rows = {}
                _card = []

                while(len(_rows) < rows):
                    _row = []
                    while (len(_row) < numbersPerRow):
                        number = random.randint(minNum, maxNum)
                        if not number in _shuffled:
                            _row.append(number)
                            _shuffled.append(number)
                    if not sorted(_row) in _shuffled_rows:
                        _rows[len(_rows) + 1] = _row
                        _shuffled_rows.append(sorted(_row))
                        _card = _card + _row
                if not sorted(_card) in _shuffled_cards:
                    _cards.append({'number':len(_cards) + 1, 'card':_rows})
                    _shuffled_cards.append(sorted(_card))
                    bar.update(1)
        return _cards
