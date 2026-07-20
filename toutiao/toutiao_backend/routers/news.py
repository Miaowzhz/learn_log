from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/news", tags=["news"])

# 接口实现流程
# 1. 模块化路由 -> API 接口规范文档
# 2. 定义模型类 -> 数据库表(数据库设计文档)
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):

    # 获取数据库里的新闻分类 --> 先定义模型类 --> 封装查询数据的方法
    categories = await news.get_categories(db, skip, limit)

    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

# 获取所有新闻
@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(..., alias="pageSize"),
        db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * page_size
    limit = page_size
    news_list = await news.get_news_list(db, category_id, skip, limit)
    total = await news.get_news_total(db, category_id)
    has_more = (skip + limit) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "total": total,
            "list": news_list,
            "hasMore": has_more
        }
    }

# 获取新闻详情
@router.get("/detail")
async def get_news_detail(
        news_id: int = Query(..., alias="id"),
        db: AsyncSession = Depends(get_db)
):

    # 获取新闻详情 + 浏览量 + 1 + 相关新闻

    # 获取新闻详情
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 浏览量 + 1
    views = await news.increase_news_views(db, news_id)
    if not views:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 相关新闻
    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id, 5)


    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "description": news_detail.description,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }