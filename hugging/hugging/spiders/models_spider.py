import pandas as pd
import scrapy
from scrapy.http import TextResponse
from scrapy_playwright.page import PageMethod
from playwright.async_api import Page
from pathlib import Path
from time import sleep


class ModelsSpider(scrapy.Spider):
    """
    Collect URLs, information, and other information from huggingface model page
    """
    name = "models"
    url = "https://huggingface.co/"

    def start_requests(self):
        urls = [
            "https://huggingface.co/models"
        ]
        for url in urls:
            yield scrapy.Request(
                url, meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', selector='a.block'),
                    ]
                )
            )

    async def _parse_single_model(self, response: TextResponse):
        entry = []
        model_headers = response.xpath("//header[contains(@class, 'flex items-center mb-0.5')]")
        for header in model_headers:
            title = header.css("h4::text").get()
            entry.append({"title": title})
        return entry

    async def parse(self, response: TextResponse, **kwargs):
        data = []
        page: Page = response.meta["playwright_page"]
        entry = await self._parse_single_model(response)
        data.extend(entry)
        self.logger.info('[!] Writing file to data directory ...')
        if "?" in page.url:
            file_number = f"{page.url.split('?')[1].split('&')[0].replace('=', '_')}.csv"
        else:
            file_number = "p_0.csv"
        pd.DataFrame(data).to_csv(
            str(Path.cwd())+f"/data/{file_number}",
            index=False
        )
        next_page_button = page.get_by_text("Next", exact=True)
        if next_page_button:
            await next_page_button.click()
            page: Page = response.meta["playwright_page"]
            yield scrapy.Request(
                page.url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', selector='a.block'),
                    ]
                )
            )
        await page.close()

