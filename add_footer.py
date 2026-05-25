import os, re, glob

ROAMERLY = r'd:\project\peyug_project\roamerly'

# Extract full footer from india.html (which has the complete footer)
india = open(os.path.join(ROAMERLY, 'india.html'), encoding='utf-8').read()

# Extract footer block
footer_match = re.search(r'(<footer\s+id="contact".*?</footer>)', india, re.DOTALL)
if not footer_match:
    print('ERROR: footer not found in india.html')
    exit()

FULL_FOOTER = footer_match.group(1)
print('Footer extracted: ' + str(len(FULL_FOOTER)) + ' chars')

# Also extract the floating buttons + chatbot + search overlay + JS from india.html
# Get everything after </footer> and before </body>
after_footer = re.search(r'</footer>(.*?)</body>', india, re.DOTALL)
AFTER_FOOTER = after_footer.group(1).strip() if after_footer else ''

# Pages that already have full footer
SKIP = {'contact.html', 'index.html', 'india.html', 'ooty.html'}

# Process all HTML files
updated = 0
for fpath in sorted(glob.glob(os.path.join(ROAMERLY, '*.html'))):
    name = os.path.basename(fpath)
    if name in SKIP:
        print('SKIP: ' + name)
        continue

    content = open(fpath, encoding='utf-8').read()

    # Check if already has full footer
    if 'footer-title' in content or 'newsletter' in content:
        print('SKIP (already has footer): ' + name)
        continue

    # Remove existing simple footer if any
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)

    # Remove old floating buttons / chatbot / scripts if present to avoid duplicates
    # Find the position of JS scripts section (last <script> block or </body>)
    
    # Remove existing search overlay
    content = re.sub(r'<!--\s*Fullscreen Search Overlay\s*-->.*?</div>\s*(?=\s*<!--)', '', content, flags=re.DOTALL)
    
    # Remove existing floating buttons
    content = re.sub(r'<!--\s*Floating Buttons?\s*-->.*?(?=\s*<!--|\s*<script|\s*</body>)', '', content, flags=re.DOTALL)
    
    # Remove existing chatbot
    content = re.sub(r'<!--\s*AI Chatbot.*?-->.*?(?=\s*<script|\s*</body>)', '', content, flags=re.DOTALL)

    # Insert full footer before </body> or before <script> tags
    # Find where script tags start
    script_pos = content.rfind('<script src=')
    if script_pos == -1:
        script_pos = content.rfind('</body>')
    
    if script_pos == -1:
        print('ERROR: no </body> in ' + name)
        continue

    # Keep existing scripts but add footer before them
    before_scripts = content[:script_pos].rstrip()
    after_scripts = content[script_pos:]

    # Build new content
    new_content = before_scripts + '\n\n' + FULL_FOOTER + '\n\n' + AFTER_FOOTER + '\n\n' + after_scripts

    # Remove any duplicate script imports that AFTER_FOOTER might create
    # Keep only unique script lines
    # Actually AFTER_FOOTER has chatbot/search overlay HTML + scripts
    # The HTML files already have their own script imports - we need to not duplicate
    # Let's just add the footer HTML and floating elements, but not re-add JS scripts
    
    # Simplified: just insert footer before existing scripts
    new_content = before_scripts + '\n\n' + FULL_FOOTER + '\n\n'
    
    # Add search overlay + floating buttons + chatbot (HTML only, no scripts)
    WIDGETS = """
    <!-- Fullscreen Search Overlay -->
    <div id="search-overlay" class="search-overlay">
        <div class="search-overlay-close" id="searchClose"><i class="fas fa-times"></i></div>
        <div class="search-overlay-content" style="width: 100%; max-width: 600px; padding: 20px;">
            <form action="contact.html" method="GET" class="w-100">
                <h3 class="text-white mb-4 text-center"><i class="fas fa-search me-2 text-gradient"></i>Search Destination Packages</h3>
                <div class="search-input-group">
                    <input type="text" name="destination" placeholder="Search Goa, Kashmir, Dubai..." required>
                    <button type="submit" class="btn-primary-glow"><i class="fas fa-arrow-right"></i></button>
                </div>
            </form>
        </div>
    </div>
    <!-- Floating Buttons -->
    <a href="https://wa.me/917015638389" target="_blank" class="floating-btn whatsapp-btn">
        <i class="fab fa-whatsapp"></i>
    </a>
    <button id="back-top-btn" class="floating-btn back-top-btn">
        <i class="fas fa-arrow-up"></i>
    </button>
    <!-- AI Chatbot Toggle -->
    <div id="chatbot-toggle-btn" class="chatbot-toggle-btn">
        <i class="fas fa-robot"></i>
    </div>
    <!-- AI Chatbot Widget -->
    <div id="chatbot-widget" class="chatbot-widget">
        <div class="chatbot-header">
            <span><i class="fas fa-robot me-2"></i> Roamerly AI</span>
            <i class="fas fa-times" id="chatbot-close" style="cursor:pointer;"></i>
        </div>
        <div class="chatbot-body">
            <div class="chat-msg bot">Hello! I am your Roamerly AI assistant. How can I help you plan your perfect trip today?</div>
        </div>
        <div class="chatbot-footer">
            <input type="text" class="chatbot-input" placeholder="Type a message...">
            <button class="chatbot-send"><i class="fas fa-paper-plane"></i></button>
        </div>
    </div>
"""
    new_content += WIDGETS + '\n' + after_scripts

    open(fpath, 'w', encoding='utf-8').write(new_content)
    print('UPDATED: ' + name)
    updated += 1

print('\nTotal updated: ' + str(updated) + ' pages')
