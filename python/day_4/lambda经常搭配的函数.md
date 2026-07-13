# lambda 经常搭配的函数

## 1. lambda 是什么

`lambda` 用来定义一个简单的匿名函数，也就是没有函数名的函数。

普通函数：

```python
def square(num):
    return num ** 2
```

对应的 lambda：

```python
lambda num: num ** 2
```

基本格式：

```python
lambda 参数: 返回值表达式
```

lambda 会自动返回冒号后面表达式的结果，不需要写 `return`。

lambda 适合只使用一次、逻辑简单的函数。如果逻辑包含循环、多次判断或多行操作，应该使用 `def`。

---

## 2. sorted()：按指定规则排序

`sorted()` 会返回一个新的列表，不会修改原容器。

```python
sorted(容器, key=排序规则, reverse=False)
```

- `key`：指定按照什么数据排序
- `reverse=False`：默认升序
- `reverse=True`：降序

### 按字符串长度排序

```python
names = ["Tom", "Alexander", "Lucy"]

result = sorted(names, key=lambda name: len(name))
print(result)
```

结果：

```python
['Tom', 'Lucy', 'Alexander']
```

过程可以理解为：

```text
"Tom"       -> lambda 返回 3
"Alexander" -> lambda 返回 9
"Lucy"      -> lambda 返回 4
```

`sorted()` 根据 lambda 返回的数字排序，但最终保留的仍然是原来的字符串。

### 按字典中的成绩排序

```python
students = [
    {"name": "小明", "score": 80},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 70},
]

result = sorted(
    students,
    key=lambda student: student["score"],
    reverse=True,
)

print(result)
```

这里每次把一个学生字典传给 lambda，lambda 返回该学生的分数，`sorted()` 按分数降序排列。

列表自身的 `sort()` 也支持相同的 `key` 写法：

```python
students.sort(key=lambda student: student["score"])
```

区别是 `list.sort()` 会直接修改原列表，而 `sorted()` 会创建新列表。

---

## 3. map()：逐个转换元素

`map()` 会遍历容器，把每个元素交给函数处理。

```python
map(处理函数, 容器)
```

### 计算每个数字的平方

```python
numbers = [1, 2, 3, 4]

result = map(lambda num: num ** 2, numbers)
print(list(result))
```

结果：

```python
[1, 4, 9, 16]
```

`map()` 返回的不是列表，需要使用 `list()` 转换后才能直接查看完整结果。

上面的代码也可以使用列表推导式：

```python
result = [num ** 2 for num in numbers]
```

对于简单转换，列表推导式通常更直观。

---

## 4. filter()：按条件筛选元素

`filter()` 会把 lambda 返回 `True` 的元素保留下来。

```python
filter(判断函数, 容器)
```

### 筛选及格分数

```python
scores = [45, 60, 80, 59, 90]

result = filter(lambda score: score >= 60, scores)
print(list(result))
```

结果：

```python
[60, 80, 90]
```

这里 lambda 返回的是布尔值：

```text
45 >= 60 -> False -> 丢弃
60 >= 60 -> True  -> 保留
```

也可以使用列表推导式：

```python
result = [score for score in scores if score >= 60]
```

---

## 5. max() 和 min()：按指定规则找最大或最小元素

`max()` 和 `min()` 也支持 `key` 参数。

### 找出成绩最高的学生

```python
students = [
    {"name": "小明", "score": 80},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 70},
]

best_student = max(students, key=lambda student: student["score"])
print(best_student)
```

结果：

```python
{'name': '小红', 'score': 95}
```

lambda 返回分数作为比较标准，`max()` 最终返回的是完整的学生字典，而不是分数。

找最低分学生：

```python
lowest_student = min(students, key=lambda student: student["score"])
```

---

## 6. reduce()：把多个元素逐步合并成一个结果

`reduce()` 不属于内置函数，需要先导入：

```python
from functools import reduce
```

### 计算所有数字的和

```python
from functools import reduce

numbers = [1, 2, 3, 4]
result = reduce(lambda total, num: total + num, numbers)
print(result)
```

计算过程：

```text
1 + 2 = 3
3 + 3 = 6
6 + 4 = 10
```

结果为 `10`。

这个例子直接使用 `sum(numbers)` 更简单。只有在需要自定义合并规则时，`reduce()` 才更有价值。

---

## 7. 常用搭配对比

| 函数 | 作用 | lambda 应返回 | 最终结果 |
| --- | --- | --- | --- |
| `sorted()` | 排序 | 排序依据 | 新列表 |
| `list.sort()` | 排序 | 排序依据 | 修改原列表 |
| `map()` | 转换 | 转换后的新值 | 可迭代对象 |
| `filter()` | 筛选 | `True` 或 `False` | 可迭代对象 |
| `max()` | 找最大元素 | 比较依据 | 原容器中的一个元素 |
| `min()` | 找最小元素 | 比较依据 | 原容器中的一个元素 |
| `reduce()` | 逐步合并 | 两个值合并后的结果 | 一个最终结果 |

---

## 8. 最小记忆版

```python
# 排序
sorted(data, key=lambda item: 排序依据)

# 转换
list(map(lambda item: 转换结果, data))

# 筛选
list(filter(lambda item: 判断条件, data))

# 查找最大或最小元素
max(data, key=lambda item: 比较依据)
min(data, key=lambda item: 比较依据)

# 合并
from functools import reduce
reduce(lambda result, item: 合并结果, data)
```

判断应该使用哪个函数：

- 想改变每个元素：`map()`
- 想保留部分元素：`filter()`
- 想改变元素顺序：`sorted()`
- 想找一个最大或最小元素：`max()`、`min()`
- 想把所有元素合成一个结果：`reduce()`

如果 lambda 已经难以一眼看懂，就应该改成普通的 `def` 函数。
