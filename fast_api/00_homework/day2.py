"""
实践任务：

图书管理API（基础版）
需求：实现图书的增删改查接口（使用内存存储）
思路：1) 定义Book Pydantic模型 2) 实现GET/POST/PUT/DELETE路由 3) 使用列表存储数据 4) 测试各接口
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 定义图书模型
class Book(BaseModel):
    book_id: int
    book_name: str
    author: str
    price: float

# 图书列表存储数据
book_list = []

# 获取全部图书
@app.get("/book/get/list")
async def get_book_list():
    return book_list

# 根据id获取图书
@app.get("/book/get/{book_id}")
async def get_book(book_id: int):
    for book in book_list:
        if book.book_id == book_id:
            return book
    return {"message": "图书不存在"}

# 添加图书
@app.post("/book/add")
async def add_book(book: Book):
    book_list.append(book)
    return {"message": "添加成功"}

# 修改图书
@app.put("/book/update")
async def put_book(book: Book):
    for p_book in book_list:
        if p_book.book_id == book.book_id:
            p_book.book_name = book.book_name
            p_book.author = book.author
            p_book.price = book.price
            return {"message": "修改成功"}
    return {"message": "图书不存在"}

# 删除图书
@app.delete("/book/delete/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(book_list):
        if book.book_id == book_id:
            del book_list[i]
            return {"message": "删除成功"}
    return {"message": "图书不存在"}