# 四则运算题目生成器 设计文档

## 目标

命令行程序，支持：

* 生成小学四则运算题：`python main.py -n 10 -r 10`
* 批改题目和答案：`python main.py -e Exercises.txt -a Answers.txt`

## 模块

* `main.py`：入口、参数解析
* `generator.py`：生成题目
* `evaluator.py`：求值、合法性检查
* `formatter.py`：分数格式化
* `dedup.py`：题目去重
* `grader.py`：批改统计

## 数据结构

表达式用二叉树：

```python

class Node:
  value = None   # Fraction
  op = None      # + - \* /
  left = None
  right = None

```

题目：

```python

class Question:
    expr_tree: Node
    expr_str: str      # 如 "1/2 + 1/3"
    answer: Fraction   # 答案
    answer_str: str    # 如 "5/6"

```

## 生成规则

* -n 题目数量
* -r 数值范围，生成 [0, r)
* 运算符最多 3 个
* 减法不能出现负数
* 除法除数不能为 0，结果不能是整数
* 题目不能重复
* 去重：对 +、* 左右子树排序后生成标准字符串比较

## 文件格式

Exercises.txt

```text
1. 1/2 + 1/3 = 
2. 2/3 × 3/4 = 
```

Answers.txt

```text
1. 5/6
2. 1/2
```

Grade.txt

```text
Correct: 5 (1, 3, 5, 7, 9)
Wrong: 5 (2, 4, 6, 8, 10)
```

## 分数格式

* 整数：`3`
* 真分数：`3/5`
* 带分数：`2'3/8`

## 批改流程

1. 读 Exercises.txt 和 Answers.txt
2. 逐题计算正确答案
3. 与答案文件比较
4. 统计正确、错误题号
5. 写入 Grade.txt

## 测试

* `-n 10 -r 10`
* `-n 10000 -r 100`
* 减法无负数
* 除法结果非整数
* 运算符不超过 3 个
* 批改统计正确