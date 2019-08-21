#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

import requests, json

class goatspider():
    def __init__(self):

        self.search_url = "https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.25.1&x-algolia-application-id=2FWOTDVM2O&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a"


    def Get_json(self, sku):
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "Referer": "https://www.goat.com/search?query={}".format(sku),
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }

        data = {"params":"distinct=true&facetFilters=()&facets=%5B%22size%22%5D&hitsPerPage=20&numericFilters=%5B%5D&page=0&query={}&clickAnalytics=true".format(sku)}

        reql = requests.post(self.search_url, headers=headers, data=json.dumps(data))

        print(reql.text)


if __name__ == '__main__':
    Goat_spider = goatspider()
    Goat_spider.Get_json("CJ9219-001")