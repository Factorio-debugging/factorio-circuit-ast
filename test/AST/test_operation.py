import unittest

from AST.Operation import *
from AST.Network import Network


class TestOperation(unittest.TestCase):
    def test_constructor(self):
        net = Network()
        op = Operation(NumericOperator.OR, SignalOperand(net, Signal.SIGNAL_A))
        self.assertEqual(op.operation, NumericOperator.OR)
        self.assertEqual(op.left, ConstantOperand(np.int32(0)))
        self.assertEqual(op.right, ConstantOperand(np.int32(0)))
        self.assertEqual(op.result, SignalOperand(net, Signal.SIGNAL_A))

    def test_eq(self):
        net = Network()
        op1 = Operation(NumericOperator.OR, SignalOperand(net, Signal.SIGNAL_A))
        op2 = Operation(NumericOperator.ADD, SignalOperand(net, Signal.SIGNAL_A))
        self.assertNotEqual(op1, ConstantOperand(np.int32(2)))
        self.assertNotEqual(op1, op2)
        op2.operation = NumericOperator.OR
        op1.left = ConstantOperand(np.int32(10))
        self.assertNotEqual(op1, op2)
        op1.left = ConstantOperand(np.int32(0))
        op2.right = ConstantOperand(np.int32(50))
        self.assertNotEqual(op1, op2)
        op2.right = ConstantOperand(np.int32(0))
        op1.result = SignalOperand(net, Signal.SIGNAL_B)
        self.assertNotEqual(op1, op2)
        op1.result = SignalOperand(net, Signal.SIGNAL_A)
        self.assertEqual(op1, op2)

    def test_set_left(self):
        net = Network()
        op = Operation(NumericOperator.ADD, SignalOperand(net, Signal.SIGNAL_A))
        op.right = SignalOperand(net, Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(net, Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(net, Signal.SIGNAL_ANYTHING)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(net, Signal.SIGNAL_EVERYTHING)
        op.left = SignalOperand(net, Signal.SIGNAL_A)
        op.right = SignalOperand(net, Signal.SIGNAL_A)
        op.left = SignalOperand(net, Signal.SIGNAL_EACH)
        op.right = ConstantOperand(np.int32(10))
        op.left = SignalOperand(net, Signal.SIGNAL_EACH)
        op.result = SignalOperand(net, Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(net, Signal.SIGNAL_A)

    def test_right(self):
        net = Network()
        op = Operation(NumericOperator.ADD, SignalOperand(net, Signal.SIGNAL_A))
        op.left = SignalOperand(net, Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(net, Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(net, Signal.SIGNAL_ANYTHING)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(net, Signal.SIGNAL_EVERYTHING)
        op.right = SignalOperand(net, Signal.SIGNAL_A)
        op.left = SignalOperand(net, Signal.SIGNAL_A)
        op.right = SignalOperand(net, Signal.SIGNAL_EACH)
        op.left = ConstantOperand(np.int32(10))
        op.right = SignalOperand(net, Signal.SIGNAL_EACH)
        op.result = SignalOperand(net, Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(net, Signal.SIGNAL_A)

    def test_set_result(self):
        net = Network()
        op = Operation(NumericOperator.ADD, SignalOperand(net, Signal.SIGNAL_A))
        with self.assertRaises(AssertionError):
            op.result = SignalOperand(net, Signal.SIGNAL_EACH)
        op.right = SignalOperand(net, Signal.SIGNAL_EACH)
        op.result = SignalOperand(net, Signal.SIGNAL_EACH)
        op.result = SignalOperand(net, Signal.SIGNAL_A)
        op.right = SignalOperand(net, Signal.SIGNAL_A)
        op.left = SignalOperand(net, Signal.SIGNAL_EACH)
        op.result = SignalOperand(net, Signal.SIGNAL_EACH)
        op.result = SignalOperand(net, Signal.SIGNAL_A)
        op.left = SignalOperand(net, Signal.SIGNAL_A)
        with self.assertRaises(AssertionError):
            op.result = SignalOperand(net, Signal.SIGNAL_EVERYTHING)
        with self.assertRaises(AssertionError):
            op.result = SignalOperand(net, Signal.SIGNAL_ANYTHING)
