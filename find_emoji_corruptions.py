import os

roots = [
    r"d:\project\peyug_project\roamerly",
    r"d:\project\peyug_project\rise_academy"
]

print("Scanning for corrupted double-encoded sequences like â„ or ðŸ...")
for root in roots:
    print(f"Scanning directory: {root}")
    if not os.path.exists(root):
        continue
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(('.html', '.php', '.js', '.css')):
                fpath = os.path.join(dirpath, f)
                try:
                    # Read as UTF-8
                    with open(fpath, 'r', encoding='utf-8') as file_obj:
                        content = file_obj.read()
                    
                    # We check for the characters
                    # â„ is usually '\u00e2\u201e'
                    # ðŸ is usually '\u00f0\u0178'
                    # Let's check for both literal sequences
                    found = []
                    if "\u00e2\u201e" in content:
                        found.append("â„")
                    if "\u00f0\u0178" in content:
                        found.append("ðŸ")
                    if "â„" in content:
                        found.append("â„ (literal)")
                    if "ðŸ" in content:
                        found.append("ðŸ (literal)")
                        
                    if found:
                        print(f"  Found {found} in {fpath}")
                        # Print lines containing them
                        lines = content.split('\n')
                        for idx, line in enumerate(lines):
                            if any(x in line for x in ["\u00e2\u201e", "\u00f0\u0178", "â„", "ðŸ"]):
                                print(f"    Line {idx+1}: {repr(line)}")
                except Exception as e:
                    pass

print("Finished scanning.")
