import requests
import os

dv = requests.get('https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/RYEANM')
dv.raise_for_status()

data = dv.json()

files = data['data']['latestVersion']['files']

root = '/Volumes/external/w51/apex/'

for fd in files:

    result = requests.get('https://dataverse.harvard.edu//api/access/datafile/{id}'
                          .format(**fd['dataFile']),
                          stream=True)
    result.raise_for_status()

    with open(os.path.join(root, fd['dataFile']['filename']), 'wb') as fh:
        fh.write(result.content)
