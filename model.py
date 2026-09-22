from fractions import Fraction

"""表达式树节点
- 叶子节点：value 为 Fraction，op/left/right 为 None
- 非叶子节点：op 为运算符，left/right 为子节点，value 为 None
"""
class Node:
    
    def __init__(self, value=None, op=None, left=None, right=None):
        self.value = value
        self.op = op
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.value is not None