"""
添加


修改

删除
"""
from datetime import datetime
from unittest import result

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func, DateTime, String, Float
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

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

DATABASE_URL = "mysql+aiomysql://root:@localhost:3306/fast_api?charset=utf8mb4"

# 创建数据库连接
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, # 数据库连接
    class_=AsyncSession, # 异步会话类
    expire_on_commit=False # 提交后对象属性不过期
)

# 获取数据库会话通用函数
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

class BookBase(BaseModel):
    id: int
    book_name: str
    author: str
    price: float
    publisher: str


# 添加
@app.post("/book/add")
async def add_book(new_book: BookBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.book_name == new_book.book_name))
    if result.scalars().one_or_none() is None:
        book_obj = Book(**new_book.__dict__)
        db.add(book_obj)
        await db.commit()
        return {"message": "添加成功"}
    else:
        return HTTPException(status_code=400, detail="图书已存在")

class BookUpdate(BaseModel):
    book_name: str
    author: str
    price: float
    publisher: str

# 修改
@app.put("/book/put/{book_id}")
async def put_book(book_id: int, data: BookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book_obj = result.scalars().one_or_none()
    if book_obj is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    book_obj.book_name = data.book_name
    book_obj.author = data.author
    book_obj.price = data.price
    book_obj.publisher = data.publisher
    await db.commit()
    return {"message": "修改成功"}

# 删除
@app.delete("/book/delete")
async def del_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book_obj = await db.get(Book, book_id)
    if book_obj is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    await db.delete(book_obj)
    await db.commit()
    return {"message": "删除成功"}