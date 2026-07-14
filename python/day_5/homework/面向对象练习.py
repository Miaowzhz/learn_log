class Car:
    # 类属性
    price_rate = 1.1

    # 魔法方法 自动调用
    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price
        print("创建了一个车对象")

    def run(self):
        print(f"{self.name} 在跑---")

    def total_cost(self):
        return self.price * 1.1

    def __str__(self):
        return f"{self.name} {self.color} {self.price}"

    def __eq__(self, other):
        return self.price == other.price

    def __lt__(self, other):
        return self.price < other.price

car_1 = Car("保时捷", "黑色", 100000)
car_2 = Car("宝马", "黄色", 200000)

car_1.run()
print(round(car_1.total_cost(), 1))

print(car_2.__str__())
print(car_1.__eq__(car_2))
print(car_1.__lt__(car_2))

# 通过类名访问类属性
print(Car.price_rate)
# 通过对象名访问类属性, 优先查找实例属性, 找不到再查找类属性
print(car_1.price_rate)
