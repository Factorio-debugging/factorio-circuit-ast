import unittest

from AST.Operation import *


class TestOperation(unittest.TestCase):
    def test_constructor(self):
        op = Operation(NumericOperator.OR)
        self.assertEqual(op.operation, NumericOperator.OR)
        self.assertEqual(op.left, ConstantOperand(0))
        self.assertEqual(op.right, ConstantOperand(0))

    def test_eq(self):
        op1 = Operation(NumericOperator.OR)
        op2 = Operation(NumericOperator.ADD)
        self.assertNotEqual(op1, ConstantOperand(2))
        self.assertNotEqual(op1, op2)
        op2.operation = NumericOperator.OR
        op1.left = ConstantOperand(10)
        self.assertNotEqual(op1, op2)
        op1.left = ConstantOperand(0)
        op2.right = ConstantOperand(50)
        self.assertNotEqual(op1, op2)
        op2.right = ConstantOperand(0)
        self.assertEqual(op1, op2)
