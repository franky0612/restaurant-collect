import googlemaps
import time
import pandas as pd

# 使用google map api(your_key為api使用金鑰,自行輸入)
gmaps = googlemaps.Client(key = your_key)
# 設定位置經緯度

loc = {'lat': 25.090143, 'lng': 121.534272}
newloc = {'lat': 0, 'lng': 0}

ids = []
results = []
    # Geocoding an address

#由於googlemap api 現在在搜索上有一筆最多60份的限制，因此將每次的搜索範圍縮小來取得較完整的資料

# 找出範圍內"restaurant"的googlemap搜尋結果
for i in range(52):#0.078
    newloc['lng'] = loc['lng'] + 0.0015*i
    for j in range(20):
        newloc['lat'] = loc['lat'] - 0.001*j
        query_result = gmaps.places_nearby(type="restaurant",location=newloc, radius=200)
        results.extend(query_result['results'])
        while query_result.get('next_page_token'):
                time.sleep(2)
                query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
                results.extend(query_result['results'])    
        print("找到的店家數量: "+str(len(results)))
        for place in results:
                ids.append(place['place_id'])


stores_info = []
# 去除重複id
ids = list(set(ids)) 
for id in ids:
    stores_info.append(gmaps.place(place_id=id, language='zh-TW')['result'])

#加入餐廳經緯度
output = pd.DataFrame.from_dict(stores_info)
output['lat'] = output['geometry'].map(lambda x: x['location']['lat'])
print("done")
output['lng'] = output['geometry'].map(lambda x: x['location']['lng'])
print("done")
output.to_csv('輸出位置')

