from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import favorite, history
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest
from schemas.history import AddHistoryRequest
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
    await history.add_history(db, user.id, add_history_request.news_id)

    return success_response(
        message="添加浏览记录成功",
        data=None
    )