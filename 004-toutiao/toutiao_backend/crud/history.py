from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from models.news import News

# 添加浏览记录
async def add_history(db: AsyncSession, user_id, news_id):

    # 查询该新闻的浏览记录否存在
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()
    # 存在则更新时间
    if history is not None:
        history.view_time = func.now()
        await db.commit()
        await db.refresh(history)
        return history

    # 添加浏览记录
    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history

# 获取浏览记录列表
async def get_history_list(db: AsyncSession, user_id, offset, page_size):

    # 查询该新闻的浏览记录总数
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # 查询该用户所有的浏览记录
    query = (
        select(News, History.view_time, History.id.label("history_id"))
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset).limit(page_size)
    )
    result = await db.execute(query)
    news_list = result.all()

    return total, news_list

# 删除浏览记录
async def remove_history(db: AsyncSession, user_id, news_id):
    deleted = delete(History).where(History.news_id == news_id, History.user_id == user_id)
    result = await db.execute(deleted)
    await db.commit()
    return result.rowcount > 0

# 清空浏览记录
async def clear_history(db: AsyncSession, user_id):
    deleted = delete(History).where(History.user_id == user_id)
    result = await db.execute(deleted)
    await db.commit()
    return result.rowcount