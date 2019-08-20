#!/usr/bin/python
# -*- coding: UTF-8 -*-

import asyncio, aiohttp
import requests, re, time
from bs4 import BeautifulSoup




class agent_poll():
    def __init__(self):
        self.xici_url_list = [
            "https://www.xicidaili.com/wn/",
            "https://www.xicidaili.com/nn/",
            "https://www.xicidaili.com/nt/",
            "https://www.xicidaili.com/wt/"
        ]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }



    async def get_html(self, url):

        async with aiohttp.ClientSession() as session:

            async with session.get(url, headers=self.headers, verify_ssl=False) as reql:

                r = await reql.text()

                soup = BeautifulSoup(r, "html.parser")

                td_list = soup.select(".odd")

                for i in td_list:
                    porta = re.findall("<td>(.*?)</td>", str(i), re.S)
                    agent = {}

                    if porta[3] == "HTTP":

                        agent[porta[3]] = str(porta[0]) + ":" + str(porta[1])

                        checking_url = "http://www.baidu.com"

                        reql_checking = requests.get(checking_url, proxies=agent, timeout=1)

                        if reql_checking.status_code == 200:
                            with open('/Users/huanghaoran/PycharmProjects/StockX_Nice_spider/poll_package/Ip_agent.txt', 'a') as fd:
                                # fd.write(str(agent))
                                fd.write(str(porta[0]) + ":" + str(porta[1]))
                                fd.write("\n")

                        else:
                            print("代理{}不可以使用！".format(agent))



    def main(self):

        for i in self.xici_url_list:
            tasks = [asyncio.ensure_future(self.get_html(i))]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))







if __name__=="__main__":
    startTime = time.time()

    agentpoll = agent_poll()
    agentpoll.main()

    endTime = time.time()

    print("程序用时{}分钟！".format(round((endTime-startTime)/60, 2)))


