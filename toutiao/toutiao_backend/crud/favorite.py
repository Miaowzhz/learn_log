import logging

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.favorite import Favorite
from models.news import News
from schemas.favorite import FavoriteCheckResponse


# 检查新闻收藏状态
async def check_favorite(db: AsyncSession, user_id, news_id):

    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    favorite = result.scalar_one_or_none()
    if favorite is None:
        return False
    return True


async def add_favorite(db: AsyncSession, user_id, news_id):

    # 校验新闻是否存在
    query = select(News).where(News.id == news_id)
    result = await db.execute(query)
    news = result.scalar_one_or_none()
    if news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")

    # 校验新闻是否已收藏
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    favorite = result.scalar_one_or_none()
    if favorite is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="新闻已收藏")

    # 添加收藏
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def remove_favorite(db: AsyncSession, user_id, news_id):

    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    favorite = await db.execute(query)
    favorite = favorite.scalar_one_or_none()

    # deleted = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    # await db.execute(deleted)

    if favorite is not None:
        await db.delete(favorite)
        await db.commit()
        return True

    return False


async def get_favorite_list(db: AsyncSession, user_id, offset, page_size):
    # 查收藏记录，提取新闻ID列表
    query = select(Favorite).where(Favorite.user_id == user_id).offset(offset).limit(page_size)
    result = await db.execute(query)
    favorites = result.scalars().all()

    if not favorites:  # 空列表，无收藏
        return []

    news_id_list = [favorite.news_id for favorite in favorites]

    # 根据新闻ID查新闻详情
    query = select(News).where(News.id.in_(news_id_list))
    result = await db.execute(query)
    news_list = result.scalars().all()

    return news_list if news_list else []