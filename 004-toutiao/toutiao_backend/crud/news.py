from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 获取所有新闻
async def get_news_list(db: AsyncSession, category_id: int, skip: int, limit: int):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 获取新闻总数
async def get_news_total(db, category_id):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

# 获取新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 更新新闻浏览量 + 1
async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    # 判断更新成功
    return result.rowcount > 0

# 获取相关新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):

    stmt = (select(News)
            .where(News.id != news_id, News.category_id == category_id)
            .order_by(News.views.desc(), News.publish_time.desc())
            .limit(limit))
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()
    # 列表推导式
    return [{
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,
        "categoryId": news.category_id,
        "views": news.views
    } for news in related_news]