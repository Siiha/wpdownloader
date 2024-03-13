#!/usr/bin/env python3
import requests,os,re
from sys import argv
s = requests.Session()
url = argv[1]
def dataurl(url):
	with s.get(url) as url:
		if url.status_code != 200: url.raise_for_status()
		return url.json()
def html(data):
	os.makedirs('html', exist_ok=True)
	for i in data:
		a = i['title']['rendered'].replace('ä','a')
		a = os.path.join('html',f"{re.sub("[^a-z0-9]+", "_", a, flags=re.I)}.html")
		if os.path.isfile(a) : continue
		open(a,'w').write(i['content']['rendered'])
def media(data):
	ext_to_dir = {
    '.png': 'pictures',
    '.pdf': 'pdf',
    '.jpg': 'pictures',
	}
	for i in data:
		a = i['guid']['rendered'].split("/")[-1]
		dir = ext_to_dir.get(os.path.splitext(a)[1], 'other')
		os.makedirs(dir, exist_ok=True)
		pth = os.path.join('.',dir,a)
		if os.path.isfile(pth): continue
		r = s.get(f"{url}{i['guid']['rendered']}", allow_redirects=True)
		if r.status_code != 200: r.raise_for_status()
		open(pth,'wb').write(r.content)
data = dataurl(f"{url}/wp-json/wp/v2/posts/?_fields=title,content&?_embed&per_page=100")
html(data)
data = dataurl(f"{url}/wp-json/wp/v2/pages/?_fields=title,content&?_embed&per_page=100")
html(data)
data = dataurl(f"{url}/wp-json/wp/v2/media/?_fields=title,guid&?_embed&per_page=100")
media(data)
