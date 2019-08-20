#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


import hashlib, time, aiohttp
import asyncio, json
import random



class Du_Spiders():
    def __init__(self):

        self.newurl = 'https://m.poizon.com/mapi/product/detail?productId={}&source=shareDetail&sign={}'

        with open('/Users/huanghaoran/PycharmProjects/StockX_Nice_spider/poll_package/Ip_agent.txt', 'r') as fd:
            pool_list = fd.readlines()

        self.Ip_pool = [i[:-1] for i in pool_list]



    async def get_sign(self, id):
        """
        获取加密sign，md5加密
        """
        sign = 'productId' + '{}'.format(id) + 'sourceshareDetail' + '048a9c4943398714b356a696503d2d36'

        hashm2 = hashlib.md5()

        hashm2.update(sign.encode('utf8'))

        newsign = hashm2.hexdigest()

        NewProductUrl = self.newurl.format(id, newsign)

        async with aiohttp.ClientSession() as session:

            proxy = random.choice(self.Ip_pool)

            async with session.get(NewProductUrl, verify_ssl=False, proxy='http://' + proxy) as resp:

                if resp.status != 200:
                    return

                else:
                    rp = await resp.text()

                    detal_page_information = json.loads(rp)

                    sellStatus = detal_page_information['data']['detail']['sellStatus']                                                                     #销售状态
                    title = detal_page_information['data']['detail']['title']                                                                                  #商品名称
                    color = detal_page_information['data']['detail']['color']





                asyncio.sleep(random.randint(2, 5))





if __name__=="__main__":

    startTime = time.time()

    du_spider = Du_Spiders()

    for i in range(1, 60000):
        tasks = [asyncio.ensure_future(du_spider.get_sign(i))]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

    endTime = time.time()

    print("用时{}分钟".format(round((endTime-startTime)/60, 2)))
