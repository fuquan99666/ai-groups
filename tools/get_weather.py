# 获取天气
import requests
import gzip
import json
import csv
from io import BytesIO
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
                    "adm": {
                        "type": "string",
                        "description": "上一级行政单位"
                    },
                    "location_name": {
                        "type": "string",
                        "description": "城市名字, 应该为英文并且全部小写，例如：beijing"
                    },
                    "time":{
                        "type": "string",
                        "description": "想要知道天气的时间，如果是即时天气就是now，如果是未来几天的天气就是几d，比如未来三天就是3d"
                    },

                },
                "required": ["city","adm"]
            },
        }
    },
]

#这个没啥用了
def get_weather(city: str):
    base_url = ""
    
    headers = {
        "Authorization": ""
    }

    params = {
        "location_id":"101010100"  # 如果是location id，填101010100；如果是城市拼音，填 beijing
    }

    res = requests.get(base_url, params=params, headers=headers)
    print("返回内容：", res.text)

    if res.status_code == 200:
        if res.headers.get("Content-Encoding") == "gzip":
            buf = BytesIO(res.content)
            f = gzip.GzipFile(fileobj=buf)
            decompressed_data = f.read().decode("utf-8")
            data = json.loads(decompressed_data)
        else:
            data = res.json()

        # 和风天气返回的数据结构可能是 data["now"] 下有 temp、text 等字段
        return {
            "city": city,
            "temperature": f"{data['now']['temp']}℃",
            "description": data['now']['text'],
            "obs_time": data['now']['obsTime']
        }
    else:
        return {"error": res.text}