import os
import glob
import re

html_files = glob.glob('*.html')

newsletter_pattern = re.compile(
    r'<!--\s*Newsletter\s*-->\s*<section class="py-5">\s*<div class="container text-center py-5">.*?</div>\s*</section>\s*',
    re.DOTALL
)

count = 0
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = newsletter_pattern.sub('', content)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed newsletter from {file}")
        count += 1

print(f"Total files updated: {count}")
