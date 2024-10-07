import re
import requests
import html
import urllib.parse
import time
crawled_data = []

def crawling():
    global crawled_data
    base_path = "https://minecraft.wiki"
    start_path = "/w/Item"
    items_data = []
    crawled_data = []

    # print(f"Fetching main page: {base_path}{start_path}")
    resp = requests.get(f"{base_path}{start_path}")
    if not resp.ok:
        # print(f"Failed to fetch main page. Status code: {resp.status_code}")
        return []
    
    resp_text = resp.text
    # print(f"Main page fetched. Content length: {len(resp_text)}")
    
    scope_data = re.search(r'<span class="mw-headline" id="List_of_items">(.*?)<span class="mw-headline" id="Video">', resp_text, re.DOTALL)
    if scope_data:
        scope_data = scope_data.group(0)
        # print(f"Found 'List of items' section. Length: {len(scope_data)}")
    else:
        # print("Couldn't find the 'List of items' section")
        return []

    items_zip = re.findall(r'href="([^"]+)" title="([^"]+)".*?class="sprite-text">.*?</span></a>', scope_data)
    # print(f"Found {len(items_zip)} items")
    
    for i, (link, item_name) in enumerate(items_zip):
        print(f"Processing item {i+1}/{len(items_zip)}: {item_name}")
        item_url = f"{base_path}{link}"
        item_name = html.unescape(item_name)
        item_data = crawl_item_page(item_url, item_name, base_path)
        crawled_data.append(item_data)
        items_data.append(item_data)

    return items_data

def crawl_item_page(url, item_name, base_path):
    max_retries = 5
    retries = 0

    while retries < max_retries:
        resp = requests.get(url)

        if resp.status_code == 200:
            resp_text = resp.text
            
            # Extract image URL
            image_url = extract_image_url(resp_text, item_name)
            if image_url:
                image_url = base_path + image_url
            else:
                image_url = "No image found"

            # Extract other information
            rarity = extract_info(resp_text, "Rarity tier")
            renewable = extract_info(resp_text, "Renewable")
            stackable = extract_info(resp_text, "Stackable")

            return {
                "name": item_name,
                "url": url,
                "image_url": image_url,
                "rarity": rarity,
                "renewable": renewable,
                "stackable": stackable
            }

        elif resp.status_code == 429:
            wait_time = int(resp.headers.get("Retry-After", 1))
            print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying.")
            time.sleep(wait_time)
            retries += 1

        else:
            return {"name": item_name, "error": f"Error {resp.status_code}: {resp.reason}"}

    return {"name": item_name, "error": "Max retries exceeded"}

def extract_image_url(resp_text, item_name):
    item_name = item_name.replace(' ', '_')
    item_name = urllib.parse.quote(item_name)
    # Adjusted pattern to capture both 'thumb' and non-'thumb' URLs
    pattern = fr'<a href="/w/File:{html.escape(item_name)}.*?"mw-file-description".*?<img.*?src="([^"]+)"'
    
    # Search for the image tag in the HTML
    image_match = re.search(pattern, resp_text, re.IGNORECASE)
    
    # Return the extracted URL if found, else return "No image found"
    return image_match.group(1) if image_match else "No image found"

def extract_info(content, label):
    # Patterns for matching <th> or <td> with the given label, followed by the correct <td> or <p> with the value
    patterns = [
        fr'<th[^>]*>\s*(?:<a[^>]*>)?\s*{re.escape(label)}\s*(?:</a>)?\s*</th>\s*<td[^>]*>(.*?)</td>',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            # Clean the extracted value by removing any remaining HTML tags
            return re.sub('<.*?>', '', match.group(1)).strip()
    
    return "Not specified"

if __name__ == "__main__":
    print("Starting the crawler...")
    items = crawling()
    print(f"\nCrawling complete. Found {len(items)} items.")
    for item in items:
        print(f"\nItem: {item['name']}")
        print(f"URL: {item['url']}")
        print(f"Image URL: {item['image_url']}")
        print(f"Rarity: {item['rarity']}")
        print(f"Renewable: {item['renewable']}")
        print(f"Stackable: {item['stackable']}")
        print("---")