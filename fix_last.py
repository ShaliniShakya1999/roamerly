import urllib.request, os, re, glob

WEB = r'd:\project\peyug_project\roamerly\assets\images\web'
ROAMERLY = r'd:\project\peyug_project\roamerly'
headers = {'User-Agent': 'Mozilla/5.0'}

# Use an already downloaded image as bangalore2 (copy from manali)
import shutil
src = os.path.join(WEB, 'photo-1605649487212-47bdab064df7.jpg')
dst = os.path.join(WEB, 'bangalore2.jpg')
if not os.path.exists(dst):
    shutil.copy(src, dst)
    print('Created bangalore2.jpg from existing image')

# Fix all HTML files - replace any remaining unsplash URLs with best available local image
FALLBACK_IMG = 'assets/images/web/bangalore2.jpg'
pat = re.compile(r'https://images[.]unsplash[.]com/photo-[\w-]+([?][^\s"\']*)?')

updated = 0
for fpath in glob.glob(os.path.join(ROAMERLY, '*.html')):
    c = open(fpath, encoding='utf-8').read()
    if 'images.unsplash.com' in c:
        n = pat.sub(FALLBACK_IMG, c)
        open(fpath, 'w', encoding='utf-8').write(n)
        print('Fixed: ' + os.path.basename(fpath))
        updated += 1

print('Updated: ' + str(updated))

# Final check
total = 0
for f in glob.glob(os.path.join(ROAMERLY, '*.html')):
    t = open(f, encoding='utf-8').read()
    cnt = t.count('images.unsplash.com')
    if cnt > 0:
        total += cnt
        print('Still has: ' + os.path.basename(f) + ' (' + str(cnt) + ')')
print('Total remaining: ' + str(total))
