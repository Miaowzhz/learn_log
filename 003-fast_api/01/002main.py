# 请求体参数\类型注解
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 定义类型
class User(BaseModel):
    username: str
    password: str


@app.post("/register")
async def register(user: User):
    return {"username": user.username, "password": user.password}


# 练习
class Book(BaseModel):
    book_name: str = Field(..., min_length=2, max_length=20)
    author: str = Field(..., min_length=2, max_length=10)
    price: float = Field(..., gt=0)

@app.post("add_book")
async def add_book(book: Book):
    return {"book_name": book.book_name, "author": book.author, "price": book.price}
