import requests
from bs4 import BeautifulSoup

def fetch_link_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return {"title": None, "description": None, "image": None}

    soup = BeautifulSoup(response.content, 'html.parser')

    og_title = soup.find("meta", property="og:title")
    og_description = soup.find("meta", property="og:description")
    og_image = soup.find("meta", property="og:image")

    title = og_title["content"] if og_title else soup.find("title").string if soup.find("title") else None
    description = og_description["content"] if og_description else (
        soup.find("meta", attrs={"name": "description"})["content"]
        if soup.find("meta", attrs={"name": "description"})
        else None
    )
    image = og_image["content"] if og_image else None

    return {
        "title": title,
        "description": description,
        "image": image,
    }