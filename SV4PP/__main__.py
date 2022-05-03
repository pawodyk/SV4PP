import click

@click.command()
def runCLI():
    print(__name__)




if __name__ == '__main__':
    runCLI()