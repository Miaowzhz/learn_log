from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from utils.response import success_response

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/user", tags=["user"])

# 接口实现流程
# 1. 模块化路由 -> API 接口规范文档
# 2. 定义模型类 -> 数据库表(数据库设计文档)
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

# 登录

# 注册
@router.post("/register")
async def register(user_request: UserRequest, db: AsyncSession = Depends(get_db)):

    # 判断用户名是否已存在
    existing_user = await users.get_user_by_username(db, user_request.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    # 创建用户
    user = await users.create_user(db, user_request)

    # 获取token
    token = await users.create_token(db, user.id)

    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)

# 获取用户信息

# 修改用户信息