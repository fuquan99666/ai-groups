# 全局配置
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 模型配置
MODEL_CONFIG = {
    "deepseek-ai/DeepSeek-V3": {
        "api_key": os.getenv("OPENAI_API_KEY"),        # 从环境变量读取
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn"),  # 带默认值
        "stream": True
    },
}

# 安全配置 - 用于输入处理
SAFETY_CONFIG = {
    # 敏感词列表
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
    # 指令注入防护关键词
    "injection_keywords" : [
    # 原始列表中的关键词
    "!system",
    "!function_call",
    "<|FunctionCallBegin|>",
    "<|FunctionCallEnd|>",

    # SQL 注入相关
    "UNION ALL SELECT",
    "DROP TABLE",
    "ALTER TABLE",
    "TRUNCATE TABLE",
    "INSERT INTO",
    "UPDATE ... SET",
    "DELETE FROM",

    # 命令注入相关
    "|",  # 管道符，用于命令拼接
    ";",  # 分号，用于多条命令执行
    "&&",
    "||",
    "`",  # 反引号，用于命令替换
    "$(",  # 命令替换

    # XSS 相关
    "<iframe",
    "<img src=x onerror",
    "<body onload",
    "<script src=",
    "javascript:",
    "data:text/html;base64,",

    # 代码注入相关
    "__import__",  # Python 导入模块
    "eval(",
    "exec(",
    "system(",  # 可能用于执行系统命令
    "shell_exec(",

    # 其他可能的恶意关键词
    "sudo",  # 提升权限
    "rm -rf",  # 危险的文件删除命令
    "wget",
    "curl",
    "nc",  # 网络工具
    "ssh",
    "python -c",  # 执行 Python 代码
    "bash -c",  # 执行 Bash 代码
    "powershell -Command",  # Windows PowerShell 命令执行
],
    # 输入长度限制
    "max_input_length": 2000,
}

# 工具配置
TOOL_CONFIG = {
    "enabled": True,
    "available_tools": [
        {
            "name": "get_weather",
            "parameters": {
                "location": {"type": "string", "description": "城市名称，如北京"},
                "date": {"type": "string", "description": "日期，格式YYYY-MM-DD，默认为今天"}
            },
            "description": "获取指定城市和日期的天气信息"
        },
    ]
}

# 流式输出配置
STREAM_CONFIG = {
    "enabled": True,
    "chunk_size": 5,  # 每次输出的字符数
    "delay": 0.05,    # 输出延迟(秒)
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