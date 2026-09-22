import re
from fractions import Fraction

"""从 "1. 1/2 + 1/3 = " 中提取表达式部分"""
def parse_exercise(line: str) -> str:
    line = line.strip()
    m = re.match(r"\d+\.\s*(.+?)\s*=", line)
    if m:
        return m.group(1)
    return line.rstrip("=").strip()

"""从 "1. 5/6" 或 "1. 2'3/8" 中解析出 Fraction"""
def parse_answer(line: str) -> Fraction:

    line = line.strip()
    m = re.match(r"\d+\.\s*(.+)", line)
    if m:
        line = m.group(1).strip()

    if "'" in line:
        integer, frac = line.split("'")
        num, den = frac.split("/")
        return Fraction(int(integer) * int(den) + int(num), int(den))

    if "/" in line:
        num, den = line.split("/")
        return Fraction(int(num), int(den))

    return Fraction(int(line))

"""对表达式字符串求值，返回 Fraction
先把 × ÷ 换成 * /，再把分数形式转成 Fraction(...)
"""
def eval_expr_string(s: str) -> Fraction:
    s = s.replace("×", "*").replace("÷", "/")

    # 带分数 a'b/c -> (Fraction(a,1)+Fraction(b,c))
    s = re.sub(r"(\d+)'(\d+)/(\d+)",
               r"(Fraction(\1,1)+Fraction(\2,\3))", s)
    # 真分数 a/b -> Fraction(a,b)
    s = re.sub(r"(\d+)/(\d+)", r"Fraction(\1,\2)", s)

    return eval(s, {"Fraction": Fraction})


def grade(exercise_file: str, answer_file: str):
    with open(exercise_file, encoding="utf-8") as f:
        exercises = [line for line in f if line.strip()]
    with open(answer_file, encoding="utf-8") as f:
        answers = [line for line in f if line.strip()]

    correct, wrong = [], []

    for i, (ex_line, ans_line) in enumerate(zip(exercises, answers), 1):
        expr = parse_exercise(ex_line)
        try:
            correct_ans = eval_expr_string(expr)
        except Exception:
            wrong.append(i)
            continue

        try:
            user_ans = parse_answer(ans_line)
        except Exception:
            wrong.append(i)
            continue

        if user_ans == correct_ans:
            correct.append(i)
        else:
            wrong.append(i)

    with open("Grade.txt", "w", encoding="utf-8") as f:
        f.write(f"Correct: {len(correct)} "
                f"({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} "
                f"({', '.join(map(str, wrong))})\n")

    print(f"批改完成，结果写入 Grade.txt")


if __name__ == "__main__":
    grade("Exercises.txt", "Answers.txt")