import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# 创建 Redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True # 是否将字节数据解码为字符串
)

# 缓存策略
# 旁路缓存 

# 设置(setex) 和 读取

# 读取: 字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None


# 读取: 列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data) # 序列化
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败: {e}")
        return None


# 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False) # 反序列化, 中文正常保存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False