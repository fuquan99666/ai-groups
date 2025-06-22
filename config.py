# config.py
import os
from dotenv import load_dotenv

# 自动加载环境变量
load_dotenv()  # 默认加载项目根目录的.env

# 敏感配置分离读取
# 安全配置中心化设定（建议写在独立配置文件 safety_config.py 中）
SAFETY_CONFIG = {
    # 敏感词汇库（支持多级分类管理）
    "sensitive_words": [
        # --- 政治敏感类 ---
        "领导人名字1", "领导人名字2", "六四", "法轮功",
        # --- 违法违规类 ---
        "冰毒", "摇头丸", "海洛因", "枪支代购",
        # --- 色情淫秽类 ---
        "成人影片", "约炮", "裸聊", "AV资源",
        # --- 暴恐血腥类 ---
        "ISIS", "人体炸弹", "斩首", "自制炸药"
    ],

    
    # 注入攻击防御正则表达式
    "injection_patterns": [
        # SQL 注入防御 (基础)
        r";\s*--",                     # 注释符攻击
        r"/\*.*?\*/",                  # SQL块注释
        r"\b(union|select|insert|delete|drop|update|alter)\b.*?\b(sql|db|table|database)\b",
        
        # XSS 跨站脚本防御
        r"<script.*?>.*?</script>",    # 基础脚本标签
        r"javascript:",                # JS协议执行
        r"on(error|submit|load)=",     # 事件处理器
        
        # 系统命令注入防御（示例）
        r"\b(ping|wget|curl|bash|sh)\s+.*?\b(127\.0\.0\.1|localhost)\b",
        
        # 路径穿越攻击防御
        r"\.\./|\.\.\\"                # 路径穿越符号
    ]
}



MODEL_CONFIG = {
    "deepseek-ai/DeepSeek-V3": {
        "api_key": os.getenv("OPENAI_API_KEY"),        # 从环境变量读取
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn"),  # 带默认值
        "stream": True
    },
}

EXTERNAL_TOOLS = {
    "weather_api": {
        "BASE_URL" :os.getenv("BASE_URL"),
        "CITY_URL" :os.getenv("CITY_URL"),
        "key": os.getenv("WEATHER_API_KEY")  ,
        "COUNTER_KEY": os.getenv("COUNTER_KEY"),
        "PROVE_KEY" :os.getenv("PROVE_KEY"),
        "PRIVATE_KEY_PATH" :"private.pem",
    }
}
