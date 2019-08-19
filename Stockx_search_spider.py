#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



from qiniu import Auth, put_file, etag
import requests, pymysql
import datetime, time
import json
import re


class StockX_Nice_spider():
    def __init__(self, stockx_sku):

        self.stockx_sku = stockx_sku

        self.stockx_url = 'https://stockx.com/api/browse?productCategory=sneakers&sort=featured&order=DESC&_search={}&dataType=product'.format(self.stockx_sku)

        self.stockX_headers = {
            'authority': 'stockx.com',
            'method': 'GET',
            'path': '/api/browse?productCategory=sneakers&sort=featured&order=DESC&_search={}&dataType=product'.format(self.stockx_sku),
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'appos': 'web',
            'appversion': '0.1',
            'cookie': '__cfduid=d913ad3a0f661753201e8aa96d701220a1565078503; _pxhd=fb78a1cbe18850245c32c59d6859fc9a95dd7da449ee3b6b8a4aa901aa605e6b:6dcc2370-b820-11e9-bd8e-fd84f74899f8; cto_lwid=f677103e-dbb4-4f6a-9eb7-71ce859dc9ae; _ga=GA1.2.1094966298.1565078507; _gid=GA1.2.78797019.1565078507; _sp_ses.1a3e=*; _tl_csid=0199a79c-177d-45bc-a185-1aaaa9c8b0e8; _tl_duuid=a4272710-b8ed-461e-8317-7cff3525c493; _pk_ses.421.1a3e=*; _gcl_au=1.1.1265765900.1565078508; _ALGOLIA=anonymous-ead77991-05c7-414f-9428-e0ccf91749a3; stockx_session=fc0ajyzjbxzg1565078503372; _tl_auid=5d4933ec79802e0019362523; _tl_sid=5d4933ec79802e0019362528; tracker_device=6add66fd-700c-4b41-aafe-2b1040bc4a61; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22e7f4aa42-1283-4ea1-b1c0-243ab9116536%22; _omappvp=I7KwQ2BM6hsyFy62Mrj81LPkSH4LviDHX9zY2hal37e4uj222bJe48aTOePJEfBIjQy59KrTnYrWi4kYufcQgN9PPWMuqpMH; _fbp=fb.1.1565078510060.112687029; IR_gbd=stockx.com; stockx_seen_bid_new_info=true; rskxRunCookie=0; rCookie=yth6v9mnvoo8n6dk1jy1dtjyzjgjne; stockx_default_sneakers_size=9.5; lastRskxRun=1565081230457; is_gdpr=false; stockx_selected_currency=USD; stockx_selected_locale=US; stockx_product_visits=12; show_all_as_number=false; brand_tiles_version=v1; show_bid_education=v2; show_bid_education_times=1; multi_edit_option=beatLowestAskBy; product_page_v2=watches%2Chandbags; show_watch_modal=false; progress_bar_variant=; IR_9060=1565081432356%7C0%7C1565078510077%7C%7C; IR_PI=721f7830-b820-11e9-965d-42010a246302%7C1565167832356; stockx_homepage=sneakers; cookie_policy_accepted=true; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; _pk_id.421.1a3e=265bb26256e10d01.1565078507.1.1565081474.1565078507.; tl_sopts_0199a79c-177d-45bc-a185-1aaaa9c8b0e8_p_p_l_h=aHR0cHMlM0ElMkYlMkZzdG9ja3guY29tJTJGc2VhcmNoJTJGc25lYWtlcnMlM0ZzJTNEQ0Q2NTc4; tl_sopts_0199a79c-177d-45bc-a185-1aaaa9c8b0e8_p_p_l_t=U3RvY2tYJTNBJTIwQnV5JTIwYW5kJTIwU2VsbCUyMFNuZWFrZXJzJTJDJTIwU3RyZWV0d2VhciUyQyUyMEhhbmRiYWdzJTJDJTIwV2F0Y2hlcw==; tl_sopts_0199a79c-177d-45bc-a185-1aaaa9c8b0e8_p_p_l=JTdCJTIyaHJlZiUyMiUzQSUyMmh0dHBzJTNBJTJGJTJGc3RvY2t4LmNvbSUyRnNlYXJjaCUyRnNuZWFrZXJzJTNGcyUzRENENjU3OCUyMiUyQyUyMmhhc2glMjIlM0ElMjIlMjIlMkMlMjJzZWFyY2glMjIlM0ElMjIlM0ZzJTNEQ0Q2NTc4JTIyJTJDJTIyaG9zdCUyMiUzQSUyMnN0b2NreC5jb20lMjIlMkMlMjJwcm90b2NvbCUyMiUzQSUyMmh0dHBzJTNBJTIyJTJDJTIycGF0aG5hbWUlMjIlM0ElMjIlMkZzZWFyY2glMkZzbmVha2VycyUyMiUyQyUyMnRpdGxlJTIyJTNBJTIyU3RvY2tYJTNBJTIwQnV5JTIwYW5kJTIwU2VsbCUyMFNuZWFrZXJzJTJDJTIwU3RyZWV0d2VhciUyQyUyMEhhbmRiYWdzJTJDJTIwV2F0Y2hlcyUyMiU3RA==; tl_sopts_0199a79c-177d-45bc-a185-1aaaa9c8b0e8_p_p_v_d=MjAxOS0wOC0wNlQwOCUzQTUxJTNBMTQuMTE3Wg==; _sp_id.1a3e=09d2991e-4369-4b01-9107-1e0f6f01d1ad.1565078507.1.1565081475.1565078507.8fc4e013-e441-4309-99a8-5826bbb0a132',
            'jwt-authorization': 'false',
            'referer': 'https://stockx.com/search/sneakers?s={}'.format(stockx_sku),
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'x-anonymous-id': '09d2991e-4369-4b01-9107-1e0f6f01d1ad',
            'x-requested-with': 'XMLHttpRequest'
        }



    def Get_stockx_prodect_detal(self, detal_page_url):

        reql = requests.get(detal_page_url, headers=self.stockX_headers)

        detal_page_information = json.loads(reql.text)

        children_dict = detal_page_information['Product']['children']

        for i, j in children_dict.items():
            information_dict = {}
            information_dict['size'] = children_dict[i]['market']['lastSaleSize']                                                   #鞋码
            information_dict['lastSale'] = children_dict[i]['market']['lastSale']                                                   #最后报价
            information_dict['lowestAsk'] = children_dict[i]['market']['lowestAsk']                                             #最低售价
            information_dict['deadstockSold'] = children_dict[i]['market']['deadstockSold']                                     #销售量

            with open('StockXdata.json', 'a') as f:
                f.write(json.dumps(information_dict))




    def StockxHtml(self):
        reql = requests.get(self.stockx_url, headers=self.stockX_headers)

        stockx_json = json.loads(reql.text)

        if len(stockx_json['Products']) != 0:
            for i in stockx_json['Products']:
                if i['styleId'] == self.stockx_sku:
                    detal_page_url = 'https://stockx.com/api/products/' + str(i['shortDescription']) + '?includes=market,360&currency=USD'

                    self.Get_stockx_prodect_detal(detal_page_url)



if __name__=="__main__":
    StockX_Nice_spiders = StockX_Nice_spider('CD6578-006')
    StockX_Nice_spiders.StockxHtml()