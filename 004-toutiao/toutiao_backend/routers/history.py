from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import favorite, history
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest
from schemas.history import AddHistoryRequest, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/history", tags=["history"])

# 接口实现流程
# 1. 模块化路由 -> API 接口规范文档
# 2. 定义模型类 -> 数据库表(数据库设计文档)
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

# 添加浏览记录
@router.post("/add")
async def add_history(
        add_history_request: AddHistoryRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    # 添加浏览记录
    result = await history.add_history(db, user.id, add_history_request.news_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="添加浏览记录失败")

    return success_response(
        message="添加浏览记录成功",
        data=None
    )

# 获取浏览历史列表
@router.get("/list")
async def get_history_list(
        page: int = 1,
        page_size: int = Query(10, alias="pageSize"),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    # 偏移量
    offset = (page - 1) * page_size
    total, news_list = await history.get_history_list(db, user.id, offset, page_size)

    news_list = [{
        **news.__dict__,
        "viewTime": view_time,
        "historyId": history_id
    } for news, view_time, history_id in news_list]

    has_more = total > offset + page_size
    data = HistoryListResponse(list=news_list, total=total, hasMore=has_more)

    return success_response(
        message="获取浏览历史列表成功",
        data=data
    )

# 删除浏览记录
@router.delete("/delete/{news_id}")
async def delete_history(
        news_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    result = await history.remove_history(db, user.id, news_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="删除浏览记录失败")

    return success_response(
        message="删除浏览记录成功",
    )

# 清空浏览记录
@router.delete("/clear")
async def clear_history(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    result = await history.clear_history(db, user.id)

    return success_response(
        message="清空浏览记录成功"
    )