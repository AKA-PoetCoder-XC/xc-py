import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/tools/get_current_time")
async def get_current_time(request: Request):
    """
    MCP工具：获取当前时间
    返回当前服务器时间，格式为ISO 8601字符串。
    """
    now = datetime.datetime.now().isoformat()
    return JSONResponse(content={"current_time": now})

@app.get("/")
def root():
    return {"msg": "MCP Demo Server，包含获取当前时间的工具。"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)