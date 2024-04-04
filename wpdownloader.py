#!/usr/bin/env python3
import requests,os,re
from tqdm import tqdm
from sys import argv
s = requests.Session()
url = argv[1]
def dataurl(url):
	def page_numbers():
		num = 1
		while True:
			yield num
			num += 1
	allpages=[]
	a = s.get(url)
	if a.status_code != 200: a.raise_for_status()
	for page in tqdm(page_numbers()):
		a = s.get(url,params={"page":page,"per_page": 100}).json()
		if isinstance(a, dict) and a["code"] == "rest_post_invalid_page_number":
			break
		allpages+=a
	return allpages
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
		y = i['guid']['rendered'] if url.replace("https","http") in i['guid']['rendered'] or url in i['guid']['rendered'] else f"{url}{i['guid']['rendered']}"
		r = s.get(y, allow_redirects=True)
		if r.status_code != 200: r.raise_for_status()
		open(pth,'wb').write(r.content)
if int(argv[2]):
	data = dataurl(f"{url}/wp-json/wp/v2/posts/")
	html(data)
if int(argv[3]):
	data = dataurl(f"{url}/wp-json/wp/v2/pages/")
	html(data)
if int(argv[4]):
	data = dataurl(f"{url}/wp-json/wp/v2/media/")
	media(data)

