import click
import bandit
import subprocess
import json


@click.command()
def runCLI():
    # print(__name__)

    file = "test.py" # temporary hardcoded location


    bandit = subprocess.Popen(["bandit", "-f", "json", file, "-q"], stdout=subprocess.PIPE)
    output = bandit.communicate()
    output_json = json.loads(output[0].decode('utf8'))
    # print(type(output_json))

    # for x, y in output_json.items() : print(x, y)
    # print(output_json['results'])

    for x in output_json['results'] :
        for y, z in x.items() : print(y, z)


if __name__ == '__main__':
    runCLI()