"""表达式求值与合法性检查。"""
from model import Node

"""表达式不满足题目约束时抛出。"""
class InvalidExpression(Exception):
    pass

"""递归求值，返回 Fraction。不满足约束时抛 InvalidExpression。"""
def evaluate(node: Node):
    
    if node.is_leaf():
        return node.value

    left = evaluate(node.left)
    right = evaluate(node.right)

    if node.op == "+":
        return left + right

    if node.op == "-":
        if left < right:
            raise InvalidExpression("减法结果为负数")
        return left - right

    if node.op == "*":
        return left * right

    if node.op == "/":
        if right == 0:
            raise InvalidExpression("除数为 0")
        result = left / right
        if result.denominator == 1:
            raise InvalidExpression("除法结果为整数")
        return result

    raise InvalidExpression(f"未知运算符：{node.op}")