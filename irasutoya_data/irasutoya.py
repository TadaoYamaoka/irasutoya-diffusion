import requests
from bs4 import BeautifulSoup
import json
import glob

exists = []
for name in glob.glob('*.json'):
    exists.append(name[:-5])

html = requests.get(r'https://www.irasutoya.com/').text

soup = BeautifulSoup(html, 'lxml')
for tag in soup.html.body.select('h2'):
    if tag.text == r'詳細カテゴリー':
        for a in tag.parent.select('a[href]'):
            category = a.text.strip()
            if category in exists:
                continue
            print(category)
            data = []
            html2 = requests.get(a.attrs['href']).text
            while True:
                soup2 = BeautifulSoup(html2, 'lxml')
                for a2 in soup2.html.body.select('#Blog1 .boxim a[href]'):
                    html3 = requests.get(a2.attrs['href']).text
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
                    data.append({
                        'category': category,
                        'url': a2.attrs['href'],
                        'title': title,
                        'caption': caption.strip(),
                        'links': links
                    })
                next = soup2.html.body.select('#Blog1_blog-pager-older-link')
                if len(next) > 0:
                    html2 = requests.get(next[0].attrs['href']).text
                    continue
                break
            with open(a.text + '.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        break
