import re
from typing import List, Dict, Any
from config import SAFETY_CONFIG

def preprocess_input(user_input: str, tools: List[Dict[str, Any]] = None) -> str:
    """
    对用户输入进行预处理，包括敏感词过滤和指令注入防护
    
    Args:
        user_input: 用户输入的内容
        tools: 可用工具列表，用于工具调用验证
        
    Returns:
        处理后的安全输入
    """
    # 步骤1: 敏感词过滤
    safe_input = filter_sensitive_words(user_input)
    
    # 步骤2: 指令注入防护
    safe_input = prevent_injection(safe_input)
    
    # 步骤3: 工具调用验证（如果有工具）
    if tools:
        safe_input = validate_tool_call(safe_input, tools)
    
    return safe_input

def filter_sensitive_words(text: str) -> str:
    """
    过滤敏感词，替换为*
    
    Args:
        text: 待过滤的文本
        
    Returns:
        过滤后的文本
    """
    # 从配置中获取敏感词列表
    sensitive_words = SAFETY_CONFIG.get("sensitive_words", [])
    
    # 使用正则表达式替换敏感词
    for word in sensitive_words:
        text = re.sub(re.escape(word), '*' * len(word), text, flags=re.IGNORECASE)
    
    return text

def prevent_injection(text: str) -> str:
    """
    防止指令注入攻击
    
    Args:
        text: 待处理的文本
        
    Returns:
        处理后的安全文本
    """
    # 从配置中获取注入关键词列表
    injection_keywords = SAFETY_CONFIG.get("injection_keywords", [])
    
    # 检查并移除注入关键词
    for keyword in injection_keywords:
        text = re.sub(re.escape(keyword), '', text, flags=re.IGNORECASE)
    
    # 额外防护：限制特殊字符连续出现次数
    text = re.sub(r'([!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~])\1{3,}', r'\1\1', text)
    
    return text

def validate_tool_call(text: str, tools: List[Dict[str, Any]]) -> str:
    """
    验证工具调用格式是否合法
    
    Args:
        text: 待验证的文本
        tools: 可用工具列表
        
    Returns:
        验证后的文本
    """
    # 工具调用格式: [TOOL]tool_name[PARAMS]param1=value1&param2=value2[/TOOL]
    tool_pattern = r'\[TOOL\](.*?)\[PARAMS\](.*?)\[/TOOL\]'
    
    # 检查是否有工具调用
    if not re.search(tool_pattern, text):
        return text
    
    # 验证每个工具调用
    def replace_tool(match):
        tool_name = match.group(1).strip()
        params = match.group(2).strip()
        
        # 检查工具是否存在
        tool_exists = any(tool.get("name") == tool_name for tool in tools)
        if not tool_exists:
            return f"[非法工具调用: {tool_name}]"
        
        # 验证参数格式 (简化版)
        if not all('=' in param for param in params.split('&') if param):
            return f"[非法参数格式: {params}]"
        
        return match.group(0)
    
    # 替换非法工具调用
    return re.sub(tool_pattern, replace_tool, text)    
