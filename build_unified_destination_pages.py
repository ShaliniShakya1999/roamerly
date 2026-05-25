"""
Rebuild menu-linked destination pages with unified layout, topic content & local images.
Run: python build_unified_destination_pages.py
"""
import os
import re
import urllib.request
from urllib.parse import quote
from update_nav_simple import build_nav, DOMESTIC_CITIES, INTERNATIONAL

IMG_DIR = "assets/images/destinations"
WHATSAPP = "917015638389"

DOMESTIC = [
    {"slug": "bangalore", "file": "bangalore.html", "name": "Bangalore",
     "hero": "photo-1529258288937-d121e6b29c74",
     "tagline": "Garden City vibes, tech parks, breweries & weekend hill escapes.",
     "intro": "Bangalore blends lush parks, vibrant cafes, and India's startup culture. Perfect for city breaks, food trails, and quick getaways to Nandi Hills.",
     "places": [
         ("Lalbagh Botanical Garden", "photo-1596176530528-1b6f4a8b0b0e", "Iconic 240-acre garden with glass house & flower shows."),
         ("Bangalore Palace", "photo-1587474260584-136574528ed5", "Tudor-style palace with royal architecture & audio tours."),
         ("Cubbon Park", "photo-1529258288937-d121e6b29c74", "Central green lung for morning walks and heritage buildings."),
         ("Nandi Hills", "photo-1506905925346-21bda4d32df4", "Sunrise viewpoint & paragliding just 60 km from the city."),
     ],
     "pkg1": ("City Lights & Culture", "3 Days / 2 Nights", "14999", "photo-1529258288937-d121e6b29c74",
              "Boutique stay, private city tour, brewery dinner & airport transfers.",
              ["3-Star Boutique Hotel", "Private AC City Tour", "Lalbagh & Palace Entry", "Daily Breakfast"]),
     "pkg2": ("Nandi Hills Escape", "2 Days / 1 Night", "8999", "photo-1506905925346-21bda4d32df4",
              "Sunrise trek, hill resort stay & private cab from Bangalore.",
              ["Hill Resort Stay", "Sunrise Viewpoint Visit", "Private Round-trip Cab", "Breakfast & Dinner"]),
    },
    {"slug": "mumbai", "file": "mumbai.html", "name": "Mumbai",
     "hero": "photo-1564507592330-4f8a4e02e0c5",
     "tagline": "Gateway of India, Marine Drive sunsets & Bollywood energy.",
     "intro": "Mumbai is India's financial capital with colonial heritage, street food, art districts, and iconic waterfronts.",
     "places": [
         ("Gateway of India", "photo-1570168007204-d1bf43f0b0b0e", "Historic arch overlooking the Arabian Sea."),
         ("Marine Drive", "photo-1564507592330-4f8a4e02e0c5", "Queen's Necklace — best at golden hour."),
         ("Elephanta Caves", "photo-1548013146-72479768bada", "UNESCO rock-cut caves via ferry ride."),
         ("Colaba & Fort", "photo-1512453979798-5ea266f8880c", "Cafes, galleries & heritage walking trails."),
     ],
     "pkg1": ("Mumbai Heritage Trail", "4 Days / 3 Nights", "18999", "photo-1564507592330-4f8a4e02e0c5",
              "Sea-facing hotel, guided heritage walk & Elephanta day trip.",
              ["4-Star Sea View Hotel", "Elephanta Ferry & Guide", "Colaba Food Walk", "Daily Breakfast"]),
     "pkg2": ("Bollywood & Beaches", "3 Days / 2 Nights", "16999", "photo-1570168007204-d1bf43f0b0b0e",
              "Film city tour, Juhu beach sunset & luxury transfers.",
              ["Film City Studio Tour", "Private SUV Transfers", "Juhu & Versova Visit", "2 Nights Premium Stay"]),
    },
    {"slug": "new-delhi", "file": "new-delhi.html", "name": "New Delhi",
     "hero": "photo-1588668216169-48a4b0b0b0e",
     "tagline": "Mughal monuments, bustling bazaars & capital-city grandeur.",
     "intro": "New Delhi offers India Gate, Red Fort, Humayun's Tomb, and world-class museums — ideal for history lovers.",
     "places": [
         ("India Gate", "photo-1588668216169-48a4b0b0b0e", "War memorial and evening picnic spot."),
         ("Red Fort", "photo-1548013146-72479768bada", "Mughal fort with light & sound show."),
         ("Humayun's Tomb", "photo-1587474260584-136574528ed5", "Stunning precursor to the Taj Mahal."),
         ("Chandni Chowk", "photo-1564507592330-4f8a4e02e0c5", "Street food, spices & Old Delhi rickshaw rides."),
     ],
     "pkg1": ("Capital Heritage Tour", "4 Days / 3 Nights", "17999", "photo-1588668216169-48a4b0b0b0e",
              "Monument passes, Old Delhi rickshaw & premium hotel in central Delhi.",
              ["Monument Entry Passes", "Old Delhi Rickshaw Tour", "Central Delhi Hotel", "Private AC Transport"]),
     "pkg2": ("Delhi Food & Culture", "3 Days / 2 Nights", "12999", "photo-1564507592330-4f8a4e02e0c5",
              "Guided food crawl, Akshardham visit & airport pickup.",
              ["Guided Food Trail", "Akshardham Entry", "Airport Transfers", "Daily Breakfast"]),
    },
    {"slug": "goa", "file": "goa.html", "name": "Goa",
     "hero": "photo-1507525428034-b723cf961d3e",
     "tagline": "Golden beaches, Portuguese churches & sunset shacks.",
     "intro": "Goa is India's beach paradise — north party vibes, south serene coves, seafood, and water sports year-round.",
     "places": [
         ("Baga & Calangute", "photo-1507525428034-b723cf961d3e", "Popular beaches with water sports & nightlife."),
         ("Old Goa Churches", "photo-1548013146-72479768bada", "UNESCO Basilica of Bom Jesus & Se Cathedral."),
         ("Dudhsagar Falls", "photo-1506905925346-21bda4d32df4", "Jeep safari to majestic monsoon waterfall."),
         ("Palolem Beach", "photo-1507525428034-b723cf961d3e", "Crescent bay in South Goa for relaxed stays."),
     ],
     "pkg1": ("Goa Beach Retreat", "4 Days / 3 Nights", "24999", "photo-1507525428034-b723cf961d3e",
              "Beach resort, private North-South tour & sunset cruise.",
              ["Beachfront Resort", "Private SUV Sightseeing", "Sunset Cruise", "Breakfast & Dinner"]),
     "pkg2": ("South Goa Serenity", "5 Days / 4 Nights", "21999", "photo-1507525428034-b723cf961d3e",
              "Boutique villa, spice plantation & dolphin spotting trip.",
              ["Boutique Villa Stay", "Spice Farm Tour", "Dolphin Trip", "Airport Transfers"]),
    },
    {"slug": "hyderabad", "file": "hyderabad.html", "name": "Hyderabad",
     "hero": "photo-1587474260584-136574528ed5",
     "tagline": "Charminar, biryani capital & pearl bazaars.",
     "intro": "Hyderabad mixes Nizam heritage, IT hubs, and legendary cuisine — perfect for long weekends.",
     "places": [
         ("Charminar", "photo-1587474260584-136574528ed5", "Iconic mosque monument in Old City."),
         ("Golconda Fort", "photo-1548013146-72479768bada", "Acoustic fort with evening sound & light."),
         ("Ramoji Film City", "photo-1512453979798-5ea266f8880c", "World's largest film studio complex."),
         ("Hussain Sagar", "photo-1564507592330-4f8a4e02e0c5", "Lake with Buddha statue & boat rides."),
     ],
     "pkg1": ("Hyderabad Heritage", "3 Days / 2 Nights", "13999", "photo-1587474260584-136574528ed5",
              "Old City tour, biryani dinner & 4-star stay near Hitec City.",
              ["Charminar & Golconda Tour", "Biryani Experience Dinner", "4-Star Hotel", "Private Transport"]),
     "pkg2": ("Ramoji & City Fun", "2 Days / 1 Night", "9999", "photo-1512453979798-5ea266f8880c",
              "Full-day Ramoji pass with family-friendly activities.",
              ["Ramoji Film City Pass", "Meal Coupon", "Hotel Stay", "Round-trip Transfers"]),
    },
    {"slug": "chennai", "file": "chennai.html", "name": "Chennai",
     "hero": "photo-1588668216169-48a4b0b0b0e",
     "tagline": "Marina Beach, temples, filter coffee & Carnatic culture.",
     "intro": "Chennai is the gateway to Tamil culture — classical arts, coastal temples, and Mahabalipuram day trips.",
     "places": [
         ("Marina Beach", "photo-1588668216169-48a4b0b0b0e", "Long urban beach promenade."),
         ("Kapaleeshwarar Temple", "photo-1548013146-72479768bada", "Dravidian architecture in Mylapore."),
         ("Mahabalipuram", "photo-1507525428034-b723cf961d3e", "Shore temple & stone carvings by the sea."),
         ("Fort St. George", "photo-1587474260584-136574528ed5", "British-era museum & colonial history."),
     ],
     "pkg1": ("Chennai Coastal Break", "3 Days / 2 Nights", "12999", "photo-1588668216169-48a4b0b0b0e",
              "City temples, Marina sunset & Mahabalipuram excursion.",
              ["Mahabalipuram Day Trip", "Temple & Museum Tour", "3-Star Hotel", "Daily Breakfast"]),
     "pkg2": ("Temple Trail", "4 Days / 3 Nights", "15999", "photo-1548013146-72479768bada",
              "Kanchipuram silk weaving & temple circuit with guide.",
              ["Kanchipuram Visit", "Expert Local Guide", "AC Transport", "3 Nights Stay"]),
    },
    {"slug": "jaipur", "file": "jaipur.html", "name": "Jaipur",
     "hero": "photo-1477587453913-6739373a0e0b",
     "tagline": "Pink City palaces, forts & royal Rajasthani culture.",
     "intro": "Jaipur delivers amber forts, bustling bazaars, heritage hotels, and unforgettable desert sunsets.",
     "places": [
         ("Amber Fort", "photo-1477587453913-6739373a0e0b", "Hilltop fort with elephant rides & light show."),
         ("Hawa Mahal", "photo-1587474260584-136574528ed5", "Palace of Winds facade photography spot."),
         ("City Palace", "photo-1548013146-72479768bada", "Royal residence & museum in old Jaipur."),
         ("Jantar Mantar", "photo-1564507592330-4f8a4e02e0c5", "UNESCO astronomical observatory."),
     ],
     "pkg1": ("Royal Jaipur Experience", "4 Days / 3 Nights", "22999", "photo-1477587453913-6739373a0e0b",
              "Heritage haveli, fort tours & traditional Rajasthani dinner.",
              ["Heritage Haveli Stay", "Amber & Nahargarh Tour", "Cultural Dinner Show", "Private Chauffeur"]),
     "pkg2": ("Pink City Weekend", "3 Days / 2 Nights", "16999", "photo-1587474260584-136574528ed5",
              "Bazaar shopping, palace entries & rooftop sunset.",
              ["City Palace Entry", "Guided Bazaar Walk", "Rooftop Dinner", "AC SUV"]),
    },
    {"slug": "kolkata", "file": "kolkata.html", "name": "Kolkata",
     "hero": "photo-1548013146-72479768bada",
     "tagline": "Colonial charm, Howrah Bridge & literary cafés.",
     "intro": "Kolkata is cultural Bengal — trams, Durga Puja art, river ghats, and legendary sweets.",
     "places": [
         ("Victoria Memorial", "photo-1548013146-72479768bada", "Marble museum set in lush gardens."),
         ("Howrah Bridge", "photo-1564507592330-4f8a4e02e0c5", "Iconic cantilever bridge over Hooghly."),
         ("Kumartuli", "photo-1587474260584-136574528ed5", "Artisan quarter crafting Durga idols."),
         ("Park Street", "photo-1512453979798-5ea266f8880c", "Restaurants, live music & nightlife."),
     ],
     "pkg1": ("Kolkata Culture Tour", "3 Days / 2 Nights", "11999", "photo-1548013146-72479768bada",
              "Colonial walk, river cruise & Bengali cuisine experience.",
              ["Hooghly River Cruise", "Victoria Memorial Entry", "Food Trail", "Central Hotel"]),
     "pkg2": ("Bengal Heritage", "4 Days / 3 Nights", "14999", "photo-1564507592330-4f8a4e02e0c5",
              "Sundarbans day option & artisan village visit.",
              ["Kumartuli Workshop Visit", "Private Guide", "AC Transport", "3 Nights Stay"]),
    },
    {"slug": "kochi", "file": "kochi.html", "name": "Kochi",
     "hero": "photo-1602216052126-53b0b0b0b0e",
     "tagline": "Backwaters, Chinese fishing nets & spice trade history.",
     "intro": "Kochi is Kerala's coastal gem — houseboats, Fort Kochi street art, and Ayurveda retreats.",
     "places": [
         ("Fort Kochi", "photo-1602216052126-53b0b0b0b0e", "Colonial streets & seaside cafes."),
         ("Chinese Fishing Nets", "photo-1507525428034-b723cf961d3e", "Photogenic nets at sunset."),
         ("Alleppey Backwaters", "photo-1507525428034-b723cf961d3e", "Houseboat cruise through canals."),
         ("Munnar Hills", "photo-1506905925346-21bda4d32df4", "Tea plantations & misty viewpoints."),
     ],
     "pkg1": ("Kerala Backwaters", "4 Days / 3 Nights", "24999", "photo-1507525428034-b723cf961d3e",
              "Houseboat night, Fort Kochi tour & traditional meals.",
              ["Premium Houseboat", "Fort Kochi Guide Tour", "All Meals on Boat", "Airport Pickup"]),
     "pkg2": ("Kochi & Munnar", "5 Days / 4 Nights", "27999", "photo-1506905925346-21bda4d32df4",
              "Tea estate stay, Eravikulam park & spice garden.",
              ["Munnar Resort", "Tea Factory Visit", "Private Cab", "Daily Breakfast"]),
    },
    {"slug": "pune", "file": "pune.html", "name": "Pune",
     "hero": "photo-1570168007204-d1bf43f0b0b0e",
     "tagline": "Oxford of the East, forts & monsoon hill stations.",
     "intro": "Pune offers Maratha history, pleasant weather, and quick escapes to Lonavala & Lavasa.",
     "places": [
         ("Shaniwar Wada", "photo-1570168007204-d1bf43f0b0b0e", "Historic Peshwa palace fortification."),
         ("Aga Khan Palace", "photo-1548013146-72479768bada", "Gandhi national memorial site."),
         ("Lonavala", "photo-1506905925346-21bda4d32df4", "Hill station with viewpoints & chikki."),
         ("Sinhagad Fort", "photo-1506905925346-21bda4d32df4", "Trek-friendly fort with valley views."),
     ],
     "pkg1": ("Pune City & Hills", "3 Days / 2 Nights", "11999", "photo-1570168007204-d1bf43f0b0b0e",
              "City heritage, Lonavala day trip & boutique stay.",
              ["Lonavala Day Excursion", "Heritage City Tour", "Boutique Hotel", "Private Cab"]),
     "pkg2": ("Sinhagad Adventure", "2 Days / 1 Night", "7999", "photo-1506905925346-21bda4d32df4",
              "Guided fort trek with local lunch on plateau.",
              ["Guided Trek", "Local Lunch", "Transport", "1 Night Stay"]),
    },
    {"slug": "varanasi", "file": "varanasi.html", "name": "Varanasi",
     "hero": "photo-1564507592330-4f8a4e02e0c5",
     "tagline": "Ganges ghats, evening aarti & spiritual India.",
     "intro": "Varanasi is one of the world's oldest living cities — dawn boat rides, silk weaving, and temple lanes.",
     "places": [
         ("Dashashwamedh Ghat", "photo-1564507592330-4f8a4e02e0c5", "Famous Ganga Aarti every evening."),
         ("Kashi Vishwanath", "photo-1548013146-72479768bada", "Sacred Shiva temple in old city."),
         ("Sarnath", "photo-1587474260584-136574528ed5", "Buddha's first sermon archaeological site."),
         ("Banarasi Silk Lanes", "photo-1587474260584-136574528ed5", "Handloom saree workshops."),
     ],
     "pkg1": ("Spiritual Varanasi", "3 Days / 2 Nights", "10999", "photo-1564507592330-4f8a4e02e0c5",
              "Sunrise boat, Ganga Aarti & guided old city walk.",
              ["Sunrise Boat Ride", "Ganga Aarti Seats", "Old City Guide", "Heritage Guest House"]),
     "pkg2": ("Varanasi & Sarnath", "4 Days / 3 Nights", "13999", "photo-1548013146-72479768bada",
              "Temple circuit, Sarnath museum & silk weaving demo.",
              ["Sarnath Excursion", "Silk Weaving Demo", "AC Transport", "3 Nights Stay"]),
    },
    {"slug": "pondicherry", "file": "pondicherry.html", "name": "Pondicherry",
     "hero": "photo-1507525428034-b723cf961d3e",
     "tagline": "French Quarter, seaside promenade & Auroville.",
     "intro": "Pondicherry (Puducherry) blends colonial boulevards, beach cafés, and the peaceful Auroville community.",
     "places": [
         ("French Quarter", "photo-1507525428034-b723cf961d3e", "Yellow villas, cafes & boutique stays."),
         ("Promenade Beach", "photo-1507525428034-b723cf961d3e", "Seaside walk with Gandhi memorial."),
         ("Auroville", "photo-1506905925346-21bda4d32df4", "Matrimandir & sustainable community tours."),
         ("Paradise Beach", "photo-1507525428034-b723cf961d3e", "Boat access to quiet sandy beach."),
     ],
     "pkg1": ("French Coast Getaway", "3 Days / 2 Nights", "14999", "photo-1507525428034-b723cf961d3e",
              "Colonial stay, cycling tour & beach sunset dinner.",
              ["French Quarter Hotel", "Bicycle Heritage Tour", "Beach Dinner", "Private Transfers"]),
     "pkg2": ("Auroville Wellness", "4 Days / 3 Nights", "18999", "photo-1506905925346-21bda4d32df4",
              "Matrimandir visit, yoga session & organic cafe trail.",
              ["Auroville Guided Tour", "Yoga Session", "Eco Lodge Stay", "Breakfast Included"]),
    },
]

