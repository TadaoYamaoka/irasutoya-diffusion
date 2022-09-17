import json
import glob
import requests
import os

for file in glob.glob('*.json'):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for row in data:
            if row['links'] != []:
                print(row['url'])
                assert row['url'].startswith('https://www.irasutoya.com/')
                assert row['url'].endswith('.html')
                basedir = row['url'][len('https://www.irasutoya.com/'):-len('.html')]
                for i, link in enumerate(row['links']):
                    dir = os.path.join('img', basedir, str(i))
                    try:
                        os.makedirs(dir)
                    except:
                        print('skip', link)
                        continue
                    if link.startswith('//'):
                        link = 'https:' + link
                    elif link.startswith('https:/1'):
                        link = 'https://' + link[len('https:/'):]
                    req = requests.get(link)
                    try:
                        content_disposition = req.headers['Content-Disposition']
                    except:
                        print('err', link)
                        continue
                    assert content_disposition.startswith('inline;filename="')
                    name = content_disposition[len('inline;filename="'):-1]
                    path = os.path.join(dir, name)
                    with open(path, 'wb') as out:
                        out.write(req.content)
