
# （多模态）大语言模型应用开发

## 项目概述
本系统采用模块化设计实现多模型对话服务，核心功能包含：
- 多模型 API 流式响应
- 参数对比可视化
- 输入内容安全过滤
- 外部工具动态集成

## 🗂️ 目录结构
```text
.
├── config.py             # 全局配置
├── schemas.py            # 输入输出定义
├── core/                 # 核心业务模块
│   ├── model_api.py      # 模型调用逻辑
│   ├── input_processing.py # 输入预处理
├── tools/         # 外部工具集成
│   ├── get_weather.py    # 天气api查询
├── main.py               # 两个示例
├── frontend/             # 前端实现
└── tests/                # 测试数据及用例
```

## 🚨 已知问题追踪

### 核心层问题
#### `core/model_api.py`
```python
# 问题：异步流输出还没验证正确性，目前仍为同步版本
def openai_chat_non_stream(request: ChatRequest):

# 问题：希望输出能为固定格式ChatMessage
def format_non_stream_response(response) -> dict:
```   

#### `core/input_processing.py`
- 可能要调查下如何防注入，又怎么把代码放进来，最好能有防注入的前后对比，如果多的话也许可以把SAFETY_CONFIG从CONFIG分离出去

### 输入输出规范
#### `schemas.py`
- tools类规范
- 校验机制实现？

### 工具
- python
- 搜索(api/selenium?)

## 🌟 未来功能规划
- 语音输入输出
- 构建领域知识库
- 开发记忆机制
- MCP

# 6.1 Update
在main分支中，实现了机器人聊天和集成天气api（目前的是实时天气）
.csv文件没啥用，test.py是查询天气的具体实现，使用的是和风天气api
现在需要一位同志解决一下流式输出的问题！
