import json
import glob
import requests
from bs4 import BeautifulSoup

for file in glob.glob('*.json'):
    fix = False
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for row in data:
            if row['links'] == []:
                print(row['url'])

                html3 = requests.get(row['url']).text
                soup3 = BeautifulSoup(html3, 'lxml')
                title = soup3.html.body.select('div.title h2')[0].text.strip()
                links = []
                for a3 in soup3.html.body.select('div.entry a[href]'):
                    if a3.attrs['href'][-4:] in ['.png', '.jpg'] or 'blogger.googleusercontent.com/img' in a3.attrs['href']:
                        links.append(a3.attrs['href'])
                caption = ''
                for tag3 in soup3.html.body.select('div.entry div,div.entry p,div.entry a'):
                    if len(tag3.text) > 3 and len(tag3.text) > len(caption):
                        caption = tag3.text
                print(title + ',\t' + caption.strip())
                row['links'] = links
                fix = True
    if fix:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
