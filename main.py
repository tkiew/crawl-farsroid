import asyncio
import aiohttp
from bs4 import BeautifulSoup
async def getdata(q: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.farsroid.com/", params={"s": q}) as response:
            req = await response.text()
            soup = BeautifulSoup(req, "html.parser")
            links = soup.find_all("a", {"rel": "bookmark"})
            tasks = []
            for link in links:
                link, text = link["href"], link.get_text()
                tasks.append(asyncio.create_task(getlink(link, text)))
            results = await asyncio.gather(*tasks)
            return results

async def getlink(link: str, text: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            req = await response.text()
            soup = BeautifulSoup(req, "html.parser")
            download_links = soup.find_all("a", {"class": "download-btn"})
            return {"link": link, "link_text": text.strip(), "download_links": [{"link": url["href"], "link_text": url.get_text().strip()} for url in download_links]}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(getdata("Music"))
    print(results)

