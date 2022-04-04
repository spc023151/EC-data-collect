# EC-data-collect
data backend engineer interview

### 商業需求
在電商平台的競爭上，需要瞭解其他電商在商品類別的訂價及貨運方式，以制定相關策略或活動，讓公司在販售商品上更具有競爭力。

### 功能範圍
1. 電商資訊爬蟲
2. 每週資料更新
3. API提供資料撈取服務

### 實作內容
* 1.資料取得
  * 爬蟲 - main/ruten_crawler.py
* 2.資料儲存
  * 關聯式資料庫 - PostgreSql
  * 資料表設計
* 3.資料處理
  * a. SQL
  * b. Pandas
* 4.服務應用
  * a. RESTful API 設計
  * b. 使用 FastAPI / Flask 實作
* 5.程式部署
  * a. Docker - main/dockerfile
* 6.程式碼管理
  * a. GitHub

### 實作流程  
> 1.資料取得
> > * 搜尋電商網頁其主要撈取資料之後端API，觀察其呼叫方式  
> > * 實作初步爬蟲並為準備未來擴充躲避封鎖ip及隨機user-agent功能擴充準備  
> > * 實作內容包含lv2、lv3類別代號、商品資訊、商品資訊來源爬蟲，lv1及頁數未實作(以單一類別及單頁爬蟲demo)  
> > * 資料簡單清理  
> >   
> > 總花費時間5小時  
> > ``` 花費大部分時間在觀察並測試其網頁API，最後找出可用的幾支 ```

> 2.資料儲存
> > * 架設關聯式資料庫PostgreSql  
> >     `pg_ctl start -D E:\PostgreSQL\14\data`
> > * 簡單資料表設計(for demo)  
> >   
> > 總花費時間3小時  
> > ``` 一開始對PostgreSql的Sql使用不熟，大寫需要用""包括 ```

> 3.程式部屬
> > * 架設Docker環境  
> > * 匯出Python環境  
> >     `pip freeze > requirement.txt`
> > * 使用dockerfile build爬蟲image  
> >     `docker build -t ruten .`
> > * 使用一次性container執行爬蟲程式並將資料存至PostgreSql  
> >     `docker run --net=host ruten`  
> >     
> > 總花費時間5小時  
> > ` docekr安裝於windows有非常多虛擬化設定要啟用，前置設定步驟多，打包時發生package找不到版本問題多次嘗試更改Python、套件版本才解決`

4.服務應用
> > * 簡單設計2種fastAPI以提供商品資料  
> >     1. 網頁帶入商品id回傳單一或多個商品資訊 /item/123456789,12354789  
> >     2. 帶參數回傳多個商品資訊 /item?offset=1&limit=10  
> >     
> > 總花費時間2小時  
> > `稍微瞭解fastAPI寫法即可使用unicorn掛上API服務`
