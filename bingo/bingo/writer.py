import os, json, random, click
import svgutils.transform as sg
from lxml import etree

class Writer:
    FONT_SIZE = 25
    H_FACTOR = 1.15
    V_FACTOR = 0.75
    def __init__(self, f, layout):
        self.dir = f.replace('.json', '')
        if not os.path.isdir(self.dir):
            print click.style('\nCreating dir %s' % self.dir, fg='blue') + '\n'
            os.mkdir(self.dir)
        with open(f) as data:
            self.data = json.load(data)
        self.layout_options = layout

    def getFillables(self):
        # Get squares that have the empty class.
        empties = etree.XPath("//*[@class='empty']")
        empties = empties(self.layout.root)
        empties = [
            {
                'x': float(empty.get('x')),
                'y': float(empty.get('y'))
            }
            for empty in empties
        ]
        # Get squares that have the data class
        fillables = etree.XPath("//*[@class='data']")
        fillables = fillables(self.layout.root)
        fillables = [
            {
            'x': float(fillable.get('x')),
            'y': float(fillable.get('y')),
            'width': float(fillable.get('width')),
            'height': float(fillable.get('height')),
            }
            for fillable in fillables
            if {
                'x': float(fillable.get('x')),
                'y': float(fillable.get('y'))
            } not in empties
        ]
        return fillables

    def getLayout(self):
        return random.choice(self.layout_options)

    def write(self):
        label = click.style('Cards Processed', fg='yellow')
        with click.progressbar(self.data, label=label, show_eta=True) as data:
            for card in data:
                self.layout = sg.fromfile(self.getLayout())
                output_file = os.path.join(self.dir, '%05d.svg' % card['number'])
                numbers = []
                for k in card['card'].keys():
                    numbers = numbers + card['card'][k]
                w, h = self.layout.get_size()
                c = sg.SVGFigure(w, h)
                c.append(self.layout)
                fillables = self.getFillables()
                for i in range(len(numbers)):
                    fillable = fillables[i]
                    number = numbers[i]
                    txt = sg.TextElement(
                        fillable['x'] + (fillable['width'] - Writer.FONT_SIZE * Writer.H_FACTOR) / 2,
                        fillable['y'] + (fillable['height'] + Writer.FONT_SIZE * Writer.V_FACTOR) / 2,
                        "%02d" % number,
                        size=Writer.FONT_SIZE,
                        weight="bold",
                        font="Helvetica"
                    )
                    c.append(txt)
                c.save(output_file)
        print click.style('\nCards written to %s' % self.dir, fg='blue') + '\n'
