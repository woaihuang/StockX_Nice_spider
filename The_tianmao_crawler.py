#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



import requests, re, json, html

from lxml import etree



class Tiammao():
    def __init__(self):
        self.headres = {
            'authority': 'detail.tmall.hk',
            'method': 'GET',
            'path': '/hk/item.htm?spm=a220m.1000858.1000725.45.326a17bdys4rb5&id=587655241391&skuId=4006080556098&user_id=2914266524&cat_id=2&is_b=1&rn=35a44bc9aff0a44a38b55c55df52f7fb',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'cq=ccp%3D1; t=da4a60fe8d1042b504db76d34842bf84; lid=%E9%BB%84%E6%B5%A9%E7%84%B6199223; tracknick=%5Cu9EC4%5Cu6D69%5Cu7136199223; enc=05%2FGP2b1%2Bx8qNkILo4bfMFcyvHw32gnnwhvN5bBDkjv%2FAdUPvInhXqaMMF1s%2B%2FWFfsSAasASGnifHYrV3QENag%3D%3D; cookie2=117ad6ecb3fdff22b7613400540015cb; _tb_token_=e99f8d33d3375; UM_distinctid=16c5a8465c554e-07f5f0aa04d1bc-1c396754-fa000-16c5a8465c656d; cna=IEjfFLhZLDsCAbZ1FpsPzi41; CNZZDATA1000427971=111007528-1564882085-https%253A%252F%252Flist.tmall.com%252F%7C1564887485; pnm_cku822=098%23E1hvFQvUvbpvUvCkvvvvvjiPRFF9tjrPPLcUQjrCPmP9sjYURLcpAjnVRFFv1jY8RphvCvvvvvvPvpvhvv2MMTyCvv9vvUv0VuX2CUyCvvOUvvVCa6VtvpvIvvvvk6CvvvvvvUUvphvhBvvv99CvpvAvvvmmvhCvmjwvvUUvphvUaQyCvhQhgiUvCATQD7zheTtYLrLWJX7rejh%2B%2BExr1EkKNoqBA47t%2B1wexb0l24VQRpn%2ByX79D40OaAuy%2BExr58tYVVzya4AAdcHvafmDYEeOvphvC9v9vvCvp8wCvvpvvUmm; isg=BLW1YHU5BDL2pWCO4UjFiSsvxDevmmgt8563djfacSx7DtUA_4J5FMOMWJKdVYH8; l=cBxCqZZHqUkOoWjbBOCanurza77OSIRYYuPzaNbMi_5C-6T6ed_Ok7kc8F96VjWd9H8B4wOSdj99-etXqWC8nydbHZ9R.',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1'
        }

        self.url = 'https://detail.tmall.hk/hk/item.htm?spm=a220m.1000858.1000725.45.326a17bdys4rb5&id=587655241391&skuId=4006080556098&user_id=2914266524&cat_id=2&is_b=1'



    def GetHtmlText(self):

        reql = requests.get(self.url, headers=self.headres)

        soup = etree.HTML(reql.text)

        title = str(soup.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[1]/h1')[0].text).strip().replace('\"', '')

        infomationJson = re.findall(r'TShop.Setup\((.*?)\);', html.unescape(reql.text), re.S)[0].strip().replace('\"', '\'')

        sizeJson = re.findall('\'skuList\':\[(.*?)\],\'defSelected\'', infomationJson)[0]

        sizelist = [i+'}' for i in str(sizeJson).split('}')]

        sizeList = [eval(i[1:]) if i[0] == ',' else eval(i) for i in sizelist if len(i)>1]

        sizeDict = {}
        for i in sizeList:
            sizeDict[i['skuId']] = re.findall('([\d+\.]+)', i['names'])[0]

        inventoryJson = re.findall('\'skuMap\':(.*?),\'salesProp\'', infomationJson)[0]

        inofrmationList = []
        for i, j in eval(inventoryJson).items():
            lastDict = {}
            lastDict['鞋款'] = title
            lastDict['鞋码'] = sizeDict[j['skuId']]
            lastDict['价格'] = j['price']
            lastDict['库存'] = j['stock']
            inofrmationList.append(lastDict)

        print(inofrmationList)



if __name__ == "__main__":
    tianmao = Tiammao()
    tianmao.GetHtmlText()

