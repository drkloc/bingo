import os, json, random, click, math
import svgutils.transform as sg
from lxml import etree

class Composer:
    DPI = 40
    VSPACING = 20
    def __init__(self, cards, cards_per_page):
        self.dir = cards
        self.cards = [
            os.path.join(cards, f)
            for f in os.listdir(cards)
            if f.endswith('.svg')
        ]
        self.n = cards_per_page

    def get_new_page(self):
        page = sg.SVGFigure(
            "%s" % (21 * Composer.DPI),
            "%s" % (29.7 * Composer.DPI)
        )
        return page

    def get_x_transform(self, page, svg):
        page_width = page.root.get('width').replace('px', '')
        page_width = float(page_width)
        svg_width = svg.root.get('width').replace('px', '')
        svg_width = float(svg_width)
        transform = (page_width - svg_width) / 2
        return transform

    def get_y_transform(self, page, svg, i):
        page_height = page.root.get('height').replace('px', '')
        page_height = float(page_height)
        svg_height = svg.root.get('height').replace('px', '')
        svg_height = float(svg_height)
        block_height = svg_height * self.n + Composer.VSPACING * (self.n - 1)
        tranform = svg_height * i + Composer.VSPACING * (i + 1)
        tranform = (page_height - block_height) / 2 + tranform
        return tranform

    def write(self):
        # Process cards into a list of svg pages
        label = click.style('Processing Cards', fg='yellow')
        with click.progressbar(self.cards, label=label, show_eta=True) as cards:
            _pages = []
            _page = self.get_new_page()
            for card in cards:
                i = self.cards.index(card)
                svg_card = sg.fromfile(card)
                h = i % self.n
                x = '%spx' % self.get_x_transform(_page, svg_card)
                y = '%spx' % self.get_y_transform(_page, svg_card, h)
                svg_card.root.set("x", x)
                svg_card.root.set("y", y)
                _page.append(svg_card)
                if not h and i:
                    _pages.append(_page)
                    _page = self.get_new_page()
                if card == self.cards[-1]:
                    _pages.append(_page)
        # Create directory if does not exist.
        output = self.dir + ".paginated"
        if not os.path.isdir(output):
            os.mkdir(output)
        # Write svg_pages to files.
        label = click.style('Writing pages', fg='yellow')
        with click.progressbar(_pages, label=label, show_eta=True) as pages:
            i = 1
            for page in pages:
                f = os.path.join(output, '%05d.svg' % i)
                page.save(f)
                i = i + 1
