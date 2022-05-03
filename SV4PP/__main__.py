import click
import bandit
import subprocess


@click.command()
def runCLI():
    # print(__name__)

    file = "test.py" # temporary hardcoded location


    bandit = subprocess.Popen(["bandit", "-h"], stdout=subprocess.PIPE)
    print(bandit.communicate())



if __name__ == '__main__':
    runCLI()