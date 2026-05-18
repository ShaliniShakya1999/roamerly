import os
import re

destinations = [
    {"file": "canada.html", "name": "Canada"},
    {"file": "australia.html", "name": "Australia"},
    {"file": "new-zealand.html", "name": "New Zealand"},
    {"file": "middle-east.html", "name": "Middle East"},
    {"file": "africa.html", "name": "Africa"},
    {"file": "far-east.html", "name": "Far East"},
    {"file": "latin-america.html", "name": "Latin America"},
    {"file": "caribbean.html", "name": "Caribbean"},
    {"file": "asia.html", "name": "Asia"},
    {"file": "mexico.html", "name": "Mexico"},
    {"file": "europe.html", "name": "Europe"}
]

with open('usa.html', 'r', encoding='utf-8') as f:
    usa_content = f.read()

# Make the USA specific text generic for the template
template = usa_content

# Title and Headers
template = template.replace('Flights to USA | Roamerly', 'Flights to {DEST_NAME} | Roamerly')
template = template.replace('FLIGHTS TO <span class="text-gradient">USA</span>', 'FLIGHTS TO <span class="text-gradient">{DEST_NAME}</span>')
template = template.replace('Find the Best Flight Deals and Holidays in USA', 'Find the Best Flight Deals and Holidays in {DEST_NAME}')
template = template.replace('Call Now to save up to 70% on flights to USA', 'Call Now to save up to 70% on flights to {DEST_NAME}')
template = template.replace('flights to USA', 'flights to {DEST_NAME}')
template = template.replace('flight tickets to USA', 'flight tickets to {DEST_NAME}')
template = template.replace('holiday to the USA', 'holiday to {DEST_NAME}')
template = template.replace('USA flight deals', '{DEST_NAME} flight deals')
template = template.replace('US cities', '{DEST_NAME} cities')
template = template.replace('living in the US', 'living in {DEST_NAME}')

# Things to do Section
template = template.replace('Things to do in USA', 'Things to do in {DEST_NAME}')

# Replace specific cards with generic ones
template = re.sub(
    r'<div class="mb-3 text-primary fs-1"><i class="fas fa-tree"></i></div>\s*<h4 class="mb-3">Central Park New York</h4>\s*<p class="text-muted small">.*?</p>',
    r'<div class="mb-3 text-primary fs-1"><i class="fas fa-landmark"></i></div>\n                        <h4 class="mb-3">Historic Landmarks</h4>\n                        <p class="text-muted small">Explore iconic historical sites and monuments that tell the rich story and heritage of {DEST_NAME}. A must-visit for culture enthusiasts.</p>',
    template, flags=re.DOTALL
)

template = re.sub(
    r'<div class="mb-3 text-info fs-1"><i class="fas fa-monument"></i></div>\s*<h4 class="mb-3">National 9/11 Memorial</h4>\s*<p class="text-muted small">.*?</p>',
    r'<div class="mb-3 text-info fs-1"><i class="fas fa-mountain"></i></div>\n                        <h4 class="mb-3">Natural Wonders</h4>\n                        <p class="text-muted small">Discover breathtaking landscapes, national parks, and scenic beauty. {DEST_NAME} offers some of the most spectacular natural attractions.</p>',
    template, flags=re.DOTALL
)

template = re.sub(
    r'<div class="mb-3 text-warning fs-1"><i class="fas fa-magic"></i></div>\s*<h4 class="mb-3">Walt Disney World</h4>\s*<p class="text-muted small">.*?</p>',
    r'<div class="mb-3 text-warning fs-1"><i class="fas fa-utensils"></i></div>\n                        <h4 class="mb-3">Local Cuisine</h4>\n                        <p class="text-muted small">Indulge in authentic local flavors and world-class dining experiences. Taste the traditional dishes that make {DEST_NAME} unique.</p>',
    template, flags=re.DOTALL
)

template = re.sub(
    r'<div class="mb-3 text-success fs-1"><i class="fas fa-mountain"></i></div>\s*<h4 class="mb-3">Yellowstone National Park</h4>\s*<p class="text-muted small">.*?</p>',
    r'<div class="mb-3 text-success fs-1"><i class="fas fa-mask"></i></div>\n                        <h4 class="mb-3">Cultural Hotspots</h4>\n                        <p class="text-muted small">Immerse yourself in vibrant local culture, arts, and traditions. Experience the lively festivals and local markets of {DEST_NAME}.</p>',
    template, flags=re.DOTALL
)

template = re.sub(
    r'<div class="mb-3 text-danger fs-1"><i class="fas fa-bridge-water"></i></div>\s*<h4 class="mb-3">Golden Gate Bridge</h4>\s*<p class="text-muted small">.*?</p>',
    r'<div class="mb-3 text-danger fs-1"><i class="fas fa-city"></i></div>\n                        <h4 class="mb-3">City Adventures</h4>\n                        <p class="text-muted small">Experience the bustling nightlife, modern architecture, and endless entertainment options in the top metropolitan cities of {DEST_NAME}.</p>',
    template, flags=re.DOTALL
)

# CTA in cards
template = template.replace('Book your flights to the USA today', 'Book your flights to {DEST_NAME} today')

# Best Time & Cheap Flights Section
template = template.replace('Best Time to Visit USA', 'Best Time to Visit {DEST_NAME}')
template = template.replace('The United States of America is a great country with 50 states.', '{DEST_NAME} is an incredible destination with diverse regions to explore.')

for dest in destinations:
    file_content = template.replace('{DEST_NAME}', dest['name'])
    # Optional: Change hero image to something random to differentiate pages.
    # Unsplash random nature/city:
    file_content = file_content.replace('photo-1496442226666-8d4d0e62e6e9', 'photo-1476514525535-07fb3b4ae5f1') # Boat on lake
    file_content = file_content.replace('photo-1501594907352-04cda38ebc29', 'photo-1506929562872-bb421503ef21') # Beach
    
    with open(dest['file'], 'w', encoding='utf-8') as f:
        f.write(file_content)
    print(f"Generated {dest['file']}")

print("All destination pages generated successfully based on usa.html layout.")