INTERNATIONAL_DATA = [
    {"slug": "usa", "file": "usa.html", "name": "USA",
     "hero": "photo-1496442226666-8d4d0e62e6e9",
     "tagline": "Skyscrapers, national parks & coast-to-coast road trips.",
     "intro": "From New York and Las Vegas to Yellowstone and California beaches — the USA offers endless holiday styles.",
     "places": [("New York City", "photo-1496442226666-8d4d0e62e6e9", "Times Square, Central Park & Broadway."),
                ("Grand Canyon", "photo-1506905925346-21bda4d32df4", "Breathtaking desert viewpoints."),
                ("San Francisco", "photo-1501594907352-04cda38ebc29", "Golden Gate Bridge & cable cars."),
                ("Orlando", "photo-1512453979798-5ea266f8880c", "Theme parks & family fun.")],
     "pkg1": ("East Coast Highlights", "8 Days / 7 Nights", "$2,499", "photo-1496442226666-8d4d0e62e6e9",
              "NYC, Washington DC & Philadelphia with guided tours.", ["4-Star Hotels", "Intercity Flights", "Guided Tours", "Breakfast Daily"]),
     "pkg2": ("West Coast Adventure", "10 Days / 9 Nights", "$2,899", "photo-1501594907352-04cda38ebc29",
              "LA, Vegas & San Francisco road trip.", ["SUV Road Trip", "National Park Entry", "Hotels", "GPS & Maps"]),
    },
    {"slug": "canada", "file": "canada.html", "name": "Canada",
     "hero": "photo-1503614472-8c93d83e29b4",
     "tagline": "Rockies, lakes, wildlife & friendly cities.",
     "intro": "Canada delivers Banff's peaks, Niagara Falls, multicultural Toronto, and aurora viewing in the north.",
     "places": [("Banff National Park", "photo-1506905925346-21bda4d32df4", "Turquoise lakes & mountain hikes."),
                ("Niagara Falls", "photo-1476514525535-07fb3b4ae5f1", "Iconic waterfall boat experience."),
                ("Toronto", "photo-1512453979798-5ea266f8880c", "CN Tower & waterfront districts."),
                ("Vancouver", "photo-1501594907352-04cda38ebc29", "Ocean, mountains & Stanley Park.")],
     "pkg1": ("Canadian Rockies", "7 Days / 6 Nights", "$2,199", "photo-1506905925346-21bda4d32df4",
              "Banff, Lake Louise & glacier tours.", ["Mountain Lodges", "Park Passes", "Private Guide", "Breakfast"]),
     "pkg2": ("Toronto & Niagara", "5 Days / 4 Nights", "$1,599", "photo-1476514525535-07fb3b4ae5f1",
              "City stay plus falls day trip.", ["4-Star Toronto Hotel", "Niagara Tour", "Transfers", "Breakfast"]),
    },
    {"slug": "australia", "file": "australia.html", "name": "Australia",
     "hero": "photo-1523482585902-397e813c5a79",
     "tagline": "Reefs, outback, koalas & surf beaches.",
     "intro": "Australia spans Great Barrier Reef diving, Sydney Opera House, Melbourne laneways, and Uluru sunsets.",
     "places": [("Sydney", "photo-1523482585902-397e813c5a79", "Opera House & Harbour Bridge."),
                ("Great Barrier Reef", "photo-1507525428034-b723cf961d3e", "Snorkel world-class coral reefs."),
                ("Melbourne", "photo-1512453979798-5ea266f8880c", "Coffee culture & Great Ocean Road."),
                ("Uluru", "photo-1506905925346-21bda4d32df4", "Sacred red rock at sunset.")],
     "pkg1": ("Sydney & Reef", "9 Days / 8 Nights", "$2,799", "photo-1523482585902-397e813c5a79",
              "City icons plus Cairns reef experience.", ["Sydney Hotel", "Reef Day Cruise", "Domestic Flight", "Breakfast"]),
     "pkg2": ("Outback & Coast", "12 Days / 11 Nights", "$3,499", "photo-1506905925346-21bda4d32df4",
              "Uluru, Adelaide & coastal drive.", ["Outback Lodge", "Guided Tours", "4WD Experience", "Most Meals"]),
    },
    {"slug": "new-zealand", "file": "new-zealand.html", "name": "New Zealand",
     "hero": "photo-1469854523086-cc02eed5c880",
     "tagline": "Middle-earth landscapes, fjords & adventure sports.",
     "intro": "New Zealand is paradise for hikers, LOTR fans, and thrill-seekers — Queenstown, Milford Sound, Auckland.",
     "places": [("Queenstown", "photo-1469854523086-cc02eed5c880", "Bungee, skiing & lake cruises."),
                ("Milford Sound", "photo-1506905925346-21bda4d32df4", "Fjord cruise through rainforests."),
                ("Auckland", "photo-1512453979798-5ea266f8880c", "Harbour city & nearby islands."),
                ("Rotorua", "photo-1506905925346-21bda4d32df4", "Geothermal pools & Maori culture.")],
     "pkg1": ("South Island Explorer", "10 Days / 9 Nights", "$2,999", "photo-1469854523086-cc02eed5c880",
              "Queenstown, glaciers & Milford Sound.", ["Scenic Drives", "Cruise Tickets", "Hotels", "Breakfast"]),
     "pkg2": ("North Island Culture", "7 Days / 6 Nights", "$2,199", "photo-1506905925346-21bda4d32df4",
              "Auckland, Rotorua geysers & Hobbiton.", ["Hobbiton Tour", "Maori Experience", "Hotels", "Transfers"]),
    },
    {"slug": "middle-east", "file": "middle-east.html", "name": "Middle East",
     "hero": "photo-1512453979798-5ea266f8880c",
     "tagline": "Dubai luxury, desert safaris & Arabian heritage.",
     "intro": "The Middle East offers ultramodern skylines, gold souks, desert camps, and world-class shopping.",
     "places": [("Dubai", "photo-1512453979798-5ea266f8880c", "Burj Khalifa & desert safari."),
                ("Abu Dhabi", "photo-1548013146-72479768bada", "Sheikh Zayed Grand Mosque."),
                ("Doha", "photo-1512453979798-5ea266f8880c", "Museum of Islamic Art & corniche."),
                ("Petra, Jordan", "photo-1548013146-72479768bada", "Rose-red ancient city.")],
     "pkg1": ("Dubai Luxury Escape", "5 Days / 4 Nights", "$1,899", "photo-1512453979798-5ea266f8880c",
              "5-star hotel, desert safari & marina cruise.", ["5-Star Hotel", "Desert Safari BBQ", "Burj Khalifa Ticket", "Transfers"]),
     "pkg2": ("UAE Twin City", "6 Days / 5 Nights", "$2,199", "photo-1548013146-72479768bada",
              "Dubai + Abu Dhabi highlights.", ["Twin City Tours", "Mosque Visit", "Hotels", "Private Cab"]),
    },
    {"slug": "africa", "file": "africa.html", "name": "Africa",
     "hero": "photo-1516026672322-bc52d61a55d5",
     "tagline": "Safari wildlife, Table Mountain & ancient wonders.",
     "intro": "Africa delivers Big Five safaris, Cape Town vineyards, pyramids of Egypt, and Serengeti migrations.",
     "places": [("Serengeti Safari", "photo-1516026672322-bc52d61a55d5", "Witness the great migration."),
                ("Cape Town", "photo-1506905925346-21bda4d32df4", "Table Mountain & Cape of Good Hope."),
                ("Pyramids of Giza", "photo-1548013146-72479768bada", "Ancient wonders near Cairo."),
                ("Victoria Falls", "photo-1476514525535-07fb3b4ae5f1", "Thundering waterfall adventure.")],
     "pkg1": ("Kenya Safari Classic", "7 Days / 6 Nights", "$2,499", "photo-1516026672322-bc52d61a55d5",
              "Game drives, lodge stay & Masai village.", ["Safari Lodge", "Daily Game Drives", "Park Fees", "All Meals"]),
     "pkg2": ("Cape Town & Winelands", "6 Days / 5 Nights", "$1,999", "photo-1506905925346-21bda4d32df4",
              "City tour, peninsula & Stellenbosch wine.", ["4-Star Hotel", "Wine Tasting", "Cape Point Tour", "Breakfast"]),
    },
    {"slug": "far-east", "file": "far-east.html", "name": "Far East",
     "hero": "photo-1540959733332-eab4deabeeaf",
     "tagline": "Tokyo neon, Bali temples & Southeast Asian beaches.",
     "intro": "Far East Asia combines futuristic cities, tropical islands, street food, and tranquil temples.",
     "places": [("Tokyo", "photo-1540959733332-eab4deabeeaf", "Shibuya, temples & sushi alleys."),
                ("Bali", "photo-1507525428034-b723cf961d3e", "Rice terraces & beach clubs."),
                ("Singapore", "photo-1512453979798-5ea266f8880c", "Gardens by the Bay & Marina Bay."),
                ("Bangkok", "photo-1564507592330-4f8a4e02e0c5", "Grand Palace & floating markets.")],
     "pkg1": ("Japan Highlights", "8 Days / 7 Nights", "$2,899", "photo-1540959733332-eab4deabeeaf",
              "Tokyo, Kyoto bullet train & cultural stays.", ["Rail Pass", "Ryokan Night", "Guided Tours", "Breakfast"]),
     "pkg2": ("Bali Wellness Retreat", "6 Days / 5 Nights", "$1,499", "photo-1507525428034-b723cf961d3e",
              "Villa, spa rituals & Ubud excursions.", ["Private Villa", "Spa Sessions", "Ubud Tour", "Airport Transfer"]),
    },
    {"slug": "latin-america", "file": "latin-america.html", "name": "Latin America",
     "hero": "photo-1483729558449-99ef09a8c325",
     "tagline": "Machu Picchu, Amazon rainforest & carnival cities.",
     "intro": "Latin America bursts with rhythm — Rio's beaches, Patagonia treks, Mayan ruins, and coffee highlands.",
     "places": [("Machu Picchu", "photo-1483729558449-99ef09a8c325", "Inca citadel in the Andes."),
                ("Rio de Janeiro", "photo-1507525428034-b723cf961d3e", "Christ the Redeemer & Copacabana."),
                ("Amazon Rainforest", "photo-1506905925346-21bda4d32df4", "Jungle lodges & river cruises."),
                ("Buenos Aires", "photo-1512453979798-5ea266f8880c", "Tango, steak & European boulevards.")],
     "pkg1": ("Peru Explorer", "8 Days / 7 Nights", "$2,399", "photo-1483729558449-99ef09a8c325",
              "Cusco, Sacred Valley & Machu Picchu train.", ["Train Tickets", "Expert Guide", "Boutique Hotels", "Breakfast"]),
     "pkg2": ("Brazil Coast & Culture", "9 Days / 8 Nights", "$2,599", "photo-1507525428034-b723cf961d3e",
              "Rio, Iguaçu Falls & Salvador heritage.", ["Domestic Flights", "Falls Tour", "Hotels", "Some Meals"]),
    },
    {"slug": "caribbean", "file": "caribbean.html", "name": "Caribbean",
     "hero": "photo-1544551763-46efeeeb4f72",
     "tagline": "Turquoise waters, reggae vibes & island hopping.",
     "intro": "The Caribbean is all-inclusive resorts, snorkeling reefs, rum distilleries, and laid-back island life.",
     "places": [("Bahamas", "photo-1544551763-46efeeeb4f72", "Crystal-clear cays & swimming pigs."),
                ("Jamaica", "photo-1507525428034-b723cf961d3e", "Dunn's River Falls & reggae culture."),
                ("Barbados", "photo-1507525428034-b723cf961d3e", "Surf beaches & rum heritage."),
                ("St. Lucia", "photo-1506905925346-21bda4d32df4", "Pitons peaks & rainforest spas.")],
     "pkg1": ("Bahamas Island Hop", "6 Days / 5 Nights", "$2,199", "photo-1544551763-46efeeeb4f72",
              "Resort stay, snorkel trip & catamaran cruise.", ["Beach Resort", "Snorkel Tour", "Catamaran", "Meals Plan"]),
     "pkg2": ("Jamaica All-Inclusive", "7 Days / 6 Nights", "$1,899", "photo-1507525428034-b723cf961d3e",
              "Waterfall climb, beach club & jerk cuisine.", ["All-Inclusive Resort", "Falls Excursion", "Transfers", "Unlimited Meals"]),
    },
    {"slug": "asia", "file": "asia.html", "name": "Asia",
     "hero": "photo-1508009603885-50cf7c579365",
     "tagline": "Thailand beaches, Vietnam streets & Himalayan peaks.",
     "intro": "Asia packs ancient temples, street markets, tropical islands, and snow peaks into one diverse continent.",
     "places": [("Thailand", "photo-1508009603885-50cf7c579365", "Bangkok temples & Phuket beaches."),
                ("Vietnam", "photo-1507525428034-b723cf961d3e", "Ha Long Bay cruises & Hoi An lanterns."),
                ("Sri Lanka", "photo-1506905925346-21bda4d32df4", "Tea hills & wildlife safaris."),
                ("Nepal", "photo-1506905925346-21bda4d32df4", "Kathmandu & Everest viewpoints.")],
     "pkg1": ("Thailand Discovery", "7 Days / 6 Nights", "$1,299", "photo-1508009603885-50cf7c579365",
              "Bangkok, Chiang Mai & island extension.", ["Domestic Flights", "Temple Tours", "Hotels", "Breakfast"]),
     "pkg2": ("Vietnam Coastal", "8 Days / 7 Nights", "$1,499", "photo-1507525428034-b723cf961d3e",
              "Ha Long cruise, Hanoi & Hoi An.", ["Overnight Cruise", "Old Quarter Tour", "Hotels", "Some Meals"]),
    },
    {"slug": "mexico", "file": "mexico.html", "name": "Mexico",
     "hero": "photo-1518638150340-f706d460de8a",
     "tagline": "Mayan ruins, cenotes, tacos & Pacific coast.",
     "intro": "Mexico blends Cancún beaches, Mexico City's museums, Oaxaca cuisine, and Chichen Itza history.",
     "places": [("Cancún & Riviera Maya", "photo-1518638150340-f706d460de8a", "Resorts & Caribbean snorkel."),
                ("Chichen Itza", "photo-1548013146-72479768bada", "Wonder of the World pyramid."),
                ("Mexico City", "photo-1512453979798-5ea266f8880c", "Frida Kahlo museum & Zócalo."),
                ("Oaxaca", "photo-1564507592330-4f8a4e02e0c5", "Mezcal, mole & indigenous crafts.")],
     "pkg1": ("Riviera Maya Beach", "6 Days / 5 Nights", "$1,699", "photo-1518638150340-f706d460de8a",
              "All-inclusive beach & cenote swim.", ["Beach Resort", "Cenote Tour", "Transfers", "Meal Plan"]),
     "pkg2": ("Mexico Heritage", "8 Days / 7 Nights", "$1,999", "photo-1548013146-72479768bada",
              "CDMX, Teotihuacán & Chichen Itza.", ["Guided Archaeology Tours", "Hotels", "Entrance Fees", "Breakfast"]),
    },
    {"slug": "europe", "file": "europe.html", "name": "Europe",
     "hero": "photo-1467269206134-efa93da8b7de",
     "tagline": "Paris romance, Swiss Alps & Mediterranean coast.",
     "intro": "Europe offers art museums, alpine trains, Greek islands, and Christmas markets across many cultures.",
     "places": [("Paris", "photo-1467269206134-efa93da8b7de", "Eiffel Tower & Louvre masterpieces."),
                ("Switzerland", "photo-1506905925346-21bda4d32df4", "Alps, lakes & scenic rail journeys."),
                ("Italy", "photo-1548013146-72479768bada", "Rome, Florence & Venice canals."),
                ("Greece", "photo-1507525428034-b723cf961d3e", "Santorini sunsets & Acropolis.")],
     "pkg1": ("Paris & Swiss Alps", "9 Days / 8 Nights", "$2,799", "photo-1467269206134-efa93da8b7de",
              "City tour, Eiffel access & Jungfrau excursion.", ["Rail Pass", "4-Star Hotels", "Guided Tours", "Breakfast"]),
     "pkg2": ("Italy Classic", "10 Days / 9 Nights", "$2,999", "photo-1548013146-72479768bada",
              "Rome, Florence, Venice with expert guides.", ["High-Speed Trains", "Museum Entries", "Hotels", "Breakfast"]),
    },
]


