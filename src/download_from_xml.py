#encoding:UTF-8

import os
import requests
from xml.etree import cElementTree

url = 'https://storage.googleapis.com/lpr-ocr/'

response = requests.get(url)

tree = cElementTree.fromstring(response.content)

tgz_file = []
for i in tree:
    if len(i) > 0:
        tgz_file.extend([k for k in i[0].itertext()])

for i in tgz_file:
    os.system('nohup wget %s%s > 1.out'%(url, i))

print('end')