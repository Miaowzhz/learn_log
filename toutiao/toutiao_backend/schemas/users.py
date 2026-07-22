from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str = Field(..., title="用户名", min_length = 2, max_length=50)
    password: str

class UserInfoBase(BaseModel):
    """
    ⽤户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")

# user_info
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 对象获取属性
    )


# 响应类
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo", title="用户信息")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # alias / 字段名兼容
        from_attributes=True  # 允许从 ORM 对象获取属性
    )

# 修改用户信息
class UpdateUserRequest(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None

# 修改用户密码
class UpdateUserPassword(BaseModel):
    old_password: str = Field(..., alias="oldPassword", title="旧密码")
    new_password: str = Field(..., alias="newPassword", title="新密码")