

import requests
from config import EXTERNAL_TOOLS as e
ex=e["weather_api"]

import datetime
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey



def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def generate_clean_jwt():
    # 加载私钥
    with open(ex["PRIVATE_KEY_PATH"], "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
        if not isinstance(private_key, Ed25519PrivateKey):
            raise TypeError("请使用 Ed25519 私钥")

    # header：不包含 typ
    header = {
        "alg": "EdDSA",
        "kid": ex["PROVE_KEY"],
    }

    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    payload = {
        "sub": ex["COUNTER_KEY"],
        "iat": now,
        "exp": now + 600
    }

    # base64url 编码 header 和 payload
    encoded_header = b64url(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = b64url(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{encoded_header}.{encoded_payload}".encode()

    # 签名
    signature = private_key.sign(signing_input)
    encoded_signature = b64url(signature)

    # 返回完整 token
    jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    return jwt_token

def get_weather(location_name="beijing", adm="北京"):

    token = generate_clean_jwt()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 第一步：城市名查 ID
    city_lookup_params = {
        "location": location_name,
        "adm": adm
    }

    res1 = requests.get(ex["CITY_URL"], headers=headers, params=city_lookup_params)
    city_data = res1.json()
    
    if city_data.get("code") != "200" or not city_data.get("location"):
        return {"error": "城市查询失败：" + city_data.get("code", "未知错误")}

    location_id = city_data["location"][0]["id"]
    print(f"📍 查到城市 ID：{location_id}")

    # 第二步：查询天气
    weather_params = {"location": location_id}
    res2 = requests.get(ex["BASE_URL"], headers=headers, params=weather_params)
    print("📦 天气响应：", res2.text)

    if res2.status_code == 200:
        return res2.json()
    else:
        return {"error": res2.text}

def tianqi(adm,location_name):
    print("📡 正在请求和风天气 API...")
    result = get_weather(location_name,adm)
    return result

if __name__ == "__main__":
    tianqi()
