#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



from multiprocessing.dummy import Pool as ThreadPool
import requests, pymysql, random, redis
import datetime, time
import json
import re


class StockX_Nice_spider():

    def __init__(self):

        self.redis_client = redis.Redis(host='', port='', db=15, decode_responses=True, password='')

        self.comm_test_conn_du = pymysql.connect(
            host='',
            user="",
            password="",
            database="",
            charset='utf8'
        )

        self.mysql_cur = self.comm_test_conn_du.cursor()

        self.women_dict = {'5W': '35.5', '5.5W': '36', '6W': '36.5', '6.5W': '37.5', '7W': '38', '7.5W': '38.5', '8W': '39', '8.5W': '40', '9W': '40.5', '9.5W': '41', '10W': '42', '10.5W': '42.5', '11W': '43', '11.5W': '44', '12W': '44.5', '12.5W': '45', '13W': '45.5', '13.5W': '46', '14W': '47', '14.5W': '47.5', '15W': '48', '15.5W': '48.5', '16W': '49.5', '16.5W': '50.5', '17W': '51.5', '17.5W': '52.5'}

        self.child_dict = {'1Y': '32', '1.5Y': '33', '2Y': '33.5', '2.5Y': '34', '3Y': '35', '3.5Y': '35.5', '4Y': '36', '4.5Y': '36.5', '5Y': '37.5', '5.5Y': '38', '6Y': '38.5', '6.5Y': '39', '7Y': '40'}

        self.men_dict = {'3.5': '35.5', '4': '36', '4.5': '36.5', '5': '37.5', '5.5': '38', '6': '38.5', '6.5': '39', '7': '40', '7.5': '40.5', '8': '41', '8.5': '42', '9': '42.5', '9.5': '43', '10': '44', '10.5': '44.5', '11': '45', '11.5': '45.5', '12': '46', '12.5': '47', '13': '47.5', '13.5': '48', '14': '48.5', '15': '49.5', '16': '50.5', '17': '51.5', '18': '52.5'}

        self.exchange_rate_url = "https://api.jijinhao.com/plus/convert.htm?from_tkc=USD&to_tkc=CNY&amount=1&"

    def Get_stockx_prodect_detal(self, detal_page_url, stockX_headers, stockx_sku, proxy_list):

        bijia_conn_du = pymysql.connect(
            host='',
            user="",
            password="",
            database="",
            charset=''
        )

        comm_test_cur = bijia_conn_du.cursor()

        rate_reql = requests.get(self.exchange_rate_url)

        rate_reql.encoding = "utf-8"

        rate = float(re.findall("result = '(.*?)'", rate_reql.text)[0])

        now_time = datetime.datetime.now()
        dt_minus1day = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        dt_minus1day1 = (now_time + datetime.timedelta(days=-0)).strftime('%Y-%m-%d')

        proxy = random.choice(proxy_list)
        retry_flag = True
        retry_num = 10
        while retry_flag:

            try:
                reql = requests.get(detal_page_url, proxies=proxy, timeout=(2, 5), headers=stockX_headers)

                detal_page_information = json.loads(reql.text)

                children_dict = detal_page_information['Product']['children']
                product_masgion_list = []
                for i, j in children_dict.items():
                    information_dict = {}

                    information_dict['sku'] = stockx_sku

                    if 'W' in children_dict[i]['shoeSize'] and children_dict[i]['shoeSize'] in self.women_dict:
                        information_dict['size'] = self.women_dict[children_dict[i]['shoeSize']]

                    elif 'Y' in children_dict[i]['shoeSize'] and children_dict[i]['shoeSize'] in self.child_dict:
                        information_dict['size'] = self.child_dict[children_dict[i]['shoeSize']]

                    elif children_dict[i]['shoeSize'] in self.men_dict:
                        information_dict['size'] = self.men_dict[children_dict[i]['shoeSize']]  # 鞋码

                    else:
                        information_dict['size'] = children_dict[i]['shoeSize']

                    if "lastSale" in children_dict[i]['market']:
                        if children_dict[i]['market']['lastSale'] !=0:
                            information_dict['price'] = str(round(int(children_dict[i]['market']['lastSale']) * rate, 0) + 350)  # 最后报价
                        else:
                            information_dict['price'] = '0'
                    else:
                        information_dict['price'] = '0'

                    if "lowestAsk" in children_dict[i]['market']:
                        if children_dict[i]['market']['lowestAsk'] != 0:
                            information_dict['lowestAsk'] = str(round(int(children_dict[i]['market']['lowestAsk']) * rate, 0) + 350)  # 最低售价
                        else:
                            information_dict['lowestAsk'] = '0'
                    else:
                        information_dict['lowestAsk'] = 0

                    if "highestBid" in children_dict[i]['market']:
                        if children_dict[i]['market']['highestBid'] != 0:
                            information_dict['highestBid'] = str(round(int(children_dict[i]['market']['highestBid']) * rate, 0) + 350)  # 最高出价
                        else:
                            information_dict['highestBid'] = '0'
                    else:
                        information_dict['highestBid'] = 0

                    if "deadstockSold" in children_dict[i]['market']:
                        information_dict['deadstockSold'] = children_dict[i]['market']['deadstockSold']  # 销售量
                    else:
                        information_dict['deadstockSold'] = 0

                    yestoday_redis_key = '{},{},{},{},2'.format(dt_minus1day, stockx_sku, 'stockX', information_dict['size'])
                    today_redis_key = '{},{},{},{},2'.format(dt_minus1day1, stockx_sku, 'stockX', information_dict['size'])

                    yestoday_redis_values = self.redis_client.hget('Price_comparison', yestoday_redis_key)

                    if yestoday_redis_values:
                        information_dict['yesterdaylowestprice'] = yestoday_redis_values
                    else:
                        information_dict['yesterdaylowestprice'] = '0'

                    information_dict['aseriesof'] = "sneakers"

                    today_redis_values = self.redis_client.hget('Price_comparison', today_redis_key)

                    if today_redis_values is None or information_dict['price'] < today_redis_values:
                        self.redis_client.hset('Price_comparison', today_redis_key, information_dict['price'])

                    information_dict['desc'] = "现货"

                    information_dict['platform'] = 'stockX'

                    self.redis_client.hset('bijia', '{},{},{},2'.format(stockx_sku, 'stockX', information_dict['size']), str(information_dict))

                    product_masgion_list.append(information_dict)

                sql = """"""
                try:
                    comm_test_cur.execute(sql)
                    bijia_conn_du.commit()
                    comm_test_cur.close()
                    bijia_conn_du.close()

                except Exception as E:
                    print(sql)
                    print("插入失败：{}".format(E), stockx_sku)

                retry_flag = False

            except Exception as E:

                print("详情查询出错{}".format(E))
                if retry_num > 0:
                    retry_num -= 1
                    proxy = random.choice(proxy_list)
                    continue
                else:
                    break





    def StockxHtml(self, stockx_url, stockX_headers, stockx_sku, proxy_list):

        proxy = random.choice(proxy_list)
        retry_flag = True
        retry_num = 10

        while retry_flag:

            try:
                time.sleep(2)
                reql = requests.get(stockx_url, proxies=proxy, headers=stockX_headers, timeout=(2, 5))

                stockx_json = json.loads(reql.text)
                if len(stockx_json['hits']) != 0:
                    asdfs = True


                    for i in stockx_json['hits']:

                        stockx_shoe_sku = str(i['style_id']).strip().replace(' ', '-')

                        stock_flag = False
                        if stockx_shoe_sku == stockx_sku:
                            stock_flag = True
                        elif stockx_shoe_sku.upper() == stockx_sku:
                            stock_flag = True
                        elif stockx_shoe_sku.lower() == stockx_sku:
                            stock_flag = True

                        if stock_flag:

                            asdfs = False
                            detal_page_url = 'https://gateway.stockx.com/api/v2/products/{}?includes=market,360&currency=USD'.format(i['objectID'])

                            deail_headers = {
                                "method": "GET",
                                "scheme": "https",
                                "path": "/api/v2/products/{}?includes=market,360&currency=USD".format(i['objectID']),
                                "authority": "gateway.stockx.com",
                                "x-anonymous-id": "4f0789bd-bff5-4ab4-9b8a-21c585254bc0",
                                "accept": "*/*",
                                "app-version": "4.0.5.23735",
                                "app-platform": "ios",
                                "app-name": "StockX-iOS",
                                "jwt-authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdG9ja3guY29tIiwic3ViIjoic3RvY2t4LmNvbSIsImF1ZCI6IndlYiIsImFwcF9uYW1lIjoiaW9zIiwiYXBwX3ZlcnNpb24iOiI0LjAuNS4yMzczNSIsImlzc3VlZF9hdCI6IjIwMTktMDgtMjkgMDQ6MTk6MzIiLCJjdXN0b21lcl9pZCI6bnVsbCwiZW1haWwiOm51bGwsImN1c3RvbWVyX3V1aWQiOm51bGwsImZpcnN0TmFtZSI6bnVsbCwibGFzdE5hbWUiOm51bGwsImdkcHJfc3RhdHVzIjpudWxsLCJkZWZhdWx0X2N1cnJlbmN5IjoiVVNEIiwibGFuZ3VhZ2UiOiJlbi1VUyIsInNoaXBfYnlfZGF0ZSI6bnVsbCwidmFjYXRpb25fZGF0ZSI6bnVsbCwicHJvZHVjdF9jYXRlZ29yeSI6InNuZWFrZXJzIiwiaXNfYWRtaW4iOm51bGwsInNlc3Npb25faWQiOiIxMzE0NTM3MDY0Mzg4MTgwMDg4MyIsImV4cCI6MTU2NzY1NzE3MiwiYXBpX2tleXMiOm51bGx9.hWSIkP8_XAW5J6cIvpiiTwSJwvdnlkOoZB_d_pPbcgs",
                                "x-api-key": "99WtRZK6pS1Fqt8hXBfWq8BYQjErmwipa3a0hYxX",
                                "accept-language": "en-US",
                                "accept-encoding": "br, gzip, deflate",
                                "user-agent": "StockX/23735 CFNetwork/978.0.7 Darwin/18.6.0",
                                "cookie": "_pxhd=c0b39506451d309ff8db901d40782f7acd222f68b3bcb51bc6901e6e5452802a:5d701ee1-ca0f-11e9-a6a5-17af9d801013; __cfduid=d7facef0e5fe658ba57a7e1ace774b5011567050295",

                            }

                            self.Get_stockx_prodect_detal(detal_page_url, deail_headers, stockx_sku, proxy_list)

                    if asdfs:
                        print("没有相等的：", stockx_sku)

                else:
                    print("没有搜到: ", stockx_sku)

                retry_flag = False

            except Exception as E:
                print("搜索出错：{}".format(E), stockx_sku)
                if retry_num > 0:
                    retry_num -= 1
                    proxy = random.choice(proxy_list)
                    continue
                else:
                    break






    def executeSql(self, sql):
        try:
            self.mysql_cur.execute(sql)

            sku_tuples = self.mysql_cur.fetchall()

            sku_list = [i[0] for i in sku_tuples]

            return sku_list

        except Exception as E:
            print(E)




    def process(self, parameter):

        proxy_dict = self.redis_client.hgetall("proxy")

        proxy_list = []
        for key, val in proxy_dict.items():
            one_dict = {}
            one_dict["HTTPS"] = val
            proxy_list.append(one_dict)

        stockx_sku = parameter.strip()

        stockx_url = 'https://gateway.stockx.com/api/v2/search?facets=%5B%22product_category%22%5D&page=0&query={}&currency=USD'.format(stockx_sku)

        stockX_headers = {
            "method": "GET",
            "scheme": "https",
            "path": "/api/v2/search?facets=%5B%22product_category%22%5D&page=0&query={}&currency=USD".format(stockx_sku),
            "authority": "gateway.stockx.com",
            "x-anonymous-id": "4f0789bd-bff5-4ab4-9b8a-21c585254bc0",
            "accept": "*/*",
            "app-version": "4.0.5.23735",
            "app-platform": "ios",
            "app-name": "StockX-iOS",
            "jwt-authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdG9ja3guY29tIiwic3ViIjoic3RvY2t4LmNvbSIsImF1ZCI6IndlYiIsImFwcF9uYW1lIjoiaW9zIiwiYXBwX3ZlcnNpb24iOiI0LjAuNS4yMzczNSIsImlzc3VlZF9hdCI6IjIwMTktMDgtMjkgMDM6NDQ6NTUiLCJjdXN0b21lcl9pZCI6bnVsbCwiZW1haWwiOm51bGwsImN1c3RvbWVyX3V1aWQiOm51bGwsImZpcnN0TmFtZSI6bnVsbCwibGFzdE5hbWUiOm51bGwsImdkcHJfc3RhdHVzIjpudWxsLCJkZWZhdWx0X2N1cnJlbmN5IjoiVVNEIiwibGFuZ3VhZ2UiOiJlbi1VUyIsInNoaXBfYnlfZGF0ZSI6bnVsbCwidmFjYXRpb25fZGF0ZSI6bnVsbCwicHJvZHVjdF9jYXRlZ29yeSI6InNuZWFrZXJzIiwiaXNfYWRtaW4iOm51bGwsInNlc3Npb25faWQiOiIxMzE0NTM3MDY0Mzg4MTgwMDg4MyIsImV4cCI6MTU2NzY1NTA5NSwiYXBpX2tleXMiOm51bGx9.nNk34OIP7DJIuJ3CyDqfXY9-s4sJqInXfyNjVEZlz4w",
            "x-api-key": "99WtRZK6pS1Fqt8hXBfWq8BYQjErmwipa3a0hYxX",
            "accept-language": "en-US",
            "accept-encoding": "br, gzip, deflate",
            "user-agent": "StockX/23735 CFNetwork/978.0.7 Darwin/18.6.0",
            "cookie": "_pxhd=c0b39506451d309ff8db901d40782f7acd222f68b3bcb51bc6901e6e5452802a:5d701ee1-ca0f-11e9-a6a5-17af9d801013; __cfduid=d7facef0e5fe658ba57a7e1ace774b5011567050295"
        }

        self.StockxHtml(stockx_url, stockX_headers, stockx_sku, proxy_list)





    def main(self):

        sql = ""

        sku_list = self.executeSql(sql)

        pool = ThreadPool(10)

        print("****************************************开始执行for循环多线程函数****************************************")
        pool.map(self.process, sku_list)
        pool.close()
        pool.join()


        self.mysql_cur.close()
        self.comm_test_conn_du.close()





if __name__=="__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    startTime = time.time()
    StockX_Nice_spiders = StockX_Nice_spider()
    StockX_Nice_spiders.main()

    print("用时{}分钟".format(round((time.time() - startTime) / 60, 2)))