def unsplash_url(photo_id, w=1200):
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={w}&q=85"


def download_image(photo_id, filename):
    os.makedirs(IMG_DIR, exist_ok=True)
    path = os.path.join(IMG_DIR, filename)
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        return path.replace("\\", "/")
    url = unsplash_url(photo_id, 1400)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Roamerly/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(path, "wb") as f:
                f.write(resp.read())
        print(f"  Downloaded {path}")
        return path.replace("\\", "/")
    except Exception as e:
        print(f"  Skip download {filename}: {e}")
        return unsplash_url(photo_id)


def img_tag(local_or_url, alt, cls="w-100 h-100 object-fit-cover"):
    return f'<img src="{local_or_url}" alt="{alt}" class="{cls}" loading="lazy">'


def package_card(pkg, city_name, slug, pkg_idx):
    title, days, price, photo, desc, includes = pkg
    img = download_image(photo, f"{slug}-pkg{pkg_idx}.jpg")
    inc_html = "".join(f'<div class="col-sm-6 small text-muted"><i class="fas fa-check text-success me-2"></i>{i}</div>' for i in includes)
    return f'''
                <div class="col-lg-6 gsap-stagger-item">
                    <div class="glass-panel glass-panel-hover package-card overflow-hidden h-100 d-flex flex-column shadow-sm">
                        <div class="package-card-img-wrap position-relative">
                            {img_tag(img, title)}
                            <span class="package-badge">{days}</span>
                        </div>
                        <div class="p-5 d-flex flex-column flex-grow-1">
                            <h3 class="fw-bold mb-3 text-dark">{title}</h3>
                            <p class="text-muted mb-4">{desc}</p>
                            <h5 class="fw-semibold mb-3 text-primary-blue">What&apos;s Included:</h5>
                            <div class="row g-2 mb-4">{inc_html}</div>
                            <div class="d-flex justify-content-between align-items-center mt-auto pt-4 border-top">
                                <div>
                                    <span class="text-muted d-block small">Starting from</span>
                                    <span class="fs-3 fw-extrabold text-dark">{price}</span> <small class="text-muted">/ person</small>
                                </div>
                                <a href="https://wa.me/{WHATSAPP}?text={quote('I want to book ' + title + ' in ' + city_name)}"
                                    target="_blank" class="btn-primary-glow px-4 py-3"><i class="fab fa-whatsapp me-2"></i> Book Now</a>
                            </div>
                        </div>
                    </div>
                </div>'''


