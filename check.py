import json
import jsonschema
from jsonschema import validate

# ====== 1. Schema 定义：结构化输出字段格式 ======
output_schema = {
        "城市": {"type": "string"},
        "天气": {"type": "string"},
        "温度范围": {"type": "string"},
        "出行建议": {"type": "string"}
}

# ====== 2. 示例 GPT 输出（可以替换为真实模型返回结果） ======
llm_response = {
    "城市": "杭州",
    "天气": "小雨",
    "温度范围": "21°C ~ 26°C",
    "出行建议": "建议携带雨具，穿防水外套。"
}

# ====== 3. 校验函数 ======
def check_output_format(response_dict):
    try:
        validate(instance=response_dict, schema=output_schema)
        print("\n✅ 输出格式正确！")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print("\n❌ 输出格式错误：", e.message)
        return False

# ====== 4. 执行校验 ======
if __name__ == "__main__":
    print("当前模型输出：")
    print(json.dumps(llm_response, indent=2, ensure_ascii=False))
    check_output_format(llm_response)
