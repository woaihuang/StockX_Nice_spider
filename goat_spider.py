#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-




import requests, json, re



class The_Goat_Spider():
    def __init__(self):
        self.Home_page_url = "https://2fwotdvm2o-1.algolianet.com/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.25.1&x-algolia-application-id=2FWOTDVM2O&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a"

        self.headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "Referer": "https://www.goat.com/sneakers",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }



    def Getproductjson(self, skip_links):
        reql_json = requests.get(skip_links, headers=self.headers)

        productJson = re.findall('window.__context__ = (.*?)</script>', reql_json.text, re.S)[0]

        return json.loads(productJson)



    def GetJsonMsg(self, pageNum):
        skip_links_list = []

        data = {"params": "distinct=true&facetFilters=()&facets=%5B%22size%22%5D&hitsPerPage=20&numericFilters=%5B%5D&page={}&query=&clickAnalytics=true".format(pageNum)}

        reql_json = requests.post(self.Home_page_url, data=json.dumps(data), headers=self.headers)

        reql_dict = json.loads(reql_json.text)

        for product_num in range(len(reql_dict['hits'])):
            slug_skip_list = []

            Skip_links = "https://www.goat.com/sneakers/{}".format(reql_dict['hits'][product_num]['slug'])
            slug_skip_list.append(reql_dict['hits'][product_num]['slug'])
            slug_skip_list.append(Skip_links)

            skip_links_list.append(slug_skip_list)

        return skip_links_list



    def Get_product_msg(self, pageNum):
        skip_links_list = self.GetJsonMsg(pageNum)

        for skip_links in skip_links_list:
            even_shoe_size_list = []

            reql_dict = self.Getproductjson(skip_links[1])

            product_msg_dict = reql_dict['default_store']['product-templates']['slug_map'][skip_links[0]]

            productid = product_msg_dict['id']                                                     #商品唯一ID，数据库去重主键

            sku = product_msg_dict['sku']                                                          #商品sku

            Skip_links = "https://www.goat.com/sneakers/{}".format(product_msg_dict['slug'])       #详情页链接

            product_name = product_msg_dict['name']                                                #商品名

            product_color = product_msg_dict['color']                                              #颜色

            new_lowest_price = int(product_msg_dict['new_lowest_price_cents'])/100                 #新鞋最低价

            used_lowest_price = int(product_msg_dict['used_lowest_price_cents'])/100               #二手鞋价格

            for shoe_size_price in product_msg_dict['formatted_available_sizes_new_v2']:
                shoe_size_price_dict = {}

                shoe_size_price_dict[shoe_size_price['size']] = int(shoe_size_price['price_cents'])/100

                even_shoe_size_list.append(shoe_size_price_dict)                                   #每个鞋码所对应的价格列表

            product_sex = product_msg_dict['gender'][0]                                            #性别





    def main(self, pageNum):
        self.Get_product_msg(pageNum)




if __name__=="__main__":
    Goat_spider = The_Goat_Spider()

    for pageNum in range(1000):
        Goat_spider.main(pageNum)
