from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserInfoBase, UpdateUserRequest, \
    UpdateUserPassword
from utils.auth import get_current_user
from utils.response import success_response

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/user", tags=["user"])

# 接口实现流程
# 1. 模块化路由 -> API 接口规范文档
# 2. 定义模型类 -> 数据库表(数据库设计文档)
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

# 登录
@router.post("/login")
async def login(user_request: UserRequest, db: AsyncSession = Depends(get_db)):

    # 判断用户名是否存在
    # 校验密码(明文\密文)
    user = await users.authenticate_user(db, user_request.username, user_request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    # 生成Token
    token = await users.create_token(db, user.id)

    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))

    return success_response(message="登录成功", data=response_data)

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
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))

# 修改用户信息
@router.put("/update")
async def update_user_info(
        user_request: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    user = await users.update_user_info(db, user.username, user_request)
    return success_response(
        message="修改用户信息成功",
        data=UserInfoResponse.model_validate(user)
    )

# 修改密码
@router.put("/password")
async def update_password(
        user_data: UpdateUserPassword,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):

    # 验证旧密码 修改密码
    user = await users.update_password(db, user.username, user_data)
    return success_response(
        message="修改密码成功",
        data=UserInfoResponse.model_validate(user)
    )
