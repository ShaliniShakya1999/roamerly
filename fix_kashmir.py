import urllib.request, os, shutil, glob, re

ROAMERLY = r'd:\project\peyug_project\roamerly'
WEB_DIR = os.path.join(ROAMERLY, 'assets', 'images', 'web')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Kashmir Dal Lake URLs - trying multiple
KASHMIR_URLS = [
    'https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1200&q=85',
    'https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=85',
    'https://images.unsplash.com/photo-1626015366271-3dcdb04a03f8?auto=format&fit=crop&w=1200&q=85',
    'https://images.unsplash.com/photo-1624461568900-5e2deb86a92c?auto=format&fit=crop&w=1200&q=85',
]

KASHMIR_FILE = os.path.join(WEB_DIR, 'photo-1598302842278-40e1e6988891.jpg')
KASHMIR_LOCAL = os.path.join(WEB_DIR, 'kashmir-dal-lake.jpg')

downloaded = False
for url in KASHMIR_URLS:
    print('Trying: ' + url[:60])
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        if len(data) > 50000:  # at least 50KB = real image
            open(KASHMIR_LOCAL, 'wb').write(data)
            open(KASHMIR_FILE, 'wb').write(data)  # also replace the wrong file
            print('  OK - ' + str(len(data)//1024) + 'KB')
            downloaded = True
            break
        else:
            print('  Too small: ' + str(len(data)) + ' bytes')
    except Exception as e:
        print('  FAILED: ' + str(e))

if not downloaded:
    print('All Kashmir URLs failed - using Manali image as fallback Kashmir')
    src = os.path.join(WEB_DIR, 'photo-1605649487212-47bdab064df7.jpg')
    shutil.copy(src, KASHMIR_FILE)
    shutil.copy(src, KASHMIR_LOCAL)

# Also fix the white-box image issue in index.html
# Check current image paths for package cards in index.html
print('\nChecking index.html image paths...')
idx = open(os.path.join(ROAMERLY, 'index.html'), encoding='utf-8').read()
img_matches = re.findall(r'src="([^"]*(?:web|destinations)[^"]*)"', idx)
for m in img_matches[:10]:
    full = os.path.join(ROAMERLY, m)
    exists = os.path.exists(full)
    print('  ' + m + ' -> ' + ('OK' if exists else 'MISSING'))

print('\nDone!')
