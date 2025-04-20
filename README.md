
# 基于 FastAPI 的智能化对话服务架构说明

## 项目概述
本系统采用模块化设计实现多模型对话服务，核心功能包含：
- 多模型 API 流式响应
- 参数对比可视化
- 输入内容安全过滤
- 外部工具动态集成
- 服务端推送(SSE)支持

## 🗂️ 目录结构
```text
.
├── config.py             # 全局配置
├── schemas.py            # 数据模型定义
├── core/                 # 核心业务模块
│   ├── model_api.py      # 模型调用逻辑
│   ├── input_processing.py # 输入预处理
│   └── tools.py          # 外部工具集成
├── main.py               # API入口路由
├── frontend/             # 前端实现
└── tests/                # 测试数据及用例