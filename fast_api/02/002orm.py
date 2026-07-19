"""
orm
"""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import Column, DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 创建数据库连接
async_engine = create_async_engine(
    "mysql+aiomysql://root:@127.0.0.1:3306/fast_api",
    echo=True,
    pool_size=10,
    max_overflow=20
)

# 定义模型类: 基类 + 模型类

class Base(DeclarativeBase):
    create_time:Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=datetime.now,
        comment="创建时间"
    )
    update_time:Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

class Book(Base):
    __tablename__ = "book"
    id:Mapped[int] = mapped_column(
        primary_key=True,
        comment="编号"
    )
    book_name:Mapped[str] = mapped_column(
        String(255),
        comment="书名"
    )
    author:Mapped[str] = mapped_column(
        String(255),
        comment="作者"
    )
    price:Mapped[float] = mapped_column(
        Float,
        comment="价格"
    )
    publisher:Mapped[str] = mapped_column(
        String(255),
        comment="出版社"
    )

# 创建表
async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 定义 lifespan 事件处理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: 应用启动时创建数据库表
    await create_table()
    yield
    # shutdown: 应用关闭时的清理工作（如有需要可在此添加）
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)


# 查询图书功能 -- 依赖注入
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, # 数据库连接
    class_=AsyncSession, # 异步会话类
    expire_on_commit=False # 提交后对象属性不过期
)

# 依赖项
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db # 返回数据库会话
            await db.commit() # 提交事务
        except  Exception:
            await db.rollback() # 回滚事务
            raise
        finally:
            await db.close() # 关闭数据库连接


@app.get("/book/list")
async def get_book_list(db: AsyncSession = Depends(get_db)):
    # 查询所有图书
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)