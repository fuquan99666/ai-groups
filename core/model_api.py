async def stream_model_response(request: ChatRequest):
    """
    流式调用不同模型的API，生成器函数
    返回 tokens 的异步生成器
    """
    if request.model == "gpt-3.5":
        async for chunk in openai_chat_stream(request):
            yield chunk
    elif request.model == "qwen":
        ...

async def openai_chat_stream(request: ChatRequest):
    """OpenAI 流式响应实现"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{MODEL_CONFIG['gpt-3.5']['base_url']}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "messages": [m.dict() for m in request.messages],
                "temperature": request.temperature,
                "stream": True,
                "top_p": request.top_p
            },
            timeout=30
        )
        async for line in response.aiter_lines():
            if line.startswith("data:"):
                yield parse_openai_chunk(line[5:].strip())
