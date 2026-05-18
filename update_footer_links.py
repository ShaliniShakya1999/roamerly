import os
import glob

replacements = [
    ('<a href="#" class="footer-link">Contact Us</a>', '<a href="contact.html" class="footer-link">Contact Us</a>'),
    ('<a href="#" class="footer-link">USA</a>', '<a href="usa.html" class="footer-link">USA</a>'),
    ('<a href="#" class="footer-link">Canada</a>', '<a href="canada.html" class="footer-link">Canada</a>'),
    ('<a href="#" class="footer-link">Australia</a>', '<a href="australia.html" class="footer-link">Australia</a>'),
    ('<a href="#" class="footer-link">New Zealand</a>', '<a href="new-zealand.html" class="footer-link">New Zealand</a>'),
    ('<a href="#" class="footer-link">Middle East</a>', '<a href="middle-east.html" class="footer-link">Middle East</a>'),
    ('<a href="#" class="footer-link">Africa</a>', '<a href="africa.html" class="footer-link">Africa</a>'),
    ('<a href="#" class="footer-link">Far East</a>', '<a href="far-east.html" class="footer-link">Far East</a>'),
    ('<a href="#" class="footer-link">Latin America</a>', '<a href="latin-america.html" class="footer-link">Latin America</a>'),
    ('<a href="#" class="footer-link">Europe</a>', '<a href="europe.html" class="footer-link">Europe</a>')
]

html_files = glob.glob('*.html')
count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated footer in {file}")

print(f"Total files updated: {count}")