def place_card(name, photo, desc, slug, idx):
    img = download_image(photo, f"{slug}-place-{idx}.jpg")
    return f'''
                <div class="col-lg-3 col-md-6 gsap-stagger-item">
                    <div class="glass-panel place-card overflow-hidden h-100">
                        <div class="place-card-img">{img_tag(img, name)}</div>
                        <div class="p-4">
                            <h5 class="fw-bold mb-2">{name}</h5>
                            <p class="text-muted small mb-0">{desc}</p>
                        </div>
                    </div>
                </div>'''


def render_page(d, is_domestic=True):
    slug = d["slug"]
    name = d["name"]
    hero_local = download_image(d["hero"], f"{slug}-hero.jpg")
    places_html = "".join(place_card(p[0], p[1], p[2], slug, i) for i, p in enumerate(d["places"]))
    pkg_html = package_card(d["pkg1"], name, slug, 1) + package_card(d["pkg2"], name, slug, 2)
    nav = build_nav()

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} Tour Packages | Roamerly</title>
    <meta name="description" content="Book {name} holiday packages with Roamerly. {d["tagline"]}">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.css" />
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="mesh-bg"><div class="mesh-blob blue"></div><div class="mesh-blob purple"></div><div class="mesh-blob cyan"></div></div>
    <div id="preloader"><i class="fas fa-plane loader-plane"></i></div>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="index.html"><img src="assets/images/logo.png" alt="Roamerly" style="height: 100px; margin-top: -15px; margin-bottom: -15px;"></a>
            <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <i class="fas fa-bars fs-3" style="color: #fff;"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
{nav}
                <div class="d-flex align-items-center mt-3 mt-lg-0">

                    <button class="nav-search-btn me-3" id="navbarSearchBtn"><i class="fas fa-search"></i></button>
                    <a href="contact.html" class="btn-nav-highlight"><i class="fas fa-paper-plane me-1"></i> Plan My Trip</a>
                </div>
            </div>
        </div>
    </nav>

    <section class="destination-hero">
        <div class="destination-hero-bg" style="background-image: url('{hero_local}');"></div>
        <div class="destination-hero-overlay"></div>
        <div class="container position-relative destination-hero-content text-center text-white">
            <span class="destination-hero-badge gsap-fade-up">EXPLORE {name.upper()}</span>
            <h1 class="display-3 fw-bold gsap-fade-up">Discover {name}</h1>
            <p class="lead gsap-fade-up mx-auto" style="max-width: 720px;">{d["tagline"]}</p>
            <div class="mt-4 gsap-fade-up">
                <a href="#packages-list" class="btn-primary-glow me-2"><i class="fas fa-suitcase-rolling me-2"></i> View Packages</a>
                <a href="contact.html" class="btn-glass"><i class="fas fa-paper-plane me-2"></i> Custom Trip</a>
            </div>
        </div>
    </section>

    <section class="py-5">
        <div class="container py-4">
            <div class="row align-items-center g-5">
                <div class="col-lg-6 gsap-fade-up">
                    <span class="section-tag">About {name}</span>
                    <h2 class="section-title">Why Visit {name}?</h2>
                    <p class="section-desc text-start">{d["intro"]}</p>
                </div>
                <div class="col-lg-6 gsap-fade-up">
                    <div class="glass-panel p-4 destination-intro-card">
                        <div class="d-flex align-items-center mb-3"><i class="fas fa-map-marked-alt text-primary-blue fs-3 me-3"></i><div><h5 class="mb-0">Curated by Roamerly</h5><small class="text-muted">Handpicked stays &amp; local experts</small></div></div>
                        <div class="d-flex align-items-center mb-3"><i class="fas fa-shield-alt text-primary-blue fs-3 me-3"></i><div><h5 class="mb-0">Secure Booking</h5><small class="text-muted">Transparent pricing, no hidden fees</small></div></div>
                        <div class="d-flex align-items-center"><i class="fab fa-whatsapp text-success fs-3 me-3"></i><div><h5 class="mb-0">Instant Support</h5><small class="text-muted">WhatsApp assistance 24/7</small></div></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="py-5" style="background: rgba(255,255,255,0.35);">
        <div class="container py-4">
            <div class="section-header text-center mb-5 gsap-fade-up">
                <span class="section-tag">Top Spots</span>
                <h2 class="section-title">Must-Visit Places in {name}</h2>
            </div>
            <div class="row g-4 gsap-stagger-container">{places_html}
            </div>
        </div>
    </section>

    <section id="packages-list" class="py-5">
        <div class="container py-4">
            <div class="section-header text-center mb-5 gsap-fade-up">
                <span class="section-tag">Packages</span>
                <h2 class="section-title">{name} Holiday Packages</h2>
                <p class="section-desc">Premium &amp; budget-friendly itineraries — fully customizable.</p>
            </div>
            <div class="row g-5 justify-content-center">{pkg_html}
            </div>
        </div>
    </section>

    <section class="py-5">
        <div class="container gsap-fade-up">
            <div class="cta-box text-center">
                <h2 class="display-5 fw-bold mb-3">Plan Your {name} Trip Today</h2>
                <p class="lead mb-4">Tell us your dates and budget — we&apos;ll craft the perfect itinerary within hours.</p>
                <a href="contact.html" class="btn-glass px-5 py-3 fs-5 me-2"><i class="fas fa-paper-plane me-2"></i> Get Custom Quote</a>
                <a href="https://wa.me/{WHATSAPP}?text={quote('Plan my trip to ' + name)}" target="_blank" class="btn-primary-glow px-5 py-3 fs-5"><i class="fab fa-whatsapp me-2"></i> WhatsApp Us</a>
            </div>
        </div>
    </section>

    <footer id="contact" class="pt-5 pb-3">
        <div class="container text-center">
            <p class="text-white-50 small">&copy; 2026 Roamerly. <a href="index.html" class="text-white-50">Home</a> · <a href="contact.html" class="text-white-50">Contact</a></p>
        </div>
    </footer>

    <a href="https://wa.me/{WHATSAPP}" target="_blank" class="floating-btn whatsapp-btn"><i class="fab fa-whatsapp"></i></a>
    <button id="back-top-btn" class="floating-btn back-top-btn"><i class="fas fa-arrow-up"></i></button>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="assets/js/main.js"></script>
</body>
</html>'''


def main():
    print("Building domestic pages...")
    for d in DOMESTIC:
        html = render_page(d, is_domestic=True)
        with open(d["file"], "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {d['file']}")

    print("Building international pages...")
    for d in INTERNATIONAL_DATA:
        html = render_page(d, is_domestic=False)
        with open(d["file"], "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {d['file']}")

    print("Done — 24 unified destination pages.")


if __name__ == "__main__":
    main()
