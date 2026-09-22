from fractions import Fraction

# 分数处理 真分数假分数格式化

# 运算符到显示符号的映射
OP_SYMBOL = {
    "+": "+",
    "-": "-",
    "*": "×",
    "/": "÷",
}

"""把 Fraction 转成题目要求的字符串格式
- 整数：3
- 真分数：3/5
- 带分数：2'3/8
"""
def fraction_to_str(f: Fraction) -> str:

    if f.denominator == 1:
        return str(f.numerator)

    if abs(f.numerator) < f.denominator:
        return f"{f.numerator}/{f.denominator}"

    integer = f.numerator // f.denominator
    remain = f.numerator % f.denominator
    return f"{integer}'{remain}/{f.denominator}"