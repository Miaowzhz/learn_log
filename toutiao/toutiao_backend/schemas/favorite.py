from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


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