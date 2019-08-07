#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

import requests, time, asyncio
import json, random, xlwt



header = {
        'Content-Type': 'keep-alive',
        'Host': 'api.oneniceapp.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'KKShopping/5.3.9 (iPhone XR; iOS 12.1.4; Scale/2.00)',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Content-Length': '123',
        'Accept-Encoding': 'gzip, deflate'
    }

newList = []


def createxcle(alllist):

    book = xlwt.Workbook()  # 创建一个Excel

    sheet1 = book.add_sheet('sheet')  # 在其中创建一个名为hello的sheet

    i = 0  # 行序号
    for onelist in alllist:
        j = 0  # 列序号

        for showmsg in onelist:
            sheet1.write(i, j, showmsg)  # 往sheet里第一行第一列写一个数据

            j = j + 1  # 列号递增
        i = i + 1  # 行号递增

    book.save("/Users/huanghaoran/Desktop/NiceTop100.xls")





async def asyncData(url, data):
    global newList

    req = requests.post(url, data=data, headers=header, verify=False)

    responsejosn = req.text

    responsetext = json.loads(responsejosn)  # data是向 api请求的响应数据，data必须是字符串类型的

    newjson = json.dumps(responsetext, ensure_ascii=False)  # ensure_ascii=False 就不会用 ASCII 编码，中文就可以正常显示了

    response = json.loads(newjson)

    for j in response['data']['list']:
        oneList = []

        oneList.append(j['name'])
        oneList.append(str(j['infos']['first_text']) + ' 件')
        newList.append(oneList)

        await asyncio.sleep(random.randint(2, 5))






def get_id_name_sku():

    data_url = {
        'nice-sign-v1://e66888212117387ce8c9a75dce49f6c3:0639cbcfc3430ae6/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":""}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.206345&a_y=-0.618790&a_z=-0.766190&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.027486&g_y=0.005279&g_z=0.009278&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://9612758d883a84d59476c01c227a113c:734e5d5050ace99c/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"10"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://b576f1ec2ef4802f26d6c3d2369887c6:7fb3a3f6c11ebad3/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"20"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://1b4550c10643603ab0c3e1985409764d:2299eb4a171faa20/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"30"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://81811570fcc9fce1fa0b6f46a9e872e8:d3e7543a1701c543/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"40"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://1329658cd90e999b02f825cf5a037c0d:7d32860d5c592769/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"50"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://1689950aca37a9b5c99da23b7e28f71b:c1a78263cbaa1daf/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"60"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://e2cace5611eaa5f96e34ad6c153249df:a0ba41e34010f73f/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"70"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://11ec3c35b373a54e89f52e78c0da8f12:65f9ac3576b06fa3/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"80"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000),
        'nice-sign-v1://03cc6a4c9466eda33e081cbc8f8a3732:5e829adb2d2d158d/{"token":"GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD","type":"allgoods","rank":"sell","nextkey":"90"}': 'https://115.182.19.27/product/getsimpleranklist?a_x=-0.097641&a_y=-0.503036&a_z=-0.838486&abroad=no&amap_latitude=31.170072&amap_longitude=121.410552&appv=5.4.8.20&ch=AppStore_5.4.8.20&did=4e90e77b9e6135e8b41d5309813ca90f&dn=%E9%BB%84%E6%B5%A9%E7%84%B6%E7%9A%84%20iPhone&dt=iPhone11%2C8&g_x=-0.012060&g_y=-0.024904&g_z=0.011487&geoacc=10&im=00000000-0000-0000-0000-000000000000&la=cn&latitude=31.171936&lm=weixin&longitude=121.405906&lp=-1.000000&n_bssid=&n_dns=192.168.2.1&n_ssid=&net=0-0-wifi&osn=iOS&osv=12.3.1&seid=a099ac195bb68f3a716aa99d08c386a9&sh=896.000000&sm_dt=201901192127432e7397d9720849bee17e93544985d0c7011c86917c4d0bd3&sw=414.000000&token=GqfrMvX-2BsT4k8t6ss8Pgy-AIC1E2aD&ts={}'.format(time.time()*1000)
    }

    for i, j in data_url.items():

        loop.run_until_complete(asyncData(j, i))

    newList.insert(0, ['商品名称', '销售量'])

    createxcle(newList)



if __name__=='__main__':

    loop = asyncio.get_event_loop()

    get_id_name_sku()