import json
import math
import requests
import os

def lambda_handler(event, context):
    query = event["queryStringParameters"]

    target_lat = query["latitude"]
    target_lon = query["longtitude"]
    month = ("0" if (len(query["month"]) == 1) else "") + query["month"]
    day = ("0" if (len(query["day"]) == 1) else "") + query["day"]
    date = query["year"] + month + day

    closest_station = get_closest_station(target_lat, target_lon)

    weather_data = request_weather_data(closest_station, date)

    weather_status = get_weather_status(weather_data)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "weather-id": weather_status
        })
    }


def get_closest_station(latitude, longtitude):
    data = {
        "id": [108, 159, 143, 112, 156, 133, 152, 184],
        "name": ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "제주"],
        "lat": [37.5665, 35.1796, 35.8714, 37.4563, 35.1595, 36.3504, 35.539, 33.4996],
        "lon": [126.9780, 129.0756, 128.6014, 126.7052, 126.8526, 127.3845, 129.3114, 126.5312]
    }

    min_distance = float('inf')
    closest_station = None

    for i in range(len(data["id"])):
        station_id = data["id"][i]
        station_lat = data["lat"][i]
        station_lon = data["lon"][i]
        distance = haversine(latitude, longtitude, station_lat, station_lon)
        if distance < min_distance:
            min_distance = distance
            closest_station = station_id
    
    return closest_station


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구의 반지름 (킬로미터)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def request_weather_data(station, date):
    api_key = os.getenv("WEATHER_API_KEY") # AWS 환경 변수

    url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"

    params = {
        'serviceKey': api_key,
        'pageNo': '1',
        'numOfRows': '1',  # 필요한 데이터 수
        'dataType': 'JSON',  # JSON 형식으로 설정
        'dataCd': 'ASOS',  # 종관기상관측자료 코드
        'dateCd': 'DAY',  # 시간 단위 자료
        'startDt': date,  # 조회 시작 날짜
        'endDt': date,  # 조회 종료 날짜
        'stnIds': str(station)  # 서울의 기상관측소 ID
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None
    
    data = response.json()

    weather_data = data["body"]["items"]["item"][0]

    return weather_data


def get_weather_status(weather_data):
    # TODO weather_status를 weather_id로 줄 수 있도록
    if weather_data['avgTca'] <= 2 and weather_data['sumRn'] == 0:
        return "맑음"
    
    if weather_data['avgTca'] >= 8 and weather_data['sumRn'] == 0:
        return "흐림"
    
    if weather_data['sumRn'] > 0 and weather_data['avgTa'] > 0:
        return "비"
    
    if weather_data['sumRn'] > 0 and weather_data['avgTa'] <= 0:
        return "눈"
    
    if weather_data['maxInsWs'] >= 10:
        return "바람"
    
    if '황사' in weather_data['iscs']:
        return "황사"
    
    if weather_data['maxTa'] >= 35:
        return "폭염"
    
    if weather_data['minTa'] <= -10:
        return "한파"
    
    if '태풍' in weather_data['iscs'] and weather_data['maxInsWs'] >= 20:
        return "태풍"
    
    return "기타"