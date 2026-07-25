from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users, favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteBaseResponse, FavoriteAddRequest, FavoriteListResponse
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserInfoBase, UpdateUserRequest, \
    UpdateUserPassword
from utils.auth import get_current_user
from utils.response import success_response

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/favorite", tags=["favorite"])

# 接口实现流程
# 1. 模块化路由 -> API 接口规范文档
# 2. 定义模型类 -> 数据库表(数据库设计文档)
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

# 检查新闻收藏状态
@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias="newsId", title="新闻ID"),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    # 检查新闻收藏状态
    favorite_check_response = await favorite.check_favorite(db, user.id, news_id)

    return success_response(
        message="检查新闻收藏状态成功",
        data=FavoriteCheckResponse(isFavorite=favorite_check_response)
    )

# 添加收藏
@router.post("/add")
async def add_favorite(
        request: FavoriteAddRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    result = await favorite.add_favorite(db, user.id, request.news_id)

    return success_response(
        message="收藏成功",
        data=result
    )

# 取消收藏
@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId", title="新闻ID"),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    # 删除收藏
    result = await favorite.remove_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏不存在")

    return success_response(
        message="取消收藏成功"
    )

# 获取收藏列表
@router.get("/list")
async def get_favorite_list(
        page: int = Query(default=1, alias="page"),
        page_size: int = Query(default=10, alias="pageSize"),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    offset = (page - 1) * page_size

    total, news_list = await favorite.get_favorite_list(db, user.id, offset, page_size)

    favorite_list = [{
        **news.__dict__,
        "favoriteTime": favorite_time,
        "favoriteId": favorite_id
    } for news, favorite_time, favorite_id in news_list]

    has_more = total > offset + page_size

    data = FavoriteListResponse(list=favorite_list, total=total, hasMore=has_more)
    return success_response(
        message="获取收藏列表成功",
        data=data
    )

# 清空收藏列表
@router.delete("/clear")
async def clear_favorite_list(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    # 清空收藏
    result = await favorite.clear_favorite_list(db, user.id)
    if result == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏列表为空")

    return success_response(
        message=f"成功删除{result}条收藏记录"
    )