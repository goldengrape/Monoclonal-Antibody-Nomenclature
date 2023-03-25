import asyncio
from playwright.async_api import async_playwright, expect
from playwright.async_api import Page
import sys
import os 

os.system("playwright install")

async def init(playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    return page

async def first_query(page: Page, query_string: str) -> None:
    await page.goto("https://poca-public.fda.gov/")
    await page.locator(".mat-checkbox-inner-container").click()
    await page.get_by_role("button", name="Accept", exact=True).click()
    await page.get_by_placeholder("Enter your proposed Drug Name").click()
    await page.get_by_placeholder("Enter your proposed Drug Name").fill(query_string)
    await page.get_by_role("button", name="Search", exact=True).click()
    await page.get_by_role("cell", name="Advanced Export to Excel").locator("a").click()
    return page

async def other_query(page: Page, query_string: str) -> None:
    await page.goto("https://poca-public.fda.gov/")
    await page.get_by_placeholder("Enter your proposed Drug Name").click()
    await page.get_by_placeholder("Enter your proposed Drug Name").fill(query_string)
    await page.get_by_role("button", name="Search", exact=True).click()
    await page.get_by_role("cell", name="Advanced Export to Excel").locator("a").click()
    return page

async def get_table(page: Page, sep=",") -> None:
    table = await page.query_selector('.mat-table.cdk-table.mat-sort.data-table')
    rows = await table.query_selector_all('tbody tr')
    data = []
    for row in rows[:3]:
        cells = await row.query_selector_all('td')
        row_data = f"{await cells[0].inner_text()}({await cells[1].inner_text()})"
        data.append(row_data)
    return data

async def main(query_list, item_sep=";", col_sep=","):
    async with async_playwright() as playwright:
        page = await init(playwright)
        df = {}
        for i in range(len(query_list)):
            q = query_list[i]
            query_method = first_query if i == 0 else other_query
            data = await get_table(await query_method(page, q), col_sep)
            data = item_sep.join(data)
            df[q] = data
    return df

# 从命令行读取参数query_list

if __name__ == "__main__":
    # query_list = ["vet", 'jup', 'innov']
    query_list = sys.argv[1:].split(",")
    df = asyncio.run(main(query_list))
    print("Done")
    print(df)
