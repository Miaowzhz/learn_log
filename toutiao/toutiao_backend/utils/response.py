from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

# 响应成功
def success_response(message: str = "success", data=None):

    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    return JSONResponse(content=jsonable_encoder(content))