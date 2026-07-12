# Python 五个容器常用方法

第三天重点学习五个容器：

- `list`：列表
- `str`：字符串
- `tuple`：元组
- `set`：集合
- `dict`：字典

先记住一句话：先判断数据长什么样，再选择合适的容器。

## 1. list 列表

列表特点：有顺序、可以修改、允许重复，通常用索引查找数据。

```python
nums = [1, 2, 3]
```

常用方法：

| 方法 | 作用 | 示例 |
| --- | --- | --- |
| `append()` | 在末尾添加一个元素 | `nums.append(4)` |
| `insert()` | 在指定位置插入元素 | `nums.insert(1, 100)` |
| `extend()` | 合并另一个列表 | `nums.extend([5, 6])` |
| `remove()` | 按元素值删除 | `nums.remove(2)` |
| `pop()` | 删除并返回元素，默认最后一个 | `nums.pop()` |
| `clear()` | 清空列表 | `nums.clear()` |
| `index()` | 查找元素索引 | `nums.index(3)` |
| `count()` | 统计元素出现次数 | `nums.count(1)` |
| `sort()` | 排序，会修改原列表 | `nums.sort()` |
| `reverse()` | 反转，会修改原列表 | `nums.reverse()` |
| `copy()` | 复制列表 | `nums.copy()` |

优先掌握：

```python
append()
remove()
pop()
index()
count()
sort()
```

## 2. str 字符串

字符串特点：有顺序、不能修改，本质是一串字符。

```python
msg = "hello python"
```

常用方法：

| 方法 | 作用 | 示例 |
| --- | --- | --- |
| `count()` | 统计出现次数 | `msg.count("o")` |
| `find()` | 查找位置，找不到返回 `-1` | `msg.find("python")` |
| `index()` | 查找位置，找不到会报错 | `msg.index("python")` |
| `replace()` | 替换内容，返回新字符串 | `msg.replace("python", "world")` |
| `split()` | 切分字符串，返回列表 | `msg.split()` |
| `join()` | 把多个字符串拼接成一个字符串 | `",".join(["a", "b", "c"])` |
| `strip()` | 去掉两边空白 | `msg.strip()` |
| `lower()` | 转小写 | `msg.lower()` |
| `upper()` | 转大写 | `msg.upper()` |
| `startswith()` | 判断是否以指定内容开头 | `msg.startswith("hello")` |
| `endswith()` | 判断是否以指定内容结尾 | `msg.endswith("python")` |

优先掌握：

```python
count()
find()
replace()
split()
join()
strip()
```

注意：字符串不能原地修改，`replace()` 会返回一个新字符串。

```python
msg = "hello python"
msg = msg.replace("python", "world")
print(msg)
```

## 3. tuple 元组

元组特点：有顺序、不能修改，适合保存固定的一组数据。

```python
student = ("mark", 18, 90)
```

常用方法：

| 方法 | 作用 | 示例 |
| --- | --- | --- |
| `count()` | 统计元素出现次数 | `student.count("mark")` |
| `index()` | 查找元素索引 | `student.index(18)` |

元组更重要的是解包：

```python
name, age, score = student
print(name, age, score)
```

优先掌握：

```python
count()
index()
解包
```

## 4. set 集合

集合特点：无顺序、不重复，适合去重和判断元素是否存在。

```python
nums = {1, 2, 3}
```

常用方法：

| 方法 | 作用 | 示例 |
| --- | --- | --- |
| `add()` | 添加元素 | `nums.add(4)` |
| `remove()` | 删除元素，不存在会报错 | `nums.remove(2)` |
| `discard()` | 删除元素，不存在也不报错 | `nums.discard(10)` |
| `pop()` | 随机删除一个元素 | `nums.pop()` |
| `clear()` | 清空集合 | `nums.clear()` |
| `union()` | 并集 | `a.union(b)` |
| `intersection()` | 交集 | `a.intersection(b)` |
| `difference()` | 差集 | `a.difference(b)` |

优先掌握：

```python
add()
remove()
discard()
union()
intersection()
```

去重示例：

```python
nums = [1, 2, 2, 3, 3, 4]
nums_set = set(nums)
print(nums_set)
```

## 5. dict 字典

字典特点：保存 `key-value` 键值对，通过 `key` 查找 `value`。

```python
student = {
    "name": "mark",
    "age": 18,
    "score": 90
}
```

常用方法：

| 方法 | 作用 | 示例 |
| --- | --- | --- |
| `get()` | 获取 value，key 不存在时不报错 | `student.get("name")` |
| `keys()` | 获取所有 key | `student.keys()` |
| `values()` | 获取所有 value | `student.values()` |
| `items()` | 获取所有 key-value | `student.items()` |
| `update()` | 更新字典 | `student.update({"score": 100})` |
| `pop()` | 删除指定 key，并返回 value | `student.pop("age")` |
| `clear()` | 清空字典 | `student.clear()` |
| `copy()` | 复制字典 | `student.copy()` |

优先掌握：

```python
get()
keys()
values()
items()
update()
pop()
```

遍历字典：

```python
for key, value in student.items():
    print(key, value)
```

## 通用操作

这些操作五个容器经常都会用到：

| 操作 | 作用 | 示例 |
| --- | --- | --- |
| `len()` | 获取长度 | `len(nums)` |
| `for` | 遍历容器 | `for item in nums:` |
| `in` | 判断是否存在 | `"name" in student` |
| 索引 | 按位置取值 | `nums[0]` |
| 切片 | 取一段数据 | `nums[1:4]` |

注意：`set` 和 `dict` 不是靠普通索引取值；`dict` 是靠 `key` 取值。

## 最小背诵版

```text
list：append remove pop sort
str：count find replace split join strip
tuple：count index 解包
set：add remove discard union intersection
dict：get keys values items update pop
```

## 怎么选容器

| 场景 | 推荐容器 |
| --- | --- |
| 保存多个待办事项 | `list` |
| 保存一段文本 | `str` |
| 保存固定不想改的数据 | `tuple` |
| 去重 | `set` |
| 保存一个对象的多个属性 | `dict` |
| 保存多个学生，每个学生有多个属性 | `list + dict` |
