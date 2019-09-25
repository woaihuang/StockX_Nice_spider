#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-


from multiprocessing.dummy import Pool as ThreadPool
import requests, pymysql, redis, random
import hashlib, json, time
import datetime




class UpdateDu():
    def __init__(self):

        self.redis_client = redis.Redis(host='', port=6379, db=15, decode_responses=True, password='')

        self.comm_test_conn_du = pymysql.connect(
            host='',
            user="",
            password="",
            database="",
            charset='utf8'
        )

        self.comm_test_cur_du = self.comm_test_conn_du.cursor()

        self.url = 'https://m.poizon.com/search/list?lastId=&limit=20&loginToken=1a2e9b23%7C26466816%7Cc46da178392ab6b1&mode=0&newSign=6952339b9d03a9c6b4e9042a1aa3f1b7&page=0&platform=iPhone&sign=73d0717694e9132058a1b7cf811a31b7&sortMode=1&sortType=0&timestamp={}&title={}&token=JLIjsdLjfsdII%253D%257CMTQxODg3MDczNA%253D%253D%257C07aaal32795abdeff41cc9633329932195&uuid=70840D3C-1B0C-4160-973D-E8D086A1D6C0&v=3.5.7'


        self.headers = {
            "method": "GET",
            "scheme": "https",
            "path": "/api/v1/app/search/ice/search/list?lastId=&limit=20&loginToken=1a2e9b23%7C26466816%7Cc46da178392ab6b1&mode=0&newSign=ab537a29934cdb05615358881fd39ac3&page=0&platform=iPhone&showHot=1&shumeiid=201907191555387e8308983c4e44e01935a91d5e49613701c35750767d11ea&sign=f5b18309decd44b2ea8772ff3d21718c&sortMode=1&sortType=0&timestamp=1566869462123&title=CP9366&token=JLIjsdLjfsdII%253D%257CMTQxODg3MDczNA%253D%253D%257C07aaal32795abdeff41cc9633329932195&uuid=UUIDf58708e26dc347c696cefcd8f687842e&v=4.11.0",
            "authority": "app.poizon.com",
            "uuid": "UUIDf58708e26dc347c696cefcd8f687842e",
            "accept": "*/*",
            "timestamp": "1566869462123",
            "shumeiid": "201907191555387e8308983c4e44e01935a91d5e49613701c35750767d11ea",
            "accept-language": "zh-Hans-CN;q=1.0",
            "accept-encoding": "gzip;q=1.0, compress;q=0.5",
            "token": "JLIjsdLjfsdII%3D%7CMTQxODg3MDczNA%3D%3D%7C07aaal32795abdeff41cc9633329932195",
            "mode": "0",
            "platform": "iPhone",
            "user-agent": "duapp/4.11.0 (com.siwuai.duapp; build:4.11.0.0; iOS 12.3.1) Alamofire/4.8.2",
            "logintoken": "1a2e9b23|26466816|c46da178392ab6b1",
            "v": "4.11.0",
            "cookie": "duToken=d41d8cd9%7C26466816%7C1547193362%7C892ff904a177d054"
        }


    def GetShoeId(self, sku, proxy_list):

        proxy = random.choice(proxy_list)

        IdList, title, retry_flag, retry_num = [], '', True, 10

        while retry_flag:

            try:
                reql = requests.get(self.url.format(time.time() * 100, str(sku).strip()), headers=self.headers, timeout=(2, 5), proxies=proxy)

                myjson = json.loads(reql.text)  # data是向 api请求的响应数据，data必须是字符串类型的


                newjson = json.dumps(myjson, ensure_ascii=False)  # ensure_ascii=False 就不会用 ASCII 编码，中文就可以正常显示了

                last_json = json.loads(newjson)  # 最后的字典数据

                title1list = last_json['data']['productList']

                for i in range(len(title1list)):
                    IdList.append(title1list[i]['productId'])

                return IdList

            except Exception as E:
                print("搜索出错：{}".format(E), sku)
                if retry_num > 0:
                    retry_num -= 1
                    proxy = random.choice(proxy_list)
                    continue
                else:
                    break



    def createdata(self, Sku, proxy_list):

        bijia_conn_du = pymysql.connect(
            host='',
            user="",
            password="",
            database="",
            charset='utf8'
        )

        bijia_cur = bijia_conn_du.cursor()

        IdList = self.GetShoeId(Sku, proxy_list)

        proxy = random.choice(proxy_list)

        now_time = datetime.datetime.now()
        dt_minus1day = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        dt_minus1day1 = (now_time + datetime.timedelta(days=-0)).strftime('%Y-%m-%d')

        for i in IdList:
            try:
                aflag = False
                sign = 'productId' + '{}'.format(int(i)) + 'sourceshareDetail' + '048a9c4943398714b356a696503d2d36'

                hashm2 = hashlib.md5()

                hashm2.update(sign.encode('utf8'))

                newsign = hashm2.hexdigest()


                newurl = 'https://m.poizon.com/mapi/product/detail?productId={}&source=shareDetail&sign={}'.format(int(i), newsign)

                reql = requests.get(newurl, headers=self.headers, timeout=(2, 5), proxies=proxy)

                myjson = json.loads(reql.text)  # data是向 api请求的响应数据，data必须是字符串类型的

                newjson = json.dumps(myjson, ensure_ascii=False)  # ensure_ascii=False 就不会用 ASCII 编码，中文就可以正常显示了

                last_json = json.loads(newjson)  # 最后的字典数据

                if type(last_json['data']['item']) is dict:

                    sku = last_json['data']['item']['product']['articleNumber'].strip().replace(' ', '-')

                    if sku == Sku:
                        aflag = True

                    elif sku.upper() == Sku:
                        aflag = True

                    elif sku.lower() == Sku:
                        aflag = True

                    if aflag == True:

                        product_masgion_list = []
                        for sku_list in last_json['data']['sizeList']:
                            information_dict = {}
                            information_dict['sku'] = sku
                            information_dict['size'] = str(sku_list['size'])  # 鞋码
                            if len(sku_list['item']) != 0:
                                information_dict['deadstockSold'] = str(sku_list['item']['product']['soldNum'])  # 销售量
                                information_dict['price'] = str(sku_list['item']['price'])[:-2]  # 价格

                            else:
                                information_dict['deadstockSold'] = '0'
                                information_dict['price'] = '0'

                            information_dict['lowestAsk'] = '0'
                            information_dict['highestBid'] = '0'
                            information_dict['desc'] = '现货'
                            information_dict['aseriesof'] = "sneakers"

                            yestoday_redis_key = '{},{},{},{},2'.format(dt_minus1day, sku, 'du', information_dict['size'])
                            today_redis_key = '{},{},{},{},2'.format(dt_minus1day1, sku, 'du', information_dict['size'])

                            yestoday_redis_values = self.redis_client.hget('Price_comparison', yestoday_redis_key)

                            if yestoday_redis_values:
                                information_dict['yesterdaylowestprice'] = yestoday_redis_values
                            else:
                                information_dict['yesterdaylowestprice'] = '0'

                            information_dict['aseriesof'] = "sneakers"

                            information_dict['platform'] = '毒'

                            today_redis_values = self.redis_client.hget('Price_comparison', today_redis_key)

                            if today_redis_values is None or information_dict['price'] < today_redis_values:
                                self.redis_client.hset('Price_comparison', today_redis_key, information_dict['price'])

                            self.redis_client.hset('bijia', '{},{},{},2'.format(sku, 'du', information_dict['size']), str(information_dict))

                            product_masgion_list.append(information_dict)

                        sql = """"""

                        try:
                            bijia_cur.execute(sql)
                            bijia_conn_du.commit()
                            bijia_cur.close()
                            bijia_conn_du.close()


                        except Exception as E:
                            print("插入失败：{}".format(E), sku)

                        break

            except Exception as F:
                print("错误：{}".format(F))




    def executeSql(self, sql):
        try:
            self.comm_test_cur_du.execute(sql)

            sku_tuples = self.comm_test_cur_du.fetchall()

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

        self.createdata(parameter, proxy_list)





    def main(self):

        sql = ""

        sku_list = self.executeSql(sql)

        pool = ThreadPool(10)

        print("****************************************开始执行for循环多线程函数****************************************")
        pool.map(self.process, sku_list)
        pool.close()
        pool.join()

        self.comm_test_cur_du.close()
        self.comm_test_conn_du.close()







if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    startTime = time.time()
    a = UpdateDu()
    a.main()
    print("用时{}分钟".format(round((time.time() - startTime) / 60, 2)))





