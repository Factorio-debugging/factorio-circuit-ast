import unittest

from AST.Network import Network
from AST.Operation import *


class TestNumericOperator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(NumericOperator.ADD.calculate(np.int32(1), np.int32(2)), 3)
        self.assertEqual(
            NumericOperator.ADD.calculate(np.int32(2**31 - 1), np.int32(1)),
            -(2**31),
        )

    def test_subtract(self):
        self.assertEqual(
            NumericOperator.SUBTRACT.calculate(np.int32(2), np.int32(1)), 1
        )
        self.assertEqual(
            NumericOperator.SUBTRACT.calculate(np.int32(1), np.int32(2)), -1
        )

    def test_multiply(self):
        self.assertEqual(
            NumericOperator.MULTIPLY.calculate(np.int32(9), np.int32(9)), 81
        )

    def test_divide(self):
        self.assertEqual(NumericOperator.DIVIDE.calculate(np.int32(10), np.int32(2)), 5)
        self.assertEqual(
            NumericOperator.DIVIDE.calculate(np.int32(10), np.int32(11)), 0
        )

    def test_modulo(self):
        self.assertEqual(
            NumericOperator.MODULO.calculate(np.int32(10), np.int32(11)), 10
        )
        self.assertEqual(NumericOperator.MODULO.calculate(np.int32(10), np.int32(5)), 0)

    def test_exponent(self):
        self.assertEqual(
            NumericOperator.EXPONENT.calculate(np.int32(2), np.int32(31)), -(2**31)
        )

    def test_left_bit_shift(self):
        self.assertEqual(
            NumericOperator.LEFT_BIT_SHIFT.calculate(np.int32(8), np.int32(3)), 64
        )

    def test_right_bit_shift(self):
        self.assertEqual(
            NumericOperator.RIGHT_BIT_SHIFT.calculate(np.int32(8), np.int32(3)), 1
        )

    def test_and(self):
        self.assertEqual(NumericOperator.AND.calculate(np.int32(15), np.int32(22)), 6)

    def test_or(self):
        self.assertEqual(NumericOperator.OR.calculate(np.int32(15), np.int32(22)), 31)

    def test_xor(self):
        self.assertEqual(NumericOperator.XOR.calculate(np.int32(15), np.int32(22)), 25)


class TestOperation(unittest.TestCase):
    def test_constructor(self):
        net = Network()
        op = Operation(NumericOperator.OR, SignalOperand(net, Signal.SIGNAL_A))
        self.assertEqual(op.operation, NumericOperator.OR)
        self.assertEqual(op.left, ConstantOperand(np.int32(0)))
        self.assertEqual(op.right, ConstantOperand(np.int32(0)))
        self.assertEqual(op.result, SignalOperand(net, Signal.SIGNAL_A))
        self.assertIsNone(op.previous_result)
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(net, Signal.SIGNAL_RED),
            SignalOperand(net, Signal.SIGNAL_EACH),
            SignalOperand(net, Signal.SIGNAL_CYAN),
        )
        self.assertEqual(op.left, SignalOperand(net, Signal.SIGNAL_EACH))
        self.assertEqual(op.right, SignalOperand(net, Signal.SIGNAL_CYAN))
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(net, Signal.SIGNAL_RED),
            ConstantOperand(np.int32(10)),
            ConstantOperand(np.int32(20)),
        )
        self.assertEqual(op.left, ConstantOperand(np.int32(10)))
        self.assertEqual(op.right, ConstantOperand(np.int32(20)))

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

    def test_tick_constant(self):
        net = Network()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(net, Signal.SIGNAL_A),
            ConstantOperand(np.int32(10)),
            ConstantOperand(np.int32(10)),
        )
        op.tick()
        net.tick()
        self.assertEqual(net.get_signal_value(Signal.SIGNAL_A), 20)
        self.assertEqual(op.previous_result, {Signal.SIGNAL_A: 20})

    def test_tick_left_each_and_output_each(self):
        out_net = Network()
        left_net = Network()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(out_net, Signal.SIGNAL_EACH),
            SignalOperand(left_net, Signal.SIGNAL_EACH),
            ConstantOperand(np.int32(10)),
        )
        left_net.update_value(Signal.WATER, np.int32(10))
        left_net.update_value(Signal.SIGNAL_RED, np.int32(20))
        left_net.tick()
        op.tick()
        out_net.tick()
        self.assertEqual(
            out_net.get_all_values(), {Signal.WATER: 20, Signal.SIGNAL_RED: 30}
        )

    def test_tick_right_each_and_output_each(self):
        out_net = Network()
        right_net = Network()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(out_net, Signal.SIGNAL_EACH),
            ConstantOperand(np.int32(10)),
            SignalOperand(right_net, Signal.SIGNAL_EACH),
        )
        right_net.update_value(Signal.WATER, np.int32(10))
        right_net.update_value(Signal.SIGNAL_RED, np.int32(20))
        right_net.tick()
        op.tick()
        out_net.tick()
        self.assertEqual(
            out_net.get_all_values(), {Signal.WATER: 20, Signal.SIGNAL_RED: 30}
        )

    def test_tick_no_each_and_output_each(self):
        net = Network()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(net, Signal.SIGNAL_CYAN),
            ConstantOperand(np.int32(10)),
            ConstantOperand(np.int32(10)),
        )
        op.result.signal = Signal.SIGNAL_EACH
        with self.assertRaises(AssertionError):
            op.tick()

    def test_tick_left_each_and_output_no_each(self):
        out_net = Network()
        left_net = Network()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(out_net, Signal.SIGNAL_PINK),
            SignalOperand(left_net, Signal.SIGNAL_EACH),
            ConstantOperand(np.int32(10)),
        )
        left_net.update_value(Signal.WATER, np.int32(10))
        left_net.update_value(Signal.SIGNAL_RED, np.int32(20))
        left_net.tick()
        op.tick()
        out_net.tick()
        self.assertEqual(out_net.get_signal_value(Signal.SIGNAL_PINK), 50)

    def test_tick_right_each_and_output_no_each(self):
        out_net = Network()
        right_net = Network()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(out_net, Signal.SIGNAL_WHITE),
            ConstantOperand(np.int32(10)),
            SignalOperand(right_net, Signal.SIGNAL_EACH),
        )
        right_net.update_value(Signal.WATER, np.int32(10))
        right_net.update_value(Signal.SIGNAL_RED, np.int32(20))
        right_net.tick()
        op.tick()
        out_net.tick()
        self.assertEqual(out_net.get_signal_value(Signal.SIGNAL_WHITE), 50)
