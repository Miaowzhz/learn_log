"""
教务系统实现
采用面向对象的编程思想，完成教务管理系统的开发。教务管理系统可以管理在校学生的成绩信息，通过控制台菜单与用户交互，具体的功能如下：
1.添加学生成绩：根据输入的学生姓名、语文成绩、数学成绩、英语成绩，记录在系统中
2. 修改学生成绩：根据输入的学生姓名，修改对应的学生成绩
3. 删除学生成绩:根据输入的学生姓名，删除对应的学生成绩
4. 查询指定学生成绩:根据输入的学生姓名，查找对应的学生成绩，并输出
5. 展示全部学生成绩：展示出系统中所有学生的成绩
需求：实现完整的教务系统
思路：1) 设计学生类 2) 实现添加、删除、修改、查询功能 3) 添加异常处理
"""

class Student:

    def __init__(self, name: str, chinese, math, english):
        self.name = name
        self.chinese = chinese
        self.math = math
        self.english = english

    def __str__(self):
        return f"姓名: {self.name}, 语文成绩: {self.chinese}, 数学成绩: {self.math}, 英语成绩: {self.english}, 总成绩: {self.chinese + self.math + self.english}"

    def put_score(self, name=None, chinese=None, math=None, english=None):
        if chinese is not None:
            self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english

class StuMG:
    version = "1.0.0"
    name = "学生管理系统"

    def __init__(self):
        self.stu_list = []

    # 添加学生信息
    def add_stu(self):
        name = input("请输入学生姓名: ")

        # 查看学生是否已存在
        for s in self.stu_list:
            if s.name == name:
                print("该学生信息已存在!")
                return

        chinese = int(input("请输入学生语文成绩: "))
        math = int(input("请输入学生数学成绩: "))
        english = int(input("请输入学生英语成绩: "))
        # 分数要在 1-100 之间
        if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
            stu = Student(name, chinese, math, english)
            self.stu_list.append(stu)
            print("学生信息添加成功!")
        else:
            print("输入的成绩不合法!")
            return

    # 修改学生信息
    def put_stu(self):
        name = input("请输入需要修改学生姓名: ")

        # 查看学生是否已存在
        for s in self.stu_list:
            if s.name == name:
                print(f"当前成绩: {s}")

                chinese = int(input("请输入学生语文成绩: "))
                math = int(input("请输入学生数学成绩: "))
                english = int(input("请输入学生英语成绩: "))
                # 分数要在 1-100 之间
                if 0 <= chinese <= 100 and 0 <= math <= 100 and 0 <= english <= 100:
                    s.put_score(name, chinese, math, english)
                    print("学生信息修改成功!")
                    print(f"修改后的成绩: {s}")
                    return
                else:
                    print("输入的成绩不合法!")
                    return
        print("未找到该学生!")
        return

    # 删除学生信息
    def del_stu(self):
        name = input("请输入需要删除学生姓名: ")

        # 查看学生是否已存在
        for s in self.stu_list:
            if s.name == name:
                self.stu_list.remove(s)
                print("学生信息删除成功!")
                return
        print("未找到该学生!")
        return

    # 查询指定学生的成绩
    def get_stu(self):
        name = input("请输入需要查询学生姓名: ")

        # 查看学生是否已存在
        for s in self.stu_list:
            if s.name == name:
                print(f"学生信息: {s}")
                return
        print("未找到该学生!")
        return

    # 查询全部学生的成绩
    def list_stu(self):
        for s in self.stu_list:
            print(s)
        print("未找到学生信息")
        return

    def run(self):
        print(f"欢迎使用学生管理系统 V{StuMG.version}")

        while True:
            print()
            print("================================================================")
            print("1 添加学生 2 修改学生 3 删除学生 4 查询指定学生 5 查询所有学生 6 退出系统")
            print("================================================================")

            choice = input("请选择要执行的操作: ")

            # 捕获异常
            try:
                match choice:
                    case '1':
                        self.add_stu()
                    case '2':
                        self.put_stu()
                    case '3':
                        self.del_stu()
                    case '4':
                        self.get_stu()
                    case '5':
                        self.list_stu()
                    case '6':
                        break
                    case _:
                        print("操作不合法")
            except ValueError:
                print("输入的数据有问题, 请检查后重新输入!")
            except Exception:
                print("程序运行出错了, 请重新选择!")

if __name__ == '__main__':
    stuMG = StuMG()
    stuMG.run()