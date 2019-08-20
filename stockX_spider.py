#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


import requests, re, random
import time, aiohttp, asyncio
from lxml import etree
import multiprocessing as mp
from bs4 import BeautifulSoup
from urllib.request import urljoin




class stockX_all_data_spider():
    def __init__(self):

        with open('/Users/huanghaoran/PycharmProjects/StockX_Nice_spider/poll_package/Ip_agent.txt', 'r') as fd:
            pool_list = fd.readlines()

        self.Ip_pool = [i[:-1] for i in pool_list]

        self.all_product_html_url = 'https://stockx.com/sneakers'

        self.stockX_headers = {
            "authority": "stockx.com",
            "method": "GET",
            "path": "/sneakers",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "__cfduid=d913ad3a0f661753201e8aa96d701220a1565078503; cto_lwid=f677103e-dbb4-4f6a-9eb7-71ce859dc9ae; _ga=GA1.2.1094966298.1565078507; _tl_duuid=a4272710-b8ed-461e-8317-7cff3525c493; _gcl_au=1.1.1265765900.1565078508; tracker_device=6add66fd-700c-4b41-aafe-2b1040bc4a61; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22e7f4aa42-1283-4ea1-b1c0-243ab9116536%22; _omappvp=I7KwQ2BM6hsyFy62Mrj81LPkSH4LviDHX9zY2hal37e4uj222bJe48aTOePJEfBIjQy59KrTnYrWi4kYufcQgN9PPWMuqpMH; _fbp=fb.1.1565078510060.112687029; rskxRunCookie=0; rCookie=yth6v9mnvoo8n6dk1jy1dtjyzjgjne; _pxhd=df7b760f7b04863c99638f4e0aca931dbc2348d00ee455a708c546893fb9b982:a1db3661-bca3-11e9-9d5a-cd41adbe5746; _ALGOLIA=anonymous-4ff95e2c-00ee-4b66-80f4-f43439bbc399; stockx_session=26hfs1g7jz7qrjok1565574718052; IR_gbd=stockx.com; stockx_bagmodal_dismissed=true; stockx_product_visits=5; _gid=GA1.2.1032472668.1566179230; is_gdpr=false; stockx_selected_currency=USD; stockx_selected_locale=US; show_all_as_number=false; brand_tiles_version=v1; show_bid_education=v2; show_bid_education_times=1; multi_edit_option=beatLowestAskBy; product_page_v2=watches%2Chandbags; show_watch_modal=false; progress_bar_variant=; cookie_policy_accepted=true; _sp_ses.1a3e=*; _tl_csid=c1e3bd73-475b-4c39-a382-65b354f67f7f; _pk_ref.421.1a3e=%5B%22%22%2C%22%22%2C1566183981%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DYmEYggAmSuABght4IyRVSmkUBNksFny53WzZE8xR7XG%26wd%3D%26eqid%3De86e8d1700274c8b000000045d59ff91%22%5D; _pk_ses.421.1a3e=*; _tl_auid=5d4933ec79802e0019362523; _tl_sid=5d5a1231fc2d8300d2e825c8; _gat=1; lastRskxRun=1566184180527; _pk_id.421.1a3e=265bb26256e10d01.1565078507.5.1566184181.1566179246.; tl_sopts_c1e3bd73-475b-4c39-a382-65b354f67f7f_p_p_n=JTJGc25lYWtlcnM=; tl_sopts_c1e3bd73-475b-4c39-a382-65b354f67f7f_p_p_l_h=aHR0cHMlM0ElMkYlMkZzdG9ja3guY29tJTJGc25lYWtlcnM=; tl_sopts_c1e3bd73-475b-4c39-a382-65b354f67f7f_p_p_l_t=U3RvY2tYJTNBJTIwQnV5JTIwYW5kJTIwU2VsbCUyMFNuZWFrZXJzJTJDJTIwU3RyZWV0d2VhciUyQyUyMEhhbmRiYWdzJTJDJTIwV2F0Y2hlcw==; tl_sopts_c1e3bd73-475b-4c39-a382-65b354f67f7f_p_p_l=JTdCJTIyaHJlZiUyMiUzQSUyMmh0dHBzJTNBJTJGJTJGc3RvY2t4LmNvbSUyRnNuZWFrZXJzJTIyJTJDJTIyaGFzaCUyMiUzQSUyMiUyMiUyQyUyMnNlYXJjaCUyMiUzQSUyMiUyMiUyQyUyMmhvc3QlMjIlM0ElMjJzdG9ja3guY29tJTIyJTJDJTIycHJvdG9jb2wlMjIlM0ElMjJodHRwcyUzQSUyMiUyQyUyMnBhdGhuYW1lJTIyJTNBJTIyJTJGc25lYWtlcnMlMjIlMkMlMjJ0aXRsZSUyMiUzQSUyMlN0b2NrWCUzQSUyMEJ1eSUyMGFuZCUyMFNlbGwlMjBTbmVha2VycyUyQyUyMFN0cmVldHdlYXIlMkMlMjBIYW5kYmFncyUyQyUyMFdhdGNoZXMlMjIlN0Q=; tl_sopts_c1e3bd73-475b-4c39-a382-65b354f67f7f_p_p_v_d=MjAxOS0wOC0xOVQwMyUzQTA5JTNBNDAuNTY4Wg==; IR_9060=1566184094037%7C0%7C1566183982191%7C%7C; IR_PI=721f7830-b820-11e9-965d-42010a246302%7C1566270494037; stockx_homepage=sneakers; _sp_id.1a3e=09d2991e-4369-4b01-9107-1e0f6f01d1ad.1565078507.4.1566184200.1566180031.79d15e72-72bd-43ce-824a-b3f6ab43c944",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }

        self.url_lst_successed = []

        self.url_lst_failed = []



    def get_The_child_links(self):
        all_product_html = requests.get(self.all_product_html_url, headers=self.stockX_headers)

        The_child_links_list =  re.findall('class="categoryOption"><div class="">(.*?)</div>', all_product_html.text, re.S)

        child_links_list = []
        for i in The_child_links_list:
            if i != "Below Retail":
                child_links_list.append("https://stockx.com/" + i)
                child_links_list.append("https://stockx.com/" + i + "?belowRetail=true")

        return child_links_list




    async def Get_product_list(self, url):

        async with aiohttp.ClientSession() as session:

            proxy = random.choice(self.Ip_pool)

            async with session.get(url, headers=self.stockX_headers, verify_ssl=False, proxy='http://' + proxy,) as resp:

                if resp.status != 200:
                    self.url_lst_failed.append(url)
                else:
                    self.url_lst_successed.append(url)

                r = await resp.text()

                product_href_list = etree.HTML(r).xpath('//*[@id="products-container"]/div[2]/div[2]/div/div/a/@href')

                for i in product_href_list:
                    product_url = 'https://stockx.com/' + i

                    print(product_url)

                asyncio.sleep(random.randint(2, 6))















if __name__=='__main__':
    stockX_spider = stockX_all_data_spider()
    url_lst = stockX_spider.get_The_child_links()

    tasks = [asyncio.ensure_future(stockX_spider.Get_product_list(str(url.lower()) + "?page=" + str(i))) for url in url_lst for i in range(1, 26)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

