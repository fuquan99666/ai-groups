import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_weather_func(location: str) -> str:
    """
    获取指定地点的专业天气信息
    参数:
        location (str): 地点名称，如"山东烟台"
    返回:
        str: 格式化后的专业天气信息
    """
    # 配置请求头（模拟浏览器）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    
    try:
        # Step 1. 发起百度搜索请求
        query = f"{location} 天气"
        url = f"https://www.baidu.com/s?wd={quote(query)}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Step 2. 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        def safe_extract(element, selector, attribute="text"):
            found = element.select_one(selector)
            if not found: return "N/A"
            return found.get_text().strip() if attribute == "text" else found.get(attribute, "N/A")
        
        # 定位专业天气指数区域
        profession_section = soup.select_one(".profession_5Z1LF.pc_Al2N0")
        if not profession_section:
            return f"未找到{location}的专业天气指数卡片，请检查城市名或页面结构是否变化"
        
        # 提取专业天气指数数据
        indices_data = {
            "feels_like": {
                "value": safe_extract(profession_section, ".box-item_4dDrB .content-num_mjUkj"),
                "description": safe_extract(profession_section, ".box-item_4dDrB rich-text span", "text")
            },
            "uv_index": {
                "level": safe_extract(profession_section, ".contentbox_1D4Mz.no-num_iJQjL .content-text_3tR6g"),
                "description": safe_extract(profession_section, ".contentbox_1D4Mz.no-num_iJQjL + rich-text span", "text")
            },
            "humidity": {
                "value": safe_extract(profession_section, ".contentbox_1D4Mz .content-num_mjUkj:nth-of-type(1)"),
                "description": safe_extract(profession_section, ".contentbox_1D4Mz + rich-text span", "text")
            },
            "precipitation": {
                "value": safe_extract(profession_section, "div.box-item_4dDrB:has(> div:contains('降水量')) .content-num_mjUkj") + "毫米",
                "description": safe_extract(profession_section, "div.box-item_4dDrB:has(> div:contains('降水量')) + rich-text span", "text")
            }
        }
        
        # 提取日出日落信息
        sun_data = {
            "sunrise": safe_extract(profession_section, ".time-box_7HzyG .time_3p7ft.num_3De1N"),
            "sunset": safe_extract(profession_section, ".right-text_5FdgQ .time_3p7ft.num_3De1N")
        }
        
        # Step 4. 组织输出格式
        output = [
            f"{location} 专业天气指数报告",
            "----------------------------",
            f"🌡️ 体感温度: {indices_data['feels_like']['value']} ({indices_data['feels_like']['description']})",
            f"☀️ 紫外线指数: {indices_data['uv_index']['level']} ({indices_data['uv_index']['description']})",
            f"💦 湿度: {indices_data['humidity']['value']} ({indices_data['humidity']['description']})",
            f"🌧️ 降水量: {indices_data['precipitation']['value']} ({indices_data['precipitation']['description']})",
            f"🌅 日出时间: {sun_data['sunrise']}",
            f"🌇 日落时间: {sun_data['sunset']}"
        ]
        
        return "\n".join(output)
        
    except Exception as e:
        return f"天气查询失败：{str(e)}"