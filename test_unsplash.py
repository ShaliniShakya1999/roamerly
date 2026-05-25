import urllib.request, urllib.parse
import re

query = urllib.parse.quote("Dudhsagar Falls Goa")
url = f"https://www.bing.com/images/search?q={query}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8')
    
    print("HTML length:", len(html))
    # Bing images has image details in JSON format inside m="..." attribute of class="iusc"
    # Format: m="{"ns":"...", "k":"...", "murl":"https://example.com/image.jpg", ...}"
    matches = re.findall(r'm="([^"]+)"', html)
    print("Found image detail strings:", len(matches))
    
    import html as html_parser
    import json
    
    urls = []
    for m in matches[:5]:
        # Decode HTML entities (like &quot;)
        decoded_m = html_parser.unescape(m)
        try:
            js = json.loads(decoded_m)
            if 'murl' in js:
                urls.append(js['murl'])
        except Exception as e:
            pass
            
    print("Extracted image URLs:")
    for u in urls:
        print("  ", u)
except Exception as e:
    print("Error:", e)
