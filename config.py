# config.py
import os
from dotenv import load_dotenv

# 自动加载环境变量
load_dotenv()  # 默认加载项目根目录的.env

# 敏感配置分离读取
MODEL_CONFIG = {
    "gpt-3.5": {
        "api_key": os.getenv("OPENAI_API_KEY"),        # 从环境变量读取
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),  # 带默认值
        "stream": True
    },
    "qwen": {
        "api_key": os.getenv("QWEN_API_KEY"),
        "endpoint": os.getenv("QWEN_ENDPOINT")
    }
}

EXTERNAL_TOOLS = {
    "weather_api": {
        "url": "https://api.weatherapi.com/v1",
        "key": os.getenv("WEATHER_API_KEY")  # 安全读取第三方密钥
    }
}
