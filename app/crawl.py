import re, requests

## Path ref ##
#https://minecraft.wiki/w/Item

## Return format ##

def crawling():
    base_path = "https://minecraft.wiki"
    start_path = "/w/Item"
    items_zip = []

    ## Get base HTML ##
    resp = requests.get(f"{base_path}{start_path}")
    if not resp.ok :
        raise(Exception("404 Not found"))
    resp = resp.text
    
    scope_data = re.search(r'<span class="mw-headline" id="List_of_items">(.*?)<span class="mw-headline" id="Video">', resp, re.DOTALL)
    scope_data = scope_data.group(0)
    # print(scope_data)

    header = re.findall(r'<h3>.*?<span class="mw-headline".*?>(.*?)<.*?</h3>', scope_data, re.DOTALL)
    header += re.findall(r'<h2>.*?>(.*?)<.*?</h2>', scope_data, re.DOTALL)
    # print(header)

    items_zip = re.findall(r'href="([^"]+)" title="(.*?)"', scope_data)
    # print(items_list)

    items_list = []
    links = []
    
    for item in items_zip: 
        items_list.append(item[1]) 
        links.append(item[0])
    print(links)
    
crawling()