import requests
import json

URL = 'https://pypi.org/stats/'

r = requests.get(URL, headers={"Accept": "application/json", "Content-Type": "application/json"})
if r.status_code == 200:
    response = r.json()
    
    with open('top_pypi.json', 'w') as f:
        f.write(json.dumps(response, indent=4))

else:
    print('request failed with status code ', r.status_code)

import pypistats
from pprint import pprint

# Call the API

pprint(pypistats.recent("castle-cms", "week", format="json"))
pprint(pypistats.recent("castle.cms", "week", format="json"))
print()
pprint(pypistats.recent("click", "week", format="json"))
pprint(pypistats.recent("aclick", "week", format="json"))

pprint(pypistats.recent("clack", "week", format="json"))
pprint(pypistats.recent("clic", "week", format="json"))
pprint(pypistats.recent("click8", "week", format="json"))


# pprint(pypistats.overall("pillow", mirrors=False, format="json"))

# pprint(pypistats.python_major("pillow", version="3", format="json"))

# pprint(pypistats.python_minor("pillow", version="3.7", format="json"))

# pprint(pypistats.system("pillow", os="linux", format="json"))