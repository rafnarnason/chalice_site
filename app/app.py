from chalice import Chalice
import httpx
from bs4 import BeautifulSoup
from slugify import slugify

app = Chalice(app_name='app')


@app.route('/')
def index():
    r = httpx.get('https://www.kevinrooke.com/book-recommendations')
    soup = BeautifulSoup(r.text, 'html.parser')
    names = [i["alt"] for i in soup.findAll('img', {'class': 'image-27'})]
    links = [f"http://localhost:8000/book-recommendations/{slugify(name)}" for name in names]
    return links


@app.route('/book-recommendations/{person}')
def recommend(person):
    r = httpx.get(f"https://www.kevinrooke.com/book-recommendations/{person}")
    soup = BeautifulSoup(r.text, 'html.parser')
    result = []
    for entry in soup.find_all('div', {'class': 'collection-item-5'}):
        data = {
            "title": entry.find("h1").text.strip(),
            "slug": slugify(entry.find("h1").text).strip(),
            "author": entry.find("h2").text.strip(),
            "recommended_by": [e.text.strip() for e in entry.find_all('div', {'class': 'recommended-by-text-block'})],
            "image": entry.find('img', {'class': 'book-image'}).get("src")
        }
        result.append(data)
    return result
















# "comments": [e.text for e in entry.find_all('div', {'class': 'recommended-by-text-block'})] #LATER
