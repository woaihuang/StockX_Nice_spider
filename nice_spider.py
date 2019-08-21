#!/usr/bin/python
#-*- coding: UTF-8 -*-


import requests, json



class Nice_spider():
    def __init__(self):

        self.url = "https://sneakers-wxmp.oneniceapp.com/index/load_more?b=iPhone&m=iPhone%20XR%3CiPhone11%2C8%3E&pr=2&sw=414&sh=896&ww=414&wh=726&sbh=44&l=zh_CN&wxv=7.0.5&osv=iOS%2012.3.1&osn=ios&fss=17&sdkv=2.8.1&mpv=0.1.3"

        self.headers = {
            "Host": "sneakers-wxmp.oneniceapp.com",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "br, gzip,deflate",
            "Connection": "keep-alive",
            "Cookie": "nice_sneakers_auth=omgvnEnnPQpi4D1AAPzLAm5oCbTXigAAHMfgygGnsoatJWkDLQ%3D%3D",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI",
            "Referer": "https://servicewechat.com/wx67b11ce5112789b5/44/page-frame.html",
            "Content-Length": "14",
            "Accept-Language": "zh-cn"
        }


        self.header = {
            "Host": "sneakers-wxmp.oneniceapp.com",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "0",
            "Connection": "keep-alive",
            "Cookie": "nice_sneakers_auth=omgvnEnnPQpi4D1AAPzLAm5oCbTXigAAHMfgygGnsoatJWkDLQ%3D%3D",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wx67b11ce5112789b5/44/page-frame.html",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "br, gzip, deflate"
        }



    def search_data(self, sku):

        id_list = []

        self.data = {"search_key": "{}".format(sku)}

        while True:

            reql = requests.post(self.url, data=self.data)

            product_json = json.loads(reql.text)

            product_list = product_json['data']['products']

            if len(product_list) > 0:

                for product in product_list:
                    if str(product['sku']).replace(' ', '-') == sku:
                        print(product['id'])
                        productid = product['id']
                        productsku = str(product['sku']).replace(' ', '-')

                        id_list.append(productid)

                        break
                break

        return id_list



    def product_details(self, sku):

        id_list = self.search_data(sku)

        for productId in id_list:

            product_url = 'https://sneakers-wxmp.oneniceapp.com/product/stocks/{}?b=iPhone&m=iPhone%20XR%3CiPhone11%2C8%3E&pr=2&sw=414&sh=896&ww=414&wh=726&sbh=44&l=zh_CN&wxv=7.0.5&osv=iOS%2012.3.1&osn=ios&fss=17&sdkv=2.8.1&mpv=0.1.3'.format(productId)

            reql = requests.get(product_url, headers=self.header)

            details_dict = json.loads(reql.text)

            product_size_list = details_dict['data']['stocks']

            for sizelist in product_size_list:
                product_size = sizelist['size']
                product_price = sizelist['price']







if __name__ == '__main__':
    nice_spider = Nice_spider()

    nice_spider.product_details('CT2253-100')