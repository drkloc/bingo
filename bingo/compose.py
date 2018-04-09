import json, os, click
from datetime import datetime as dt
from bingo.composer import Composer

WORKING_DIR = os.getcwd()
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

@click.command()
@click.option('--cards', required=True, help='Directory Containing the cards')
@click.option('--cards_per_page', default=6, help='How many cards per pdf page?')
@click.option('--confirm/--no-confirm', default=True)
def compose(cards, cards_per_page, confirm):
    click.clear()
    print '\n'
    print click.style('                          ', bg='blue')
    print click.style('   BINGO CARD COMPOSER    ', bg='blue', fg='white')
    print click.style('                          ', bg='blue')
    print '\n'
    cards = os.path.abspath(cards)
    # Let user confirm his options
    d = {
        'cards': cards,
        'cards_per_page': cards_per_page
    }
    d = ['%s %s' % (click.style('%s' % k, fg='red'), d[k]) for k in d.keys()]
    d = '\n'.join(d)
    if confirm:
        click.confirm(click.style('\nDo you want to continue with the following options?', fg='green') + '\n\n%s\n' % d, abort=True)
    else:
        print click.style('\nWriting', fg='green') + '\n\n%s\n' % d
    # Compose pdf.
    composer = Composer(cards, cards_per_page)
    composer.write()
    print '\n'
    print click.style('                         ', bg='green')
    print click.style('         SUCCESS         ', bg='green', fg='black')
    print click.style('                         ', bg='green')
    print '\n'

if __name__ == '__main__':
    compose()
