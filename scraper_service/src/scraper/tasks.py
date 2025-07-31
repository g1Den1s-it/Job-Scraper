import asyncio
from src.scraper.celery import celery_app


from src.scraper.work_scraper import WorkScraper



@celery_app.task(is_async=True)
async def scrap_work():
    try:
        work = WorkScraper()

        await work.scrap_list_work_page()

        await work.scrap_list_work()

        print(work.scraped_data)

    except Exception as e:
        raise e
    