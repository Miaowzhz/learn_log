from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


#
class AddHistoryRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", title="新闻ID")

