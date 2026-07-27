import logging

from fastapi import HTTPException
from sqlalchemy import select, update, delete, func
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

    stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_favorite_list(db: AsyncSession, user_id, offset, page_size):
    # # 查收藏记录，提取新闻ID列表
    # query = select(Favorite).where(Favorite.user_id == user_id).offset(offset).limit(page_size)
    # result = await db.execute(query)
    # favorites = result.scalars().all()
    #
    # if not favorites:  # 空列表，无收藏
    #     return []
    #
    # news_id_list = [favorite.news_id for favorite in favorites]
    #
    # # 根据新闻ID查新闻详情
    # query = select(News).where(News.id.in_(news_id_list))
    # result = await db.execute(query)
    # news_list = result.scalars().all()
    #
    # return news_list if news_list else []

    # 最终返回: 总量 + 收藏的新闻列表
    # 总量
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # 联表查询: join + 时间排序 + 分页
    query = (
        select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    news_list = result.all()
    return total, news_list



async def clear_favorite_list(db: AsyncSession, user_id):

    # 查询一共有多少条记录
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0