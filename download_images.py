import os, re, time, glob
import urllib.request
from collections import OrderedDict

ROAMERLY = r'd:\project\peyug_project\roamerly'
WEB_IMG_DIR = os.path.join(ROAMERLY, 'assets', 'images', 'web')
os.makedirs(WEB_IMG_DIR, exist_ok=True)

# Find all HTML and CSS files
html_files = glob.glob(os.path.join(ROAMERLY, '*.html'))
css_files = glob.glob(os.path.join(ROAMERLY, 'assets', 'css', '*.css'))
all_files = html_files + css_files

# Patterns to find
unsplash_pat = re.compile(r'https://images\.unsplash\.com/photo-([\w-]+)(\?[^\s"\'<>]*)?')
randomuser_pat = re.compile(r'https://randomuser\.me/api/portraits/([\w]+)/(\d+)\.jpg')

# Map: original_url -> (local_filename, full_download_url)
url_map = OrderedDict()

for fpath in all_files:
    is_css = fpath.endswith('.css')
    try:
        content = open(fpath, encoding='utf-8').read()
    except:
        continue

    for m in unsplash_pat.finditer(content):
        orig_url = m.group(0)
        photo_id = m.group(1)
        local_name = f'photo-{photo_id}.jpg'
        download_url = f'https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=1200&q=85'
        if orig_url not in url_map:
            url_map[orig_url] = (local_name, download_url, is_css)

    for m in randomuser_pat.finditer(content):
        orig_url = m.group(0)
        gender = m.group(1)
        num = m.group(2)
        local_name = f'avatar-{gender}-{num}.jpg'
        if orig_url not in url_map:
            url_map[orig_url] = (local_name, orig_url, is_css)

print(f"Found {len(url_map)} unique external images\n")

# Group by local_name to avoid duplicate downloads
downloaded = set()
for orig_url, (local_name, download_url, _) in url_map.items():
    full_path = os.path.join(WEB_IMG_DIR, local_name)
    if local_name in downloaded or os.path.exists(full_path):
        size = os.path.getsize(full_path) if os.path.exists(full_path) else 0
        print(f"  SKIP (exists {size//1024}KB): {local_name}")
        downloaded.add(local_name)
        continue

    print(f"  Downloading: {local_name} ...")
    try:
        req = urllib.request.Request(download_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(full_path, 'wb') as f:
            f.write(data)
        print(f"    OK ({len(data)//1024} KB)")
        downloaded.add(local_name)
        time.sleep(0.4)
    except Exception as e:
        print(f"    FAILED: {e}")

print("\nUpdating HTML and CSS files...")

for fpath in all_files:
    is_css = fpath.endswith('.css')
    try:
        content = open(fpath, encoding='utf-8').read()
    except:
        continue

    original = content
    for orig_url, (local_name, _, _) in url_map.items():
        full_local = os.path.join(WEB_IMG_DIR, local_name)
        if not os.path.exists(full_local):
            continue
        if is_css:
            rel_path = f'../images/web/{local_name}'
        else:
            rel_path = f'assets/images/web/{local_name}'
        content = content.replace(orig_url, rel_path)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {os.path.basename(fpath)}")

print("\nDone!")
