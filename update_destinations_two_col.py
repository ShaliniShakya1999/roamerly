import os
import re
from update_destinations_menu import build_destinations_dropdown

dest_html = build_destinations_dropdown()

for fname in os.listdir('.'):
    if not fname.endswith('.html'):
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r'<!-- Destinations Dropdown -->.*?destinations-mega.*?</ul>\s*</li>',
        dest_html.strip(),
        content,
        count=1,
        flags=re.DOTALL,
    )

    if new_content != content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {fname}')
    else:
        print(f'Skip (no match) {fname}')

print('Two-column Destinations menu applied.')
