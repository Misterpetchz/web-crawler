import re, requests

## Path ref ##
#https://minecraft-archive.fandom.com/wiki/Items

## Return format ##

def crawling():
    base_path = "https://minecraft-archive.fandom.com"
    start_path = "/wiki/Items"
    items_list = []

    ## Get base HTML ##
    resp = requests.get(f"{base_path}{start_path}")
    if not resp.ok :
        raise(Exception("404 Not found"))
    resp = resp.text

    ## Get Alphabet of the page ##
    header = re.findall(r'<span class="mw-headline" id="[^"]*\/[^"]*">([^<]+)</span>', resp)
    # print(header)
    
    all_items_list = re.search(r'<tbody>.*?</tbody>', resp, re.DOTALL)
    all_items_list = all_items_list.group(0)
    
    categories = re.findall(r'<th class="navbox-group">(.*?)</th>', all_items_list, re.DOTALL)
    category_names = [re.sub(r'<a.*?>(.*?)</a>', r'\1', category) for category in categories]
    
    items_list_text = re.findall(r'<td class="navbox-list">(.*?)</td>', all_items_list, re.DOTALL)
    items_lists = [re.findall(r'href="([^"]+)" title="(.*?)"', items_text) for items_text in items_list_text]

    zipped_items = []
    links = []
    
    for category_name, items in zip(category_names, items_lists):
        for item in items:
            zipped_items.append((category_name, item[1]))
            links.append(item[0])
    
crawling()