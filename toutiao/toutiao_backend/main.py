from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许的跨域请求的源
    allow_credentials=True, # 允许携带 cookie
    allow_methods=["*"], # 允许的 HTTP 方法
    allow_headers=["*"], # 允许的 HTTP 头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 挂载路由
# 新闻模块
app.include_router(news.router)

# 用户模块
app.include_router(users.router)
