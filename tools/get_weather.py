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

                },
                "required": ["city","adm"]
            },
        }
    },
]

