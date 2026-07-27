"""
记账小程序
"""

# 存储列表
bill_list = []

# 程序入口
while True:
    print("============记账小程序============")
    print("1. 添加收入")
    print("2. 添加支出")
    print("3. 查看记录")
    print("4. 查看统计")
    print("5. 退出")
    print("================================")
    choose = int(input("请选择操作："))
    match choose:
        case 1:
            bill = dict()
            bill_amount = float(input("请输入收入金额："))
            bill_type = input("请输入收入类型：")
            bill_remark = input("请输入收入备注：")
            bill["amount"] = bill_amount
            bill["type"] = bill_type
            bill["remark"] = bill_remark
            bill_list.append(bill)
            print("添加收入成功")
        case 2:
            # 添加支出
            bill = dict()
            bill_amount = float(input("请输入支出金额："))
            bill_type = input("请输入支出类型：")
            bill_remark = input("请输入支出备注：")
            bill["amount"] = -bill_amount
            bill["type"] = bill_type
            bill["remark"] = bill_remark
            bill_list.append(bill)
            print("添加支出成功")
        case 3:
            # 查看记录
            print("============记账列表============")
            for bill in bill_list:
                print(f"金额：{bill['amount']}，类型：{bill['type']}，备注：{bill['remark']}")
        case 4:
            # 查看统计
            print("============记账统计============")
            income = sum([bill["amount"] for bill in bill_list if bill["amount"] > 0])
            expenditure = sum([bill["amount"] for bill in bill_list if bill["amount"] < 0])
            print(f"总收入：{income} 元，\n总支出：{expenditure} 元，\n当前余额：{income + expenditure} 元")
        case 5:
            print("退出成功")
            break
        case _:
            print("输入错误，请重新输入")