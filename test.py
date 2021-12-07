import asyncio
import time
#スクレイピングツール
# pip install pyppeteer をしてください
from pyppeteer import launch

async def requestdata(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle2')

    time.sleep(10)
    
    element_unit_info = await page.JJ('div.post_mrstarchive_info')

    result = list()
    # print(len(element_unit_info))
    for info in element_unit_info:
        #ユニット名取得
        name_span = await info.J('div.post_mrstunit_title > h2 > span')
        name = await (await name_span.getProperty('textContent')).jsonValue()
        print(name)

        #計算値取得(もしかしたらミスってるかも)
        calc_result_title_span = await info.J('div.post_mrstunit_detail > span.data_calc > span.data_title')
        calc_result_value_span = await info.J('div.post_mrstunit_detail > span.data_calc > span.value')
        calc_result_title = await (await calc_result_title_span.getProperty('textContent')).jsonValue()
        calc_result_value = await (await calc_result_value_span.getProperty('textContent')).jsonValue()
        print(calc_result_title + calc_result_value)

        #お好きなように
        result.append({name: calc_result_title + calc_result_value})
    
    return result

# How To Use
if __name__ == "__main__":
    # requestUrl = 'https://yugalab.net/mrst/units?smo=0&mrstunit_type=water&mrstunit_weapon=bow&cgt=2&cfa=5&cfw=3&cft=5&cmi=100,101,101&gag=5&skilv=1&sort=28'
    # だめなurl
    requestUrl = 'https://yugalab.net/mrst/units?smo=0&mrstunit_type=water&cgt=2&cfa=5&cfw=3&cft=5&cmi=100,101,101&gag=5&skilv=1&sort=28'
    # requestUrl = 'https://yugalab.net/mrst/units?smo=0&mrstunit_type=water&mrstunit_weapon=bow&cgt=2&cfa=5&cfw=3&cft=5&cas=5&cmi=100,101,101&gag=5&skilv=1&sort=33'
    result = asyncio.get_event_loop().run_until_complete(requestdata(requestUrl))
    print(result)
