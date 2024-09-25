import re
import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    res = requests.get(url)
    return res.content

def extract_items(content):
    soup = BeautifulSoup(content, 'html.parser')
    items = set()

    main_content = soup.find('div', class_='mw-parser-output')
    if main_content:
        links = main_content.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('/wiki/'):
                item_name = link.text.strip()
                # ! Change this regular expression
                # Use regex to filter out non-item links, allowing for more diverse item names
                if re.match(r'^[A-Z][a-z]+( [A-Za-z0-9\'\-]+)*$', item_name):
                    items.add(item_name)
    
    return items

def crawl(start_url, max_depth=2):
    visited = set()
    all_items = set()
    to_visit = [(start_url, 0)]

    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue

        print(f'Crawling: {url}')
        content = get_page_content(url)
        # print(content)
        items = extract_items(content)
        all_items.update(items)
        visited.add(url)

        if depth < max_depth:
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=re.compile(r'^/wiki/'))
            print(links)
            for link in links:
                new_url = f"https://minecraft.wiki{link['href']}"
                if new_url not in visited:
                    to_visit.append((new_url, depth + 1))

    return all_items

# Updated start URL
start_url = 'https://minecraft.wiki/w/Item'
minecraft_items = crawl(start_url)

print(f'Total items found: {len(minecraft_items)}')
print('Sample items:')
for item in list(minecraft_items)[:10]:
    print(item)