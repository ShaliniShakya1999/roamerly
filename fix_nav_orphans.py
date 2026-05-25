import os
import re

for fname in os.listdir('.'):
    if not fname.endswith('.html'):
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    fixed = re.sub(
        r'(\s*<li><a class="dropdown-item" href="europe\.html">Europe</a></li>\s*</ul>\s*</li>)'
        r'(?:\s*<li>.*?</li>\s*)+\s*</ul>\s*</li>\s*'
        r'(\s*<!-- Adventure Trips Dropdown -->)',
        r'\1\n\n\2',
        content,
        count=1,
        flags=re.DOTALL,
    )

    if fixed != content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f'Fixed {fname}')
    else:
        print(f'No change {fname}')
