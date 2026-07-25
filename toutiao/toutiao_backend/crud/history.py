from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.favorite import Favorite
from models.news import News
from schemas.favorite import FavoriteCheckResponse

# 添加浏览记录
async def add_history(db, user_id, news_id):

    # 查询该新闻是否存在
    query = select(News).where(News.id == news_id)
    result = await db.execute(query)
    news = result.scalars().first()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")

    # 

    return None