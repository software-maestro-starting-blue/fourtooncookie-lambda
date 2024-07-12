import json
import math
import requests
import os

def lambda_handler(event, context):

    try:
        query = event["queryStringParameters"]

        target_lat = float(query["latitude"])
        target_lon = float(query["longtitude"])
        month = ("0" if (len(query["month"]) == 1) else "") + query["month"]
        day = ("0" if (len(query["day"]) == 1) else "") + query["day"]
        date = query["year"] + month + day
    except:
        return {
            'statusCode': 400,
            'body': json.dumps("요청 인자가 잘 못 되었습니다.")
        }

    closest_station = get_closest_station(target_lat, target_lon)

    weather_data = request_weather_data(closest_station, date)

    if weather_data == None:
        return {
            'statusCode': 500,
            'body': json.dumps("날씨 정보를 받아올 수 없습니다.")
        }

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

    url = "https://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"

    params = {
        "serviceKey": api_key,
        "pageNo": "1",
        "numOfRows": "10",  # 필요한 데이터 수
        "dataType": "JSON",  # JSON 형식으로 설정
        "dataCd": "ASOS",  # 종관기상관측자료 코드
        "dateCd": "DAY",  # 시간 단위 자료
        "startDt": date,  # 조회 시작 날짜
        "endDt": date,  # 조회 종료 날짜
        "stnIds": str(station)  # 기상관측소 ID
    }

    back = ""

    for k, v in params.items():
        back += k + "=" + v + "&"
    
    back = back[:-1]

    response = requests.get(url + "?" + back)

    if response.status_code != 200:
        return None
    
    data = response.json()

    try:
        weather_data = data["response"]["body"]["items"]["item"][0]
        return weather_data
    except:
        return None


def convert_to_float(value, default=0.0):
    try:
        return float(value)
    except ValueError:
        return default


def get_weather_status(weather_data):
    # TODO weather_status를 weather_id로 줄 수 있도록
    avgTca = convert_to_float(weather_data.get('avgTca', '0'))
    sumRn = convert_to_float(weather_data.get('sumRn', '0'))
    avgTa = convert_to_float(weather_data.get('avgTa', '0'))
    maxInsWs = convert_to_float(weather_data.get('maxInsWs', '0'))
    maxTa = convert_to_float(weather_data.get('maxTa', '0'))
    minTa = convert_to_float(weather_data.get('minTa', '0'))
    iscs = weather_data.get('iscs', '')

    if avgTca <= 2 and sumRn == 0:
        return "clear"

    if avgTca >= 8 and sumRn == 0:
        return "cloudy"

    if sumRn > 0 and avgTa > 0:
        return "rain"

    if sumRn > 0 and avgTa <= 0:
        return "snow"

    if maxInsWs >= 10:
        return "wind"

    if '황사' in iscs:
        return "yellow dust"

    if maxTa >= 35:
        return "hot"

    if minTa <= -10:
        return "cold"

    if '태풍' in iscs and maxInsWs >= 20:
        return "typhoon"

    return "other"