import os
import re

destinations = [
    {"file": "usa.html", "name": "USA"},
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

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for dest in destinations:
    new_content = content
    # Replace title
    new_content = re.sub(r'<title>.*?</title>', f'<title>Flights to {dest["name"]} | Roamerly</title>', new_content)
    
    # Replace H1
    new_content = re.sub(
        r'<h1 class="gsap-zoom-in">Explore The World With <span class="text-gradient">Roamerly</span></h1>',
        f'<h1 class="gsap-zoom-in">Discover <span class="text-gradient">{dest["name"]}</span></h1>',
        new_content
    )
    
    # Replace Subtitle
    new_content = re.sub(
        r'<p class="gsap-fade-up">Find Flights, Hotels, Holidays & Adventures At The Best Prices</p>',
        f'<p class="gsap-fade-up">Find the Best Flight Deals and Holidays in {dest["name"]}</p>',
        new_content
    )
    
    with open(dest["file"], 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Generated 12 destination pages successfully.")
