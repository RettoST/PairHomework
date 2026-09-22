"""诊断脚本：找出第一批被判错的题目的详情。"""
from grader import parse_exercise, parse_answer, eval_expr_string
from fractions import Fraction

with open("Exercises.txt", encoding="utf-8") as f:
    exercises = [line.strip() for line in f if line.strip()]
with open("Answers.txt", encoding="utf-8") as f:
    answers = [line.strip() for line in f if line.strip()]

wrong_ids = [2, 63, 99]  # 前几个出错题号

for i, (ex, ans) in enumerate(zip(exercises, answers), 1):
    if i not in wrong_ids:
        continue
    expr = parse_exercise(ex)
    try:
        correct = eval_expr_string(expr)
    except Exception as e:
        correct = f"ERROR: {e}"
    user = parse_answer(ans)
    print(f"第 {i} 题")
    print(f"  原始行    : {ex!r}")
    print(f"  提取表达式: {expr!r}")
    print(f"  批改器算出: {correct}")
    print(f"  答案文件  : {user}")
    print(f"  相等?     : {correct == user if not isinstance(correct, str) else False}")
    print()