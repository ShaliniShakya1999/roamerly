import os
import re

INDIA_CITIES = [
    {"file": "bangalore.html", "name": "Bangalore", "count": "5,372", "hero": "photo-1529258288937-d121e6b29c74"},
    {"file": "mumbai.html", "name": "Mumbai", "count": "4,177", "hero": "photo-1564507592330-4f8a4e02e0c5"},
    {"file": "hyderabad.html", "name": "Hyderabad", "count": "2,735", "hero": "photo-1587474260584-136574528ed5"},
    {"file": "new-delhi.html", "name": "New Delhi", "count": "12,786", "hero": "photo-1588668216169-48a4b0b0b0e"},
    {"file": "goa.html", "name": "Goa", "count": "9,254", "hero": "photo-1507525428034-b723cf961d3e"},
    {"file": "chennai.html", "name": "Chennai", "count": "2,832", "hero": "photo-1588668216169-48a4b0b0b0e"},
    {"file": "jaipur.html", "name": "Jaipur", "count": "3,082", "hero": "photo-1477587453913-6739373a0e0b"},
    {"file": "ooty.html", "name": "Ooty", "count": "1,427", "hero": "photo-1506905925346-21bda4d32df4"},
    {"file": "kochi.html", "name": "Kochi", "count": "2,165", "hero": "photo-1602216052126-53b0b0b0b0e"},
    {"file": "pune.html", "name": "Pune", "count": "2,494", "hero": "photo-1570168007204-d1bf43f0b0b0e"},
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


def build_destinations_dropdown():
    india_items = [
        '                                <li><a class="dropdown-item" href="india.html"><strong>India</strong> <small class="text-muted d-block">All domestic packages</small></a></li>',
    ]
    for c in INDIA_CITIES:
        india_items.append(
            f'                                <li><a class="dropdown-item" href="{c["file"]}"><strong>{c["name"]}</strong> <small class="text-muted d-block">{c["count"]} accommodations</small></a></li>'
        )

    intl_items = [
        f'                                <li><a class="dropdown-item" href="{d["file"]}">{d["name"]}</a></li>'
        for d in INTERNATIONAL
    ]

    return '\n'.join([
        '                    <!-- Destinations Dropdown -->',
        '                    <li class="nav-item dropdown">',
        '                        <a class="nav-link dropdown-toggle" href="#" role="button"',
        '                            data-bs-toggle="dropdown">Destinations</a>',
        '                        <ul class="dropdown-menu glass-card destinations-mega p-0">',
        '                            <li class="destinations-mega-wrap">',
        '                                <div class="row g-0 destinations-mega-row">',
        '                                    <div class="col-md-6 destinations-mega-col destinations-mega-india">',
        '                                        <h6 class="dropdown-header">India</h6>',
        '                                        <ul class="list-unstyled mb-0">',
        *india_items,
        '                                        </ul>',
        '                                    </div>',
        '                                    <div class="col-md-6 destinations-mega-col destinations-mega-intl">',
        '                                        <h6 class="dropdown-header">International</h6>',
        '                                        <ul class="list-unstyled mb-0">',
        *intl_items,
        '                                        </ul>',
        '                                    </div>',
        '                                </div>',
        '                            </li>',
        '                        </ul>',
        '                    </li>',
    ])


def build_domestic_dropdown():
    city_links = ''.join(
        f'                            <li><a class="dropdown-item" href="{c["file"]}">{c["name"]}</a></li>\n'
        for c in INDIA_CITIES
    )
    return f'''                    <!-- Domestic Tours Dropdown -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Domestic
                            Tours</a>
                        <ul class="dropdown-menu glass-card">
                            <li><a class="dropdown-item" href="india.html">All India Packages</a></li>
{city_links}                            <li><a class="dropdown-item" href="india.html">Manali Adventure</a></li>
                            <li><a class="dropdown-item" href="india.html">Kashmir Paradise</a></li>
                            <li><a class="dropdown-item" href="india.html">Kerala Backwaters</a></li>
                        </ul>
                    </li>'''


def build_international_dropdown():
    links = ''.join(
        f'                            <li><a class="dropdown-item" href="{d["file"]}">{d["name"]}</a></li>\n'
        for d in INTERNATIONAL
    )
    return f'''                    <!-- International Tours Dropdown -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button"
                            data-bs-toggle="dropdown">International Tours</a>
                        <ul class="dropdown-menu glass-card">
{links}                        </ul>
                    </li>'''


def update_nav_in_file(path, dest_html, domestic_html, intl_html):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'<!-- Destinations Dropdown -->.*?<!-- Domestic Tours Dropdown -->.*?<!-- International Tours Dropdown -->'
        r'.*?</ul>\s*</li>',
        dest_html + '\n\n' + domestic_html + '\n\n\n\n' + intl_html,
        content,
        count=1,
        flags=re.DOTALL,
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_city_pages(dest_html, domestic_html, intl_html):
    with open('india.html', 'r', encoding='utf-8') as f:
        template = f.read()

    template = re.sub(
        r'<!-- Destinations Dropdown -->.*?</li>\s*\n\s*<!-- Domestic Tours Dropdown -->.*?</li>\s*\n\s*<!-- International Tours Dropdown -->.*?</li>',
        dest_html + '\n\n' + domestic_html + '\n\n\n\n' + intl_html,
        template,
        count=1,
        flags=re.DOTALL,
    )

    for c in INDIA_CITIES:
        slug = c['name'].lower().replace(' ', '-')
        page = template
        page = re.sub(r'<title>.*?</title>', f'<title>{c["name"]} Hotels & Tour Packages | Roamerly</title>', page)
        page = page.replace(
            'Explore the best of India with Roamerly. Book domestic tour packages for Goa, Manali, Kashmir, Nainital, and Jaipur',
            f'Book hotels and tour packages in {c["name"]} with Roamerly. {c["count"]}+ accommodations',
        )
        page = page.replace('INSPIRING\n                INDIA', f'EXPLORE\n                {c["name"].upper()}')
        page = page.replace('Discover the Magic of India', f'Discover {c["name"]}')
        page = page.replace(
            'Explore curated domestic tour packages\n                tailored for unforgettable memories, from sun-kissed beaches to majestic snow peaks.',
            f'Find the best stays and curated holiday packages in {c["name"]}. {c["count"]} accommodations available.',
        )
        page = page.replace('<span class="section-tag">Explore India</span>', f'<span class="section-tag">Explore {c["name"]}</span>')
        page = page.replace('All India Holiday Packages', f'{c["name"]} Holiday Packages')
        page = page.replace('photo-1548013146-72479768bada', c['hero'])
        page = page.replace('india tour packages', f'{slug} tour packages')

        with open(c['file'], 'w', encoding='utf-8') as f:
            f.write(page)
        print(f'Generated {c["file"]}')


def main():
    dest_html = build_destinations_dropdown()
    domestic_html = build_domestic_dropdown()
    intl_html = build_international_dropdown()

    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for fname in html_files:
        if fname in [c['file'] for c in INDIA_CITIES]:
            continue
        update_nav_in_file(fname, dest_html, domestic_html, intl_html)
        print(f'Updated nav in {fname}')

    generate_city_pages(dest_html, domestic_html, intl_html)
    print('Done.')


if __name__ == '__main__':
    main()
