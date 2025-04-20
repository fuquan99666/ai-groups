async def call_external_tool(tool_name: str, params: dict):
    """外部工具路由"""
    if tool_name == "weather":
        return await get_weather(params["location"])
    elif tool_name == "calculator":
        return calculate(params["expression"])

async def get_weather(location: str):
    """天气API示例"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{EXTERNAL_TOOLS['weather_api']}/current.json",
            params={"q": location}
        )
        return f"{location}天气：{response.json()['current']['condition']['text']}"
