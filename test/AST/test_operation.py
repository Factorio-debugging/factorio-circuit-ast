import unittest

from AST.Operation import *


class TestOperation(unittest.TestCase):
    def test_constructor(self):
        op = Operation(NumericOperator.OR)
        self.assertEqual(op.operation, NumericOperator.OR)
        self.assertEqual(op.left, ConstantOperand(np.int32(0)))
        self.assertEqual(op.right, ConstantOperand(np.int32(0)))

    def test_eq(self):
        op1 = Operation(NumericOperator.OR)
        op2 = Operation(NumericOperator.ADD)
        self.assertNotEqual(op1, ConstantOperand(np.int32(2)))
        self.assertNotEqual(op1, op2)
        op2.operation = NumericOperator.OR
        op1.left = ConstantOperand(np.int32(10))
        self.assertNotEqual(op1, op2)
        op1.left = ConstantOperand(np.int32(0))
        op2.right = ConstantOperand(np.int32(50))
        self.assertNotEqual(op1, op2)
        op2.right = ConstantOperand(np.int32(0))
        self.assertEqual(op1, op2)
