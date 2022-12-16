# -*- coding: utf-8 -*-
"""a.ipynb의 사본

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AI_b62EONdsy5ezLqDRHXb3-_MRCSz70
"""

#네이버 api와 주소에서 위도, 경도를 이용하기 위한 라이브러리 설치
!pip install PyNaver
!pip install geopy

import pandas as pd
import folium
import webbrowser
import json
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from folium.plugins import MarkerCluster
from folium.plugins import MiniMap

#데이터로 이용할 csv파일 확인 및 최소화
file = '서울시 공중화장실 위치정보.csv'
orgdata = pd.read_csv(file, encoding = 'cp949')

orgdata=orgdata.rename(columns={'WSG84X좌표':'경도','WSG84Y좌표':'위도'})

for i in range(len(orgdata)):
    
    lat = orgdata.loc[i, '위도']
    long = orgdata.loc[i, '경도']
    region = orgdata.loc[i, '대명칭']
    
orgdata.head()

dir_client_id = 'xsnyon27l3'
dir_client_secret = '1IwY2M3lxQN2rBV4z5JfS4nOqaTFL2vJWIPZspqT'

url = f'https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving'

start = ''
goal =  ''
headers = {'X-NCP-APIGW-API-KEY-ID':dir_client_id, 'X-NCP-APIGW-API-KEY': dir_client_secret}

#원하는 주소 입력
from geopy.geocoders import Nominatim

def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd
user =  input('주소를 입력하세요.')
crd = geocoding(user)
print(crd['lat'])
print(crd['lng'])

#data에서 필요한 속성만 가져오기
data = orgdata[['대명칭', '위도', '경도']]

mycrd = (crd['lat'],crd['lng'])
dist=[]
for n in data.index:
    t_loc = (data.loc[n, '위도'],data.loc[n, '경도'])     
    #print(geodesic(mycrd,t_loc).kilometers)
    dist.append(geodesic(mycrd,t_loc).kilometers)
dist[:10]
data['거리']=dist
data

# 7. 사용자 주소와 가장 가까운 공중화장실 상위 10곳 구하기
neardata = data.sort_values(by=['거리']).head(10)

neardata['위도'].mean(), neardata['경도'].mean()

# 8. 지도 준비
w_map = folium.Map(location=[neardata['위도'].mean(), neardata['경도'].mean()], zoom_start=14)

# 9. 사용자 주소와 상위 10곳의 공중화장실 마커 올리기
folium.Marker([crd['lat'], crd['lng']], 
    icon=folium.Icon(color='red', icon='glyphicon glyphicon-home')).add_to(w_map)

nearlist=[]
# 10. 지도에 popup을 이용해 마커를 클릭시 해당 마커에 대명칭을 표시
for n in neardata.index:
    folium.Marker([neardata.loc[n, '위도'], neardata.loc[n, '경도']],
                  popup = neardata.loc[n, '대명칭'],
                           icon=folium.Icon(color='blue',icon='flag'
                 ,prefix='fa')).add_to(w_map)
  
    nearlist.append([neardata.loc[n, '위도'], neardata.loc[n, '경도']])
#folium.PolyLine(locations=(crd['lat'], crd['lng']),tooltip='Polyline').add_to(w_map)

w_map

#네이버 api id
#x-ncp-apigw-api-key-id:{xsnyon2713}
#x-ncp-apigw-api-key:{1IwY2M3lxQN2rBV4z5JfS4nOqaTFL2vJWIPZspqT}

neardata
mycrd
from PyNaver import NaverCloudPlatform
client_id = "xsnyon27l3"
client_secret = "1IwY2M3lxQN2rBV4z5JfS4nOqaTFL2vJWIPZspqT"

# 네이버 API 인스턴스 생성
ncp = NaverCloudPlatform(client_id, client_secret)
#start = "127.1115061,37.3864539"
#goal = "127.01953476,37.5160802"
start = f"{mycrd[0]},{mycrd[1]}"
goal = f"{nearlist[0]},{nearlist[1]}"
# 실행
res = ncp.directions15(start=start, goal=goal, )
res