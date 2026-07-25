from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


# 添加浏览记录请求体
class AddHistoryRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", title="新闻ID")

# 获取浏览记录基础响应体
class HistoryBaseResponse(NewsItemBase):

    history_id: int = Field(alias="historyId", title="浏览记录ID")
    view_time: datetime = Field(alias="viewTime", title="浏览时间")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

# 获取浏览记录列表响应体
class HistoryListResponse(BaseModel):
    """获取浏览记录列表响应体"""
    list: list[HistoryBaseResponse]
    total: int
    has_more: bool = Field(alias="hasMore", title="是否有更多")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )