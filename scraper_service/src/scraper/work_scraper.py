import httpx
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime

from schemas import WorkSchema



class WorkScraper:
    def __init__(self):
        self.url = "https://www.work.ua"
        self.queries = "/jobs-python+developer/"
        self.header = {
            'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://www.google.com/',
        }

        self.list_work = []
        self.scraped_data = []


    async def scrap_list_work_page(self):
        runing = True
        while runing:
            async with httpx.AsyncClient(headers=self.header) as client:
                res = await client.get(f'{self.url}{self.queries}')

                soup = BeautifulSoup(res.text, "lxml")
                try:

                    list_work_el = soup.find("div", attrs={"id":"pjax-jobs-list"})

                    a_link_els = list_work_el.find_all('a', attrs={"tabindex": "-1"})
                
                    for a in a_link_els:
                        self.list_work.append(a['href'])            
            
                    pagination_ul = soup.find("ul", class_="pagination hidden-xs") 

                    try:
                        if pagination_ul.find('li', class_="no-style disabled add-left-default"):
                            break
                        next_el = pagination_ul.find_all("a", class_="link-icon")[1]
                    except:
                        next_el = pagination_ul.find("a", class_="link-icon")

                    self.queries = next_el['href']

                    if not  self.queries:
                        runing = False

                except Exception as e:
                    runing = False
                    raise e


    async def __scrap_work(self, link, client):
        work_link_url = f"{self.url}{link}"
        res = await client.get(url=work_link_url)

        soup = BeautifulSoup(res.text, "lxml")

        title_el = soup.find('h1', attrs={"id": "h1-name"})
        content_el = soup.find('div', attrs={"id":"job-description"})

        sub_title_el = soup.find_all('li', class_="text-indent no-style mt-sm mb-0")

        list_technologies_el = soup.find_all('ul', class_="flex flex-wrap list-unstyled w-100 my-0 pb-0 toggle-block overflow block-relative js-toggle-block")

        published_el = soup.find('time', class_="text-default-7 mr-xs mb-sm")

        date_val = published_el.get("datetime")

        if '.' in date_val:
            date_val = date_val.split('.')[0]


        return WorkSchema(
            source="work.ua",
            url=work_link_url,
            title=title_el.text,
            content=content_el.text,
            company=sub_title_el[0].text,
            remote=sub_title_el[1].text,
            time=sub_title_el[2].text,
            eng_level=sub_title_el[3].text if len(sub_title_el) >= 4 else None,
            tags=[t.text for t in list_technologies_el],
            published_at=datetime.strptime(date_val, '%Y-%m-%d %H:%M:%S')
        )

    async def scrap_list_work(self):
        tasks = []
        async with httpx.AsyncClient(headers=self.header) as client:
            for link in self.list_work:
                tasks.append(self.__scrap_work(link, client))

            res = await asyncio.gather(*tasks)

            self.scraped_data = [data for data in res if data is not None]



async def main():
    work = WorkScraper()

    await work.scrap_list_work_page()

    await work.scrap_list_work()


if __name__ == "__main__":
    asyncio.run(main())
