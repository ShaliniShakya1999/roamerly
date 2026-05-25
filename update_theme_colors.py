import os

roots = [
    r'd:\project\peyug_project\roamerly',
    r'd:\project\peyug_project\rise_academy'
]

replacements = {
    '#14B8A6': '#1E88E5',          # Primary Blue (Teal -> Royal Blue)
    '#F97316': '#FF8A65',          # Accent Orange (Orange -> Sunset Orange)
    '#0d9488': '#1565C0',          # Hover/Darker Teal -> Hover/Darker Royal Blue
    '#ea580c': '#e67650',          # Hover/Darker Orange -> Hover/Darker Sunset Orange
    '20,184,166': '30,136,229',    # RGB of Teal (compact)
    '20, 184, 166': '30, 136, 229', # RGB of Teal
    '249,115,22': '255,138,101',   # RGB of Orange (compact)
    '249, 115, 22': '255, 138, 101' # RGB of Orange
}

print("Scanning all HTML and PHP files for old theme colors...")
for root in roots:
    if not os.path.exists(root):
        continue
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(('.html', '.php', '.css')):
                fpath = os.path.join(dirpath, f)
                try:
                    with open(fpath, 'r', encoding='utf-8') as file_obj:
                        content = file_obj.read()
                    
                    modified = False
                    for bad, good in replacements.items():
                        # Case-insensitive for hex
                        if bad.startswith('#'):
                            bad_l = bad.lower()
                            if bad_l in content:
                                content = content.replace(bad_l, good)
                                modified = True
                            bad_u = bad.upper()
                            if bad_u in content:
                                content = content.replace(bad_u, good)
                                modified = True
                        else:
                            if bad in content:
                                content = content.replace(bad, good)
                                modified = True
                    
                    if modified:
                        with open(fpath, 'w', encoding='utf-8') as file_obj:
                            file_obj.write(content)
                        print(f"  Updated color references in: {fpath}")
                except Exception as e:
                    pass

print("Finished scanning and updating all color references.")
