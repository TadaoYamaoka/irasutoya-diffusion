import json
import pandas as pd
import glob
import os
import re

exclude_ptn = re.compile(r'^.*message_memo.*\.jpg$')
data = []
dic = {}
for file in glob.glob('*.json'):
    with open(file, 'r', encoding='utf-8') as f:
        for row in json.load(f):
            if row['url'] in ['https://www.irasutoya.com/2013/02/50.html', 'https://www.irasutoya.com/2014/10/blog-post_7.html', 'https://www.irasutoya.com/2020/01/blog-post_67.html']:
                continue
            # if row['url'] in dic:
            #     for record in dic[row['url']]:
            #         record[row['category']] = 1
            #     continue
            basedir = row['url'][len('https://www.irasutoya.com/'):-len('.html')]
            # 1つのみに絞る
            if len(row['links']) > 1:
                continue
            caption = row['caption']
            if caption == '':
                caption = row['title']
            for i, link in enumerate(row['links']):
                if exclude_ptn.match(link):
                    continue
                pathname = os.path.join('img', basedir, str(i), '*')
                if pathname == 'img/2016/09/blog-post_307/1/*':
                    continue
                files = glob.glob(pathname)
                assert len(files) == 1
                path = files[0]
                record = {
                    'url': row['url'],
                    'title': row['title'],
                    'caption': caption,
                    'path': path,
                    'index': i,
                    # row['category']: 1,
                }
                data.append(record)
                # if i == 0:
                #     dic[row['url']] = [record]
                # else:
                #     dic[row['url']].append(record)

pd.DataFrame(data).to_csv('irasutoya.csv', index=False)
