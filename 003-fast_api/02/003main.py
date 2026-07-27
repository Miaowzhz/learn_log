"""
查询
    条件查询:where(模糊查询 与或非 包含)
    聚合查询:func(计数 大小值 平均 求和)
    分页查询:offset limit

    获取所有数据
        scalars().all()

    获取单条数据
        scalars().first():提取第一个数据
        scalar_one_or_none():提取一个或null
        scalar():提取标量值(配合聚合查询使用)

添加


修改

删除
"""
from datetime import datetime
from unittest import result

from fastapi import FastAPI, Depends
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


# 查询接口
# 查询全部
@app.get("/book/list")
async def get_book_list(db: AsyncSession = Depends(get_db)):
    # 创建查询对象
    result = await db.execute(select(Book))
    # 获取查询结果
    book = result.scalars().all()
    return book

# 价格 — 必须放在 /book/{b_id} 前面，否则 price 会被当成动态参数
@app.get("/book/price")
async def get_book_price(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.price >= 33.0))
    return result.scalars().all()

# 指定id
@app.get("/book/{b_id}")
async def get_book(b_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == b_id))
    # print(f"会话进行提交: {result}")
    return result.scalars().one()

# 模糊查询
@app.get("/book/get/search_book")
async def search_book(db: AsyncSession = Depends(get_db)):
    # 模糊查询 like: % 任意个字符 _ 一个字符
    # result = await db.execute(select(Book).where((Book.book_name.like("三国%"))))

    # & | ~ 逻辑运算符
    # result = await db.execute(select(Book).where(Book.book_name.like("三国%") | Book.book_name.like("%国%")))

    # in_() 包含
    id_list = [1, 3, 5]
    result = await db.execute(select(Book).where(Book.id.in_(id_list)))

    return result.scalars().all()

# 聚合查询
@app.get("/book/select/aggregate")
async def aggregate(db: AsyncSession = Depends(get_db)):
    # 聚合查询: select( func.方法名(模型名.属性) )
    # result = await db.execute(select(func.count(Book.id)))

    # result = await db.execute(select(func.sum(Book.price)))

    result = await db.execute(select(func.avg(Book.price)))
    return result.scalar()

# 分页查询
@app.get("/book/select/page")
async def page(
        page:int = 1,
        page_size:int = 3,
        db: AsyncSession = Depends(get_db)
):
    offset_num = (page-1) * page_size
    result = await db.execute(select(Book).offset(offset_num).limit(page_size))
    return result.scalars().all()

# 添加
@app.post("/book/add")
async def add_book(new_book: Book, db: AsyncSession = Depends(get_db)):
    result = db.execute(select(Book).where(Book.book_name == new_book.book_name))
    if result.scalars().one_or_none() is None:
        db.add(new_book)
        await db.commit()
        return {"message": "添加成功"}
    else:
        return {"message": "图书已存在"}
