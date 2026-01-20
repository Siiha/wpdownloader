#!/usr/bin/env python3
import requests,os,re
from tqdm import tqdm
from sys import argv
import unicodedata
import urllib
import mimetypes
s = requests.Session()
url,post,page,media = argv[1:5] # url, download posts(1/0), pages(1/0), media(1/0)
def dataurl(url): # downloads all pages of a WP REST API endpoint
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
def html(data): # saves posts/pages as html files
	os.makedirs('html', exist_ok=True)
	for i in data:
		a = i['title']['rendered'].replace('ä','a')
		a = os.path.join('html',f"{re.sub("[^a-z0-9]+", "_", a, flags=re.I)}.html")
		if os.path.isfile(a) : continue
		open(a,'w').write(i['content']['rendered'])

def safe_filename(name: str) -> str:
    name = name.split('?', 1)[0].split('#', 1)[0]
    name = unicodedata.normalize('NFKD', name)
    name = re.sub(r'[^a-zA-Z0-9._-]+', '_', name).strip('._')
    return name or 'file'

def guess_ext_from_content_type(ct: str) -> str:
    if not ct:
        return ''
    ext = mimetypes.guess_extension(ct.split(';', 1)[0].strip())
    return {'.jpe': '.jpg'}.get(ext, ext or '')


def Media(data):  # downloads media files
    ext_to_dir = {
        '.png': 'pictures',
        '.jpg': 'pictures',
        '.jpeg': 'pictures',
        '.webp': 'pictures',
        '.gif': 'pictures',
        '.svg': 'svg',
        '.pdf': 'pdf',
    }

    for i in data:
        src = i.get('source_url') or i.get('guid', {}).get('rendered')
        if not src:
            continue

        parsed = urllib.parse.urlparse(src)
        last_seg = os.path.basename(parsed.path)
        fname = safe_filename(last_seg)

        
        ext = os.path.splitext(fname)[1].lower() if fname else ''

        # 4) Päätä kohdekansio
        dest_dir = ext_to_dir.get(ext, 'other')

        
        if os.path.isfile(dest_dir):
            dest_dir = dest_dir + '_files'
        os.makedirs(dest_dir, exist_ok=True)

        if src.startswith('//'):
            src = 'https:' + src
        elif src.startswith('/'):
            
            base = url.rstrip('/')
            p = urllib.parse.urlparse(base)
            root = f"{p.scheme}://{p.netloc}"
            src = urllib.parse.urljoin(root + '/', src.lstrip('/'))

        
        r = s.get(src, allow_redirects=True, timeout=60)
        if r.status_code >= 400:
            
            if src.startswith('https://'):
                retry = 'http://' + src[len('https://'):]
            elif src.startswith('http://'):
                retry = 'https://' + src[len('http://'):]
            else:
                retry = src
            r = s.get(retry, allow_redirects=True, timeout=60)
            r.raise_for_status()

        if not fname or not ext:
            ct = r.headers.get('Content-Type', '')
            guessed_ext = guess_ext_from_content_type(ct)
            if not fname:
                media_id = i.get('id')
                base = f"file_{media_id}" if media_id is not None else "file"
                fname = base + (guessed_ext or '.bin')
            elif not ext and guessed_ext:
                fname = fname + guessed_ext

        fname = safe_filename(fname)
        if not os.path.splitext(fname)[1]:
            fname = fname + '.bin'

        pth = os.path.join(dest_dir, fname)

        if os.path.isfile(pth):
            continue

        with open(pth, 'wb') as f: # write file
            f.write(r.content)

if int(post):
	data = dataurl(f"{url}/wp-json/wp/v2/posts/")
	html(data)
if int(page):
	data = dataurl(f"{url}/wp-json/wp/v2/pages/")
	html(data)
if int(media):
	data = dataurl(f"{url}/wp-json/wp/v2/media/")
	Media(data)

