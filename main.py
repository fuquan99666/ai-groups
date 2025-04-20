from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

@app.post("/chat")
async def chat_stream(request: ChatRequest):
    """流式聊天端点"""
    validate_request(request)  # 使用pydantic自动校验
    
    async def event_generator():
        async for chunk in stream_model_response(request):
            yield {"data": chunk}
    
    return EventSourceResponse(event_generator())

@app.post("/compare_params")
async def compare_parameters(request1: ChatRequest, request2: ChatRequest):
    """参数对比演示接口"""
    ...
