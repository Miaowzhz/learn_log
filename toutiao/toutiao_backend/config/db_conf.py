"""
数据库配置 - SQLAlchemy 异步引擎 + MySQL
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# DSN 格式：dialect+driver://user:password@host:port/database?params
# aiomysql = MySQL 异步驱动，charset=utf8mb4 支持 emoji 等四字节字符
DATABASE_URL = "mysql+aiomysql://root:@localhost:3306/fast_api?charset=utf8mb4"

# 异步引擎：管理连接池，将 ORM 操作翻译为 SQL
# 同步用 create_engine（WSGI），异步用 create_async_engine（ASGI/FastAPI）
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,              # True=打印SQL到控制台，生产环境建议 False
    pool_size=10,           # 连接池常驻连接数
    max_overflow=20,        # 超出 pool_size 后最多额外创建的连接数
                            # 峰值连接数 = pool_size + max_overflow = 30
)

# 会话工厂：每次调用产出一个新 session（类比"生产线"）
# session 是 ORM 操作的工作单元，所有增删改查都在其中进行
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False, # commit 后对象属性仍可直接访问，避免异步场景下延迟加载报错
)

# FastAPI 依赖注入：路由中通过 db: AsyncSession = Depends(get_db) 使用
# 生命周期：创建 session → yield db → 路由执行 → commit/rollback → 关闭
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db               # 将 db 交给路由函数
            await db.commit()      # 正常：提交事务，真正写入数据库
        except Exception:
            await db.rollback()    # 异常：回滚，撤销所有未提交操作
            raise                  # 重新抛出，让 FastAPI 返回错误响应
        finally:
            await db.close()       # 归还连接到池中（非断开 TCP）
