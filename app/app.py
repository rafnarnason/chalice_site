from chalice import Chalice
import httpx
from bs4 import BeautifulSoup
from slugify import slugify
import urllib.parse
import json
import logging

app = Chalice(app_name='app')

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}




@app.route('/book-recommendations/{person}')
def recommend(person):
    print(person,"##########################################################")
    result = []
    try:
        r = httpx.get(f"https://www.kevinrooke.com/book-recommendations/{person}",headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = []
        for entry in soup.find_all('div', {'class': 'collection-item-5'}):
            data = {
                "title": entry.find("h1").text.strip(),
                "slug": slugify(entry.find("h1").text).strip(),
                "author": entry.find("h2").text.strip(),
                "recommended_by": [e.text.strip() for e in entry.find_all('div', {'class': 'recommended-by-text-block'})],
                "image": entry.find('img', {'class': 'book-image'}).get("src"),
                "genius_link": entry.find('a', {'class': 'link-block-24'}).get("href"),
            }
            query = urllib.parse.quote(f"{data['title']} {data['author']}")
            data["amzn"] = f"https://www.amazon.com/s?k={query}"
            result.append(data)
    except Exception as e:
        logging.error(e)
    
    return result



@app.route('/')
def index():
    r = httpx.get('https://www.kevinrooke.com/book-recommendations',headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    names = [i["alt"] for i in soup.findAll('img', {'class': 'image-27'})]
    links = [f"{slugify(name)}" for name in names]
    return links
    with open('chalicelib/people.json', 'w', encoding='utf-8') as f:
        data = { i : recommend(i) for i in links }
        res = json.dump(data, f, ensure_ascii=False, indent=4)
    return data











## DUMPSTER

## more text
# "comments": [e.text for e in entry.find_all('div', {'class': 'recommended-by-text-block'})] #LATER

## redirect or other ways
# response = httpx.get(data["genius_link"],headers=headers,follow_redirects=True)
# print(response)
# if response.history:
#     for resp in response.history:
#         print(resp.status_code, resp.url)
