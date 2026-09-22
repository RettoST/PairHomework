import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="小学四则运算题目生成 / 批改程序",
        add_help=True,
    )
    parser.add_argument("-n", type=int, help="生成题目的个数")
    parser.add_argument("-r", type=int, help="题目中数值的范围")
    parser.add_argument("-e", type=str, help="题目文件路径")
    parser.add_argument("-a", type=str, help="答案文件路径")
    return parser.parse_args()


def main():
    args = parse_args()

    # 批改
    if args.e or args.a:
        if not (args.e and args.a):
            print("错误：批改模式必须同时指定 -e 和 -a")
            print("用法：main.py -e <exercisefile>.txt -a <answerfile>.txt")
            sys.exit(1)
        from grader import grade
        grade(args.e, args.a)
        return

    # 生成
    if args.n is not None:
        if args.r is None:
            print("错误：生成题目必须指定 -r 参数")
            print("用法：main.py -n 10 -r 10")
            sys.exit(1)
        if args.n <= 0:
            print("错误：-n 必须为正整数")
            sys.exit(1)
        if args.r <= 0:
            print("错误：-r 必须为正整数")
            sys.exit(1)
        from generator import generate_and_save
        generate_and_save(args.n, args.r)
        return

    # 没有有效参数
    print("用法：")
    print("  生成题目：main.py -n 10 -r 10")
    print("  批改答案：main.py -e Exercises.txt -a Answers.txt")
    sys.exit(1)


if __name__ == "__main__":
    main()