import os, re, glob, time, urllib.request

ROAMERLY = r'd:\project\peyug_project\roamerly'
WEB_DIR = os.path.join(ROAMERLY, 'assets', 'images', 'web')
headers = {'User-Agent': 'Mozilla/5.0'}

FINAL = {
    '1529258288937-d121e6b29c74': ('bangalore2.jpg', 'https://images.unsplash.com/photo-1570168007204-d1bf43f0b0b0e?auto=format&fit=crop&w=1200&q=85'),
    '1596176530528-1b6f4a8b0b0e': ('bangalore3.jpg', 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=85'),
    '1602216052126-53b0b0b0b0e': ('kochi2.jpg', 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=85'),
}

for broken_id, (fname, url) in FINAL.items():
    full = os.path.join(WEB_DIR, fname)
    print('Downloading ' + fname)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        open(full, 'wb').write(data)
        print('  OK ' + str(len(data)//1024) + 'KB')
        time.sleep(0.3)
    except Exception as e:
        print('  FAIL: ' + str(e))

pat = re.compile(r'https://images\.unsplash\.com/photo-([\w-]+)(\?[^\s"\']*)?')

def rep(m):
    pid = m.group(1)
    if pid in FINAL:
        f = FINAL[pid][0]
        if os.path.exists(os.path.join(WEB_DIR, f)):
            return 'assets/images/web/' + f
    return m.group(0)

for fpath in glob.glob(os.path.join(ROAMERLY, '*.html')):
    c = open(fpath, encoding='utf-8').read()
    n = pat.sub(rep, c)
    if n != c:
        open(fpath, 'w', encoding='utf-8').write(n)
        print('Fixed: ' + os.path.basename(fpath))

total = 0
for f in glob.glob(os.path.join(ROAMERLY, '*.html')):
    total += len(re.findall('images.unsplash.com', open(f, encoding='utf-8').read()))
print('Final remaining: ' + str(total))
