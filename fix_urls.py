import os, re, glob

ROAMERLY = r'd:\project\peyug_project\roamerly'

all_files = glob.glob(os.path.join(ROAMERLY, '*.html'))
all_files += glob.glob(os.path.join(ROAMERLY, 'assets', 'css', '*.css'))

unsplash_pat = re.compile(r'https://images\.unsplash\.com/photo-([\w-]+)(\?[^\s"\'<>]*)?')
randomuser_pat = re.compile(r'https://randomuser\.me/api/portraits/([\w]+)/(\d+)\.jpg')

def replace_unsplash(m, is_css):
    photo_id = m.group(1)
    local_name = 'photo-' + photo_id + '.jpg'
    full = os.path.join(ROAMERLY, 'assets', 'images', 'web', local_name)
    if os.path.exists(full):
        if is_css:
            return '../images/web/' + local_name
        return 'assets/images/web/' + local_name
    return m.group(0)

def replace_randomuser(m, is_css):
    g = m.group(1)
    n = m.group(2)
    local_name = 'avatar-' + g + '-' + n + '.jpg'
    full = os.path.join(ROAMERLY, 'assets', 'images', 'web', local_name)
    if os.path.exists(full):
        if is_css:
            return '../images/web/' + local_name
        return 'assets/images/web/' + local_name
    return m.group(0)

updated = 0
for fpath in all_files:
    is_css = fpath.endswith('.css')
    try:
        content = open(fpath, encoding='utf-8').read()
    except:
        continue
    original = content

    content = unsplash_pat.sub(lambda m: replace_unsplash(m, is_css), content)
    content = randomuser_pat.sub(lambda m: replace_randomuser(m, is_css), content)

    if content != original:
        open(fpath, 'w', encoding='utf-8').write(content)
        print('Updated: ' + os.path.basename(fpath))
        updated += 1

print('Total updated: ' + str(updated) + ' files')

remaining = 0
for fpath in all_files:
    try:
        c = open(fpath, encoding='utf-8').read()
        remaining += len(re.findall(r'images\.unsplash\.com', c))
    except:
        pass
print('Remaining unsplash URLs: ' + str(remaining))
