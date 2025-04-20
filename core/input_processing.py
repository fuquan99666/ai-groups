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
    for pattern in SAFETY_CONFIG["injection_patterns"]:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text
