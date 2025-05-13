import requests
from bs4 import BeautifulSoup

BASE_URL = "https://healme.kr"
MAX_POSTS = 1000
STEP = 150
urls = []

for start in range(1, MAX_POSTS, STEP):
    feed_url = f"{BASE_URL}/atom.xml?redirect=false&start-index={start}&max-results={STEP}"
    print(f"📡 Fetching: {feed_url}")
    res = requests.get(feed_url)
    soup = BeautifulSoup(res.content, "xml")
    entries = soup.find_all("entry")
    print(f"✔️ Found {len(entries)} entries")

    for entry in entries:
        links = entry.find_all("link")
        for link in links:
            print(f"🔗 link: {link}")
        # 시도: rel="alternate" 또는 첫 번째 링크
        link = entry.find("link", {"rel": "alternate"}) or entry.find("link")
        if link and link.get("href"):
            urls.append(link["href"])

print(f"✅ Total URLs: {len(urls)}")

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{u}</loc></url>\n")
    f.write('</urlset>')
