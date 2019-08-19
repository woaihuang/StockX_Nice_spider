#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



'协程异步'
import asyncio, random
import re, json, aiohttp
from bs4 import BeautifulSoup




first_url = "https://www.kugou.com/yy/html/rank.html?from=homepage"

headers = {
    'cookie': 'kg_mid=5eadfe887735621c3b4acc934c58e9d4; kg_dfid=0hk22J4SuCE30KlWlk2mltjn; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1564988362,1564988582,1564988645,1565860609; ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22gzlogin-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10016=%7B%22list%22%3A%5B%5B%22gzreg-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10017=%7B%22list%22%3A%5B%5B%22gzverifycode.service.kugou.com%22%5D%5D%7D; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid_temp=5eadfe887735621c3b4acc934c58e9d4; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1565860761',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

play_url_list = []
href_list = []
music_url_list = []



async def Get_html(session, url):
    async with session.get(url, headers=headers, verify_ssl=False) as response:
        asyncio.sleep(random.randint(2, 4))
        return await response.text()





async def download_music(session, url, song_name):
    async with session.get(url, headers=headers, verify_ssl=False) as response:
        asyncio.sleep(random.randint(2, 4))
        with open('/Users/huanghaoran/PycharmProjects/StockX_Nice_spider/song/{}'.format(song_name), 'wb') as fd:
            while 1:
                chunk = await response.content.read(1024)  # 每次获取1024字节
                fd.write(chunk)





async def main():

    global href_list, play_url_list, music_url_list



    async with aiohttp.ClientSession() as session:
        html = await Get_html(session, first_url)

        soup = BeautifulSoup(html, 'html.parser')

        li_list = soup.select('.pc_temp_side div ul li a')

        for i in li_list:
            href = re.findall('href=\"(.*?)\"', str(i), re.S)

            href_list.append(href[0])




    for href_url in href_list:
        async with aiohttp.ClientSession() as session1:

            asyncio.sleep(random.randint(2, 4))

            html1 = await Get_html(session1, href_url)

            Hash_list = re.findall('global.features = (.*?)];', html1)

            for i in eval(Hash_list[0]+']'):
                play_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash=' + i['Hash']

                play_url_list.append(play_url)





    for play_url in play_url_list:

        async with aiohttp.ClientSession() as session2:
            music_url_dict = []
            asyncio.sleep(random.randint(2, 4))

            html2 = await Get_html(session2, play_url)

            song_details = json.loads(html2)

            song_name = song_details['data']['song_name'] + '.mp3'

            song_play_url = song_details['data']['play_url']

            music_url_dict.append(song_name)
            music_url_dict.append(song_play_url)
            music_url_list.append(music_url_dict)

    for music_url in music_url_list:
        async with aiohttp.ClientSession() as session3:
            asyncio.sleep(random.randint(2, 4))

            await download_music(session3, music_url[1], music_url[0])







if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

