import json, os, click
from datetime import datetime as dt

from bingo.shuffler import Cards
from bingo.writer import Writer

WORKING_DIR = os.getcwd()
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

@click.command()
@click.option('--cards', default=5, help='Number of cards for the set')
@click.option('--minimum', default=1, help='Min Number for the distribution')
@click.option('--maximum', default=90, help='Max Number for the distribution')
@click.option('--rows', default=3, help='Rows')
@click.option('--columns', default=5, help='Columns')
@click.option('--data', default=False, help='Where do we store the cards?')
@click.option('--confirm/--no-confirm', default=True)
def shuffle(cards, minimum, maximum, rows, columns, data, confirm):
    click.clear()
    print '\n'
    print click.style('                         ', bg='blue')
    print click.style('     BINGO SHUFFLER      ', bg='blue', fg='white')
    print click.style('                         ', bg='blue')
    print '\n'
    # Provide better defaults for data and layout
    if not data:
        data = os.path.join(WORKING_DIR, 'data')
        if not os.path.exists(data):
            os.makedirs(data)
    # Let user confirm his options
    d = {
        'cards': cards,
        'range': '%s-%s' % (minimum, maximum),
        'size': '%sx%s' % (rows, columns),
        'data': data,
    }
    d = ['%s %s' % (click.style('%s' % k, fg='red'), d[k]) for k in d.keys()]
    d = '\n'.join(d)
    if confirm:
        click.confirm(click.style('\nDo you want to continue with the following options?', fg='green') + '\n\n%s\n' % d, abort=True)
    else:
        print click.style('\nWriting', fg='green') + '\n\n%s\n' % d
    # Shuffle cards.
    cards = Cards().shuffle(cards, minimum, maximum, rows, columns)
    OUTPUT = os.path.join(data, '%s.json' % dt.now().strftime("%Y-%m-%dT%H-%M-%S"))
    with open(OUTPUT, 'w') as output:
        json.dump(cards, output)
    print '\n'
    print 'Data writed to ' + click.style(OUTPUT, fg='blue')
    print '\n'
    print click.style('                         ', bg='green')
    print click.style('         SUCCESS         ', bg='green', fg='black')
    print click.style('                         ', bg='green')
    print '\n'

if __name__ == '__main__':
    shuffle()
