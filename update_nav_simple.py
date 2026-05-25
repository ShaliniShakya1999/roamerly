import os
import re

DOMESTIC_CITIES = [
    {"file": "bangalore.html", "name": "Bangalore"},
    {"file": "mumbai.html", "name": "Mumbai"},
    {"file": "new-delhi.html", "name": "New Delhi"},
    {"file": "goa.html", "name": "Goa"},
    {"file": "hyderabad.html", "name": "Hyderabad"},
    {"file": "chennai.html", "name": "Chennai"},
    {"file": "jaipur.html", "name": "Jaipur"},
    {"file": "kolkata.html", "name": "Kolkata"},
    {"file": "kochi.html", "name": "Kochi"},
    {"file": "pune.html", "name": "Pune"},
    {"file": "varanasi.html", "name": "Varanasi"},
    {"file": "pondicherry.html", "name": "Pondicherry"},
]

INTERNATIONAL = [
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
    {"file": "europe.html", "name": "Europe"},
]

NEW_CITIES = [
    {"file": "kolkata.html", "name": "Kolkata", "hero": "photo-1548013146-72479768bada"},
    {"file": "varanasi.html", "name": "Varanasi", "hero": "photo-1564507592330-4f8a4e02e0c5"},
    {"file": "pondicherry.html", "name": "Pondicherry", "hero": "photo-1507525428034-b723cf961d3e"},
]


def build_nav():
    intl_links = '\n'.join(
        f'                            <li><a class="dropdown-item" href="{d["file"]}">{d["name"]}</a></li>'
        for d in INTERNATIONAL
    )
    domestic_links = '\n'.join(
        f'                            <li><a class="dropdown-item" href="{c["file"]}">{c["name"]}</a></li>'
        for c in DOMESTIC_CITIES
    )
    return f'''                <ul class="navbar-nav mx-auto">
                    <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>

                    <!-- International Tours Dropdown -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button"
                            data-bs-toggle="dropdown">International Tours</a>
                        <ul class="dropdown-menu glass-card">
{intl_links}
                        </ul>
                    </li>

                    <!-- Domestic Tours Dropdown -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button"
                            data-bs-toggle="dropdown">Domestic Tours</a>
                        <ul class="dropdown-menu glass-card">
{domestic_links}
                        </ul>
                    </li>

                    <li class="nav-item"><a class="nav-link" href="contact.html">About Us</a></li>
                    <li class="nav-item"><a class="nav-link" href="contact.html">Contact</a></li>
                </ul>'''


def create_new_city_pages():
    with open('bangalore.html', 'r', encoding='utf-8') as f:
        template = f.read()

    for c in NEW_CITIES:
        page = template
        page = re.sub(r'<title>.*?</title>', f'<title>{c["name"]} Hotels & Tour Packages | Roamerly</title>', page)
        page = re.sub(
            r'content="Book hotels and tour packages in Bangalore with Roamerly\.[^"]*"',
            f'content="Book hotels and tour packages in {c["name"]} with Roamerly. Premium stays and curated holiday packages."',
            page,
        )
        page = page.replace('EXPLORE\n                BANGALORE', f'EXPLORE\n                {c["name"].upper()}')
        page = page.replace('Discover Bangalore', f'Discover {c["name"]}')
        page = page.replace(
            'Find the best stays and curated holiday packages in Bangalore. 5,372 accommodations available.',
            f'Find the best stays and curated holiday packages in {c["name"]}.',
        )
        page = page.replace('<span class="section-tag">Explore Bangalore</span>', f'<span class="section-tag">Explore {c["name"]}</span>')
        page = page.replace('Bangalore Holiday Packages', f'{c["name"]} Holiday Packages')
        page = page.replace('photo-1529258288937-d121e6b29c74', c['hero'])
        with open(c['file'], 'w', encoding='utf-8') as f:
            f.write(page)
        print(f'Created {c["file"]}')


def main():
    nav_html = build_nav()

    for fname in os.listdir('.'):
        if not fname.endswith('.html'):
            continue
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = re.sub(
            r'<ul class="navbar-nav mx-auto">.*?</ul>\s*\n\s*<div class="d-flex align-items-center',
            nav_html + '\n                <div class="d-flex align-items-center',
            content,
            count=1,
            flags=re.DOTALL,
        )

        if new_content != content:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated nav: {fname}')

    create_new_city_pages()
    print('Done — menu: Home | International Tours | Domestic Tours | About Us | Contact')


if __name__ == '__main__':
    main()
