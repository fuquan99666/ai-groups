import re

from config import SAFETY_CONFIG

def preprocess_input(text: str) -> str:
    """输入预处理"""
    text = filter_sensitive_words(text)
    text = prevent_injection(text)
    return text

def filter_sensitive_words(text: str) -> str:
    for word in SAFETY_CONFIG["sensitive_words"]:
        text = text.replace(word, "***")
    return text

def prevent_injection(text: str) -> str:
    injection_keywords = [
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
    ]
    for keyword in injection_keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub("", text)
    for pattern in SAFETY_CONFIG["injection_patterns"]:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text
