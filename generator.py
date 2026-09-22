import random
from fractions import Fraction

from model import Node
from evaluator import evaluate, InvalidExpression
from formatter import fraction_to_str, OP_SYMBOL

"""生成 [0, r) 范围内的自然数或真分数"""
def random_number(r: int) -> Fraction: 
    if r <= 1:
        return Fraction(0)

    if random.random() < 0.5:
        return Fraction(random.randint(0, r - 1))

    den = random.randint(2, r - 1) if r > 2 else 2
    num = random.randint(1, den - 1)
    return Fraction(num, den)


def random_operator() -> str:
    return random.choice(["+", "-", "*", "/"])

"""递归构建含 num_ops 个运算符的表达式树"""
def build_tree(num_ops: int, r: int) -> Node:
    if num_ops == 0:
        return Node(value=random_number(r))

    left_ops = random.randint(0, num_ops - 1)
    right_ops = num_ops - 1 - left_ops

    left = build_tree(left_ops, r)
    right = build_tree(right_ops, r)
    return Node(op=random_operator(), left=left, right=right)

"""表达式树转字符串。子表达式非叶子时加括号"""
def tree_to_str(node: Node) -> str:
    if node.is_leaf():
        return fraction_to_str(node.value)

    left = tree_to_str(node.left)
    right = tree_to_str(node.right)
    if not node.left.is_leaf():
        left = f"({left})"
    if not node.right.is_leaf():
        right = f"({right})"
    return f"{left} {OP_SYMBOL[node.op]} {right}"


"""把表达式树标准化成字符串，用于去重
+ 和 × 满足交换律，左右子树标准化后按字典序排序
"""
def canonical(node: Node) -> str:

    if node.is_leaf():
        return fraction_to_str(node.value)

    left = canonical(node.left)
    right = canonical(node.right)
    if node.op in ("+", "*") and left > right:
        left, right = right, left
    return f"({node.op} {left} {right})"

"""生成一道题。失败返回 None"""
def generate_one(r: int):
    num_ops = random.randint(1, 3)
    for _ in range(50):
        tree = build_tree(num_ops, r)
        try:
            answer = evaluate(tree)
        except InvalidExpression:
            continue
        expr_str = tree_to_str(tree)
        return tree, expr_str, answer
    return None

"""生成 n 道题，写入 Exercises.txt 和 Answers.txt"""
def generate_and_save(n: int, r: int):
    questions = []
    seen = set()
    max_tries = n * 200
    tries = 0

    while len(questions) < n and tries < max_tries:
        tries += 1
        result = generate_one(r)
        if result is None:
            continue

        tree, expr_str, answer = result
        key = canonical(tree)
        if key in seen:
            continue
        seen.add(key)
        questions.append((expr_str, answer))

    with open("Exercises.txt", "w", encoding="utf-8") as f:
        for i, (expr, _) in enumerate(questions, 1):
            f.write(f"{i}. {expr} = \n")

    with open("Answers.txt", "w", encoding="utf-8") as f:
        for i, (_, ans) in enumerate(questions, 1):
            f.write(f"{i}. {fraction_to_str(ans)}\n")

    print(f"已生成 {len(questions)} 道题目，输出到 Exercises.txt 和 Answers.txt")