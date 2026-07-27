from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


# 检查新闻收藏状态
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite", title="是否收藏")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # alias / 字段名兼容
        from_attributes=True  # 允许从 ORM 对象获取属性
    )

# 添加收藏请求体
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", title="新闻ID")

# 收藏基础响应
class FavoriteBaseResponse(BaseModel):
    id: int
    user_id: int
    news_id: int
    created_at: datetime


# 收藏基础响应类
class FavoriteNewsItemResponse(NewsItemBase):

    favorite_id: int = Field(alias="favoriteId", title="收藏ID")
    favorite_time: datetime = Field(alias="favoriteTime", title="收藏时间")

    model_config = ConfigDict(
        populate_by_name=True, # alias / 字段名兼容
        from_attributes=True  # 允许从 ORM 对象获取属性
    )


# 收藏列表响应类
class FavoriteListResponse(BaseModel):

    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore", title="是否有更多")

    model_config = ConfigDict(
        populate_by_name=True, # alias / 字段名兼容
        from_attributes=True  # 允许从 ORM 对象获取属性
    )