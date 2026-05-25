import os, re, glob, time
import urllib.request

ROAMERLY = r'd:\project\peyug_project\roamerly'
WEB_DIR = os.path.join(ROAMERLY, 'assets', 'images', 'web')

# Map broken photo IDs -> replacement working Unsplash photos
REPLACEMENTS = {
    '1523482585902-397e813c5a79': ('australia-landscape.jpg',   'https://images.unsplash.com/photo-1491466424936-e304919aada7?auto=format&fit=crop&w=1200&q=85'),
    '1529258288937-d121e6b29c74': ('bangalore-city.jpg',        'https://images.unsplash.com/photo-1596176530528-c7df5d42b0a5?auto=format&fit=crop&w=1200&q=85'),
    '1596176530528-1b6f4a8b0b0e': ('bangalore-garden.jpg',      'https://images.unsplash.com/photo-1520059001898-e7f43fb6abce?auto=format&fit=crop&w=1200&q=85'),
    '1503614472-8c93d83e29b4':   ('canada-mountains.jpg',       'https://images.unsplash.com/photo-1500932334442-8761ee4810a7?auto=format&fit=crop&w=1200&q=85'),
    '1544551763-46efeeeb4f72':   ('caribbean-beach.jpg',        'https://images.unsplash.com/photo-1501286353178-1ec881214838?auto=format&fit=crop&w=1200&q=85'),
    '1588668216169-48a4b0b0b0e': ('chennai-temple.jpg',         'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=85'),
    '1477587453913-6739373a0e0b': ('jaipur-fort.jpg',           'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=85'),
    '1602216052126-53b0b0b0b0e': ('kochi-backwaters.jpg',       'https://images.unsplash.com/photo-1591018653054-d3ba1bc1c5f5?auto=format&fit=crop&w=1200&q=85'),
    '1570168007204-d1bf43f0b0b0e': ('mumbai-city.jpg',          'https://images.unsplash.com/photo-1567157577867-05ccb1388e66?auto=format&fit=crop&w=1200&q=85'),
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Download replacement images
print("Downloading replacement images...")
for broken_id, (fname, url) in REPLACEMENTS.items():
    full = os.path.join(WEB_DIR, fname)
    if os.path.exists(full):
        print(f"  EXISTS: {fname}")
        continue
    print(f"  Downloading {fname}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        open(full, 'wb').write(data)
        print(f"    OK {len(data)//1024}KB")
        time.sleep(0.3)
    except Exception as e:
        print(f"    FAILED: {e}")

# Update HTML files - replace broken Unsplash URLs with local images
all_files = glob.glob(os.path.join(ROAMERLY, '*.html'))
pat = re.compile(r'https://images\.unsplash\.com/photo-([\w-]+)(\?[^\s"\'<>]*)?')

def replacer(m):
    photo_id = m.group(1)
    if photo_id in REPLACEMENTS:
        fname = REPLACEMENTS[photo_id][0]
        full = os.path.join(WEB_DIR, fname)
        if os.path.exists(full):
            return 'assets/images/web/' + fname
    return m.group(0)

updated = 0
for fpath in all_files:
    try:
        content = open(fpath, encoding='utf-8').read()
    except:
        continue
    new_content = pat.sub(replacer, content)
    if new_content != content:
        open(fpath, 'w', encoding='utf-8').write(new_content)
        print(f"Updated: {os.path.basename(fpath)}")
        updated += 1

print(f"\nUpdated {updated} files")

# Final count
remaining = sum(
    len(re.findall(r'images\.unsplash\.com', open(f, encoding='utf-8').read()))
    for f in all_files
    if os.path.exists(f)
)
print(f"Remaining unsplash URLs: {remaining}")
