from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import sys

# 4小時
class crawler_info():

    def fake_user_agent(self):
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'

    def proxies(self):
        return None

class Ruten():
    
    crawler_info = crawler_info()
    
    fake_user_agent = crawler_info.fake_user_agent()
    
    proxies = crawler_info.proxies()
    headers = {'user-agent': fake_user_agent}
    
    def get_lv2_catg_list(self, catg):
        " return list of json "
        LV2_LEN = 4
        if(len(catg)!=LV2_LEN):
            raise Exception("lv1 catg length must be {}".format(LV2_LEN))
                    
        url = "https://rtapi.ruten.com.tw/api/cate/v1/index.php/cate/{}/cate".format(catg)
        
        html = requests.get(url, headers=self.headers, proxies=self.proxies)
        soup = BeautifulSoup(html.text, "lxml")
        result = soup.find("p").text
        result = json.loads(result)
        
        return result
    
    def get_lv3_catg_list(self, catg):
        " return list of json "
        LV3_LEN = 8
        if(len(catg)!=LV3_LEN):
            raise Exception("lv3 catg length must be {}".format(LV3_LEN))
        
        url = "https://rtapi.ruten.com.tw/api/cate/v1/index.php/cate/{}/cate".format(catg)
        
        html = requests.get(url, headers=self.headers, proxies=self.proxies)
        soup = BeautifulSoup(html.text, "lxml")
        result = soup.find("p").text
        result = json.loads(result)
        
        return result
    
    def get_item_by_lv3_catg(self, catg, p, limit=48):
        " return iteminfo list of json "
        def get_item_info_by_item_id(item_id, headers, proxies):
            url = "https://rtapi.ruten.com.tw/api/prod/v2/index.php/prod?id={}".format(",".join(item_id))
            html = requests.get(url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(html.text, "lxml")
            result = soup.find("p").text
            result = json.loads(result)

            return result
    
        url = "https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?type=direct&cateid={}&sort=rnk%2Fdc&limit={}&offset={}".format(catg, limit, 1+(int(p)-1)*limit)
        self.headers["referer"] = "https://www.ruten.com.tw/category/{}/list?p={}".format(catg, p)
        
        html = requests.get(url, headers=self.headers, proxies=self.proxies)
        soup = BeautifulSoup(html.text, "lxml")
        item = soup.find("p").text
        item = json.loads(item)
        
        item_id = [item_id["Id"] for item_id in item["Rows"]]
        
        result = get_item_info_by_item_id(item_id, self.headers, self.proxies)
        
        return result

if __name__=='__main__':

    catg = sys.argv[1]
    p = sys.argv[2]
    passwd = sys.argv[3]
    dbhost = sys.argv[4] # localhost

    ruten = Ruten()

    lv2_list = ruten.get_lv2_catg_list(catg)
    lv3_list = ruten.get_lv3_catg_list(lv2_list[0]["Id"])

    item = ruten.get_item_by_lv3_catg(lv3_list[0]["Id"], p=p)

    df = pd.DataFrame(item)
    df["PriceRange1"] = df["PriceRange"].apply(lambda x:x[0])
    df["PriceRange2"] = df["PriceRange"].apply(lambda x:x[1])
    df["SourceInfo"] = df["SourceInfo"].apply(lambda x:{} if x==None else x)
    df["Translate"] = df["Translate"].apply(lambda x:{} if x==None else x)

    df2 = pd.DataFrame(list(df["SourceInfo"]))
    df2["ProdId"] = df["ProdId"]
    df2 = df2.dropna()
    df2 = df2.rename(columns={"Source":"SourceFrom"})

    del df["SourceInfo"]
    del df["PriceRange"]
    del df["Translate"]

    engine = create_engine('postgresql://postgres:{}@{}:5432/ruten'.format(passwd, dbhost))

    df.to_sql("iten_detail", engine, index=False, if_exists="replace")
    df2.to_sql("othersource", engine, index=False, if_exists="replace")





