"""
中间件
依赖注入
"""
from fastapi import FastAPI, Query, Depends

app = FastAPI()

@app.middleware("http")
async def middleware(request, call_next):
    print("中间件1开始执行")
    response = await call_next(request)
    print("中间件1结束执行")
    return response

@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2开始执行")
    response = await call_next(request)
    print("中间件2结束执行")
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def common_parameters(
        skip: int = Query(0, description="跳过几条数据", lt=100),
        limit: int = Query(10, description="返回多少条数据", le=100)
):
    return {"skip": skip, "limit": limit}

@app.get("/news/news_list")
async def get_news_list(
        commons = Depends(common_parameters)
):
    return commons

@app.get("/news/news_list2")
async def get_news_list2(
        commons = Depends(common_parameters)
):
    return commons
