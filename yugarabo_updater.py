import asyncio
import os
import time
from pyppeteer import launch
import ast
import json
from collections import OrderedDict
import pprint
import tqdm


async def requestdata(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle2')

    time.sleep(10)
    result = await page.evaluate('''() => { return unitsdatajson; }''')
   
    return result

# How To Use
if __name__ == "__main__":
    requestUrls = [
        'https://yugalab.net/mrst/units?mrstunit_type=fire',
        'https://yugalab.net/mrst/units?mrstunit_type=water',
        'https://yugalab.net/mrst/units?mrstunit_type=wind',
        'https://yugalab.net/mrst/units?mrstunit_type=light',
        'https://yugalab.net/mrst/units?mrstunit_type=dark',
        ]
    # requestUrls = ['https://yugalab.net/mrst/units?mrstunit_type=water&mrstunit_weapon=stab&mrstunit_reach=1&mrstunit_from=17']
    os.makedirs('yugarabo_json', exist_ok=True)
    results = []
    for url in tqdm.tqdm(requestUrls, 'updating'):
        result = asyncio.get_event_loop().run_until_complete(requestdata(url))
        results.append(result)
    for i, res in enumerate(results):
        savename = 'yugarabo_json/' + requestUrls[i].replace('https://yugalab.net/mrst/units?mrstunit_type=','') + '.json'
        with open(savename, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
