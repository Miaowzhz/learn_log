"""
实践任务：

文件下载服务
需求：实现一个支持文件下载和HTML页面返回的接口
思路：1) 创建返回HTML页面的路由 2) 创建文件下载路由 3) 处理文件不存在等异常情况 4) 测试不同响应类型
"""
from fastapi import FastAPI
from starlette.responses import HTMLResponse, FileResponse

app = FastAPI()

# 创建返回HTML页面的路由
@app.get("/", response_class=HTMLResponse)
async def get_html():
    return HTMLResponse("<h1>这是HTML格式</h1>")

# 创建文件下载路由
# todo