import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.users import User, UserToken
from schemas.users import UserRequest, UpdateUserRequest, UpdateUserPassword
from utils import security


# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 创建用户
async def create_user(db: AsyncSession, user_request: UserRequest):

    # 密码加密
    # pip install "passlib[bcrypt]==1.7.4"
    # 创建密码加密上下⽂
    hashed_password = security.get_password_hash(user_request.password)

    user = User(username=user_request.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# 生成 Token
async def create_token(db: AsyncSession, user_id: int):
    # 流程: 1. 生成 token 2. 保存到数据库 3. 返回 token

    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
        await db.refresh(user_token)

    return token

# 校验密码
async def verify_password(password: str, hashed_password: str):
    return security.verify_password(password, hashed_password)

# 校验用户
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not security.verify_password(password, user.password):
        return None
    return user


async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    # 判断令牌是否存在/是否过期
    if user_token is None or user_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == user_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 修改用户信息
async def update_user_info(db: AsyncSession, username: str, user_request: UpdateUserRequest):

    query = update(User).where(User.username == username).values(**user_request.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    updated_user = await get_user_by_username(db, username)
    return updated_user

# 修改密码
async def update_password(db, username, user_data: UpdateUserPassword):
    user = await get_user_by_username(db, username)

    # 校验密码
    verify_result = await verify_password(user_data.old_password, user.password)
    if not verify_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")

    # 新旧密码不能相同
    if user_data.new_password == user_data.old_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="新旧密码不能相同")

    v_password = security.get_password_hash(user_data.new_password)
    query = update(User).where(User.username == username).values(password=v_password)
    await db.execute(query)
    await db.commit()
    updated_user = await get_user_by_username(db, username)
    return updated_user