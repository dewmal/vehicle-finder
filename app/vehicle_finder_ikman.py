import requests
from bs4 import BeautifulSoup

def get_vehicle_details(query:str):
    # Replace with your target URL
    url = f"https://ikman.lk/en/ads/sri-lanka/vehicles?sort=relevance&buy_now=0&urgent=0&query={query}&page=1"  

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
    }

    # Fetch HTML
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raise error if request fails

    soup = BeautifulSoup(response.text, "html.parser")

    ads = []

    # Find the UL that contains all listings
    ul = soup.find("ul", class_="list--3NxGO")

    if ul:
        for li in ul.find_all("li", recursive=False):
            try:
                title = li.find("h2").get_text(strip=True)
                link = li.find("a")["href"]
                image = li.find("img")["src"] if li.find("img") else None
                km = li.find("div", class_="details--1GUIn").get_text(strip=True)
                location_category = li.find("div", class_="description--2-ez3").get_text(strip=True)
                price = li.find("div", class_="price--3SnqI").get_text(strip=True)
                updated = li.find("div", class_="updated-time--1DbCk").get_text(strip=True)

                ads.append({
                    "title": title,
                    "link": "https://ikman.lk" + link,
                    "image": image,
                    "mileage": km,
                    "location_category": location_category,
                    "price": price,
                    "updated": updated
                })
            except Exception as e:
                print("Skipping LI due to error:", e)

    # Show extracted ads
    for ad in ads:
        print(ad)
        
    return ads

if __name__ == "__main__":
    res = get_vehicle_details("Alto")
    print(res)