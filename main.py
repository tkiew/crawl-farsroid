from requests import get
from bs4 import BeautifulSoup

def getdata(q: str):
    req = get("https://www.farsroid.com/", {"s": q}).text
    soup = BeautifulSoup(req, "html.parser")
    links = soup.find_all("a", {"rel": "bookmark"})
    for link in links:
        link, text = link["href"], link.get_text()
        req = get(link).text
        soup = BeautifulSoup(req, "html.parser")
        download_links =  soup.find_all("a", {"class": "download-btn"})
        yield {"link": link, "link_text": text.strip(), "download_links": [{"link": url["href"], "link_text": url.get_text().strip()} for url in download_links]}

if __name__ == "__main__":
	for info in getdata("Music"): print(info)go get github.com/PuerkitoBio/goquery
