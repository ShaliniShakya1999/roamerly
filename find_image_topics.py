import os, re, glob

ROAMERLY = r'd:\project\peyug_project\roamerly'
dest_dir = os.path.join(ROAMERLY, 'assets', 'images', 'destinations')

# Find all HTML files
html_files = glob.glob(os.path.join(ROAMERLY, '*.html'))

img_to_topic = {}

# Regexes to capture images and their alt tags or adjacent heading text
# Standard image pattern: <img src="assets/images/destinations/..." alt="..."
img_pat = re.compile(r'<img[^>]+src=["\'](assets/images/destinations/[^"\']+)["\'][^>]*>')
alt_pat = re.compile(r'alt=["\']([^"\']+)["\']')

# Let's read files and extract mappings
for fpath in html_files:
    fname = os.path.basename(fpath)
    try:
        content = open(fpath, encoding='utf-8').read()
    except Exception as e:
        continue
    
    # Also find hero style background images: background-image: url('assets/images/destinations/...')
    hero_matches = re.findall(r'url\(["\']?(assets/images/destinations/[^"\'\)]+)["\']?\)', content)
    for h in hero_matches:
        img_name = os.path.basename(h)
        # Determine topic from filename
        dest = img_name.split('-')[0]
        topic = f"{dest.replace('_', ' ').title()} Hero Banner"
        img_to_topic[img_name] = (topic, fname)

    # Let's find images using regex
    for match in re.finditer(r'<img\s+[^>]*src=["\'](assets/images/destinations/[^"\']+)["\'][^>]*>', content):
        full_tag = match.group(0)
        img_path = match.group(1)
        img_name = os.path.basename(img_path)
        
        # Find alt inside tag
        alt_match = alt_pat.search(full_tag)
        alt = alt_match.group(1) if alt_match else ""
        
        if alt:
            img_to_topic[img_name] = (alt, fname)
        else:
            # If no alt, use the filename to guess topic
            dest = img_name.split('-')[0]
            img_to_topic[img_name] = (img_name, fname)

print(f"Total destination images mapped: {len(img_to_topic)}")
for img, (topic, page) in sorted(img_to_topic.items())[:20]:
    print(f"  {img} -> '{topic}' (in {page})")

# Save the map to a file so we can read it in the next step
import json
with open('image_topics.json', 'w', encoding='utf-8') as f:
    json.dump(img_to_topic, f, indent=4)
