TEST_CASES = [
    {
        "description": "客服场景-参数对比",
        "input": {
            "messages": [{"role": "user", "content": "请解释云计算的优势"}],
            "params": [
                {"temperature": 0.3, "top_p": 0.9}, 
                {"temperature": 1.2, "top_p": 0.5}
            ]
        }
    },
    {
        "description": "工具集成测试",
        "input": {
            "messages": [{"role": "user", "content": "今天北京天气如何？"}],
            "expected_tool": "weather"
        }
    }
]
