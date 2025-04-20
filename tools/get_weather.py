# 获取天气
import requests
from config import EXTERNAL_TOOLS

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of an location, the user shoud supply a city name first",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名字, 应该为英文并且全部小写，例如：beijing",
                    }
                },
                "required": ["city"]
            },
        }
    },
]

def get_weather(city: str):
    weather_api = EXTERNAL_TOOLS["weather_api"]
    base_url = weather_api["url"]
    params = {
        "q": city,
        "appid": weather_api["key"],
        "units": "metric",  # 温度单位：metric(℃)/imperial(℉)
        "lang": "zh_cn"     # 中文输出
    }
    res = requests.get(base_url, params=params)
    
    if res.status_code == 200:
        data = res.json()
        return {
            "city": data["name"],
            "temperature": f"{data['main']['temp']}℃",
            "description": data["weather"][0]["description"],
            "humidity": f"{data['main']['humidity']}%"
        }
    else:
        return {"error": res.text}