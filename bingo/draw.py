import json, os, click
from datetime import datetime as dt
from bingo.writer import Writer

WORKING_DIR = os.getcwd()
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

@click.command()
@click.option('--cards', help='JSON File with the data for the cards')
@click.option('--layout', default=False, help='Where do we find layout files?')
@click.option('--confirm/--no-confirm', default=True)
def draw(cards, layout, confirm):
    click.clear()
    print '\n'
    print click.style('                          ', bg='blue')
    print click.style('    BINGO CARDS DRAWER    ', bg='blue', fg='white')
    print click.style('                          ', bg='blue')
    print '\n'
    cards = os.path.abspath(cards)
    # Provide better defaults for data and layout
    if not layout:
        layout = os.path.join(WORKING_DIR, 'layout')
    # Prompt user for layout options.
    if not '.svg' in layout:
        # List layout files and prompt user for which to use.
        layout_files = [f for f in os.listdir(layout) if f.endswith('.svg')]
        layout_options = ['%s %s' % (click.style('%s)' % (i + 1),fg='red') , layout_files[i]) for i in range(len(layout_files))]
        layout_options = '\n'.join(layout_options)
        value = click.prompt(
            click.style('Which layout files should I use?', fg='green') +
            '\n\n%s\n' % layout_options,
            default='1'
        )
        value = value.split(',')
        value = [(int(v)-1) for v in value if int(v)]
        if len(value):
            layout_files = [layout_files[i] for i in value]
        layout = [os.path.join(layout, f) for f in layout_files]
    else:
        layout = [os.path.abspath(layout)]
    # Let user confirm his options
    d = {
        'cards': cards,
        'layout': layout
    }
    d = ['%s %s' % (click.style('%s' % k, fg='red'), d[k]) for k in d.keys()]
    d = '\n'.join(d)
    if confirm:
        click.confirm(click.style('\nDo you want to continue with the following options?', fg='green') + '\n\n%s\n' % d, abort=True)
    else:
        print click.style('\nWriting', fg='green') + '\n\n%s\n' % d
    # Draw cards.
    writer = Writer(cards, layout)
    writer.write()
    print '\n'
    print click.style('                         ', bg='green')
    print click.style('         SUCCESS         ', bg='green', fg='black')
    print click.style('                         ', bg='green')
    print '\n'

if __name__ == '__main__':
    draw()
