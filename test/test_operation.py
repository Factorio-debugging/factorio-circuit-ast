import unittest

from factorio_circuit_ast.NetworkLibrary import NetworkLibrary, NetworkType
from factorio_circuit_ast.Operation import *

lib: NetworkLibrary = NetworkLibrary()


class TestNumericOperator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(NumericOperator.ADD.calculate(np.int32(1), np.int32(2)), 3)
        with self.assertWarns(RuntimeWarning):
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

    def test_ir_repr(self):
        self.assertEqual(NumericOperator.ADD.to_ir(), "add")
        self.assertEqual(NumericOperator.SUBTRACT.to_ir(), "sub")
        self.assertEqual(NumericOperator.MULTIPLY.to_ir(), "mult")
        self.assertEqual(NumericOperator.DIVIDE.to_ir(), "div")
        self.assertEqual(NumericOperator.MODULO.to_ir(), "mod")
        self.assertEqual(NumericOperator.EXPONENT.to_ir(), "exp")
        self.assertEqual(NumericOperator.LEFT_BIT_SHIFT.to_ir(), "lsh")
        self.assertEqual(NumericOperator.RIGHT_BIT_SHIFT.to_ir(), "rsh")
        self.assertEqual(NumericOperator.AND.to_ir(), "and")
        self.assertEqual(NumericOperator.OR.to_ir(), "or")
        self.assertEqual(NumericOperator.XOR.to_ir(), "xor")


def get_nets() -> DoubleNetwork:
    r_net = lib.add_network(NetworkType.RED)
    g_net = lib.add_network(NetworkType.GREEN)
    d_net = DoubleNetwork(r_net, g_net)
    return d_net


class TestOperation(unittest.TestCase):
    def test_constructor(self):
        i_net = get_nets()
        o_net = get_nets()
        op = Operation(NumericOperator.OR, SignalOperand(Signal.SIGNAL_A))
        self.assertEqual(op.operation, NumericOperator.OR)
        self.assertEqual(op.left, ConstantOperand(np.int32(0)))
        self.assertEqual(op.right, ConstantOperand(np.int32(0)))
        self.assertEqual(op.result, SignalOperand(Signal.SIGNAL_A))
        self.assertIsNone(op.previous_result)
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_RED),
            o_net,
            i_net,
            SignalOperand(Signal.SIGNAL_EACH),
            SignalOperand(Signal.SIGNAL_CYAN),
        )
        self.assertEqual(op.left, SignalOperand(Signal.SIGNAL_EACH))
        self.assertEqual(op.right, SignalOperand(Signal.SIGNAL_CYAN))
        self.assertEqual(op.input_network, i_net)
        self.assertEqual(op.output_network, o_net)
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_RED),
            i_net,
            o_net,
            ConstantOperand(np.int32(10)),
            ConstantOperand(np.int32(20)),
        )
        self.assertEqual(op.left, ConstantOperand(np.int32(10)))
        self.assertEqual(op.right, ConstantOperand(np.int32(20)))

    def test_eq(self):
        i_net = get_nets()
        o_net = get_nets()
        op1 = Operation(NumericOperator.OR, SignalOperand(Signal.SIGNAL_A))
        op2 = Operation(NumericOperator.ADD, SignalOperand(Signal.SIGNAL_A))
        self.assertNotEqual(op1, ConstantOperand(np.int32(2)))
        self.assertNotEqual(op1, op2)
        op2.operation = NumericOperator.OR
        op1.left = ConstantOperand(np.int32(10))
        self.assertNotEqual(op1, op2)
        op1.left = ConstantOperand(np.int32(0))
        op2.right = ConstantOperand(np.int32(50))
        self.assertNotEqual(op1, op2)
        op2.right = ConstantOperand(np.int32(0))
        op1.result = SignalOperand(Signal.SIGNAL_B)
        self.assertNotEqual(op1, op2)
        op1.result = SignalOperand(Signal.SIGNAL_A)
        op2.output_network = o_net
        self.assertNotEqual(op1, op2)
        op1.output_network = o_net
        op1.input_network = i_net
        self.assertNotEqual(op1, op2)
        op2.input_network = i_net
        self.assertEqual(op1, op2)

    def test_set_left(self):
        op = Operation(NumericOperator.ADD, SignalOperand(Signal.SIGNAL_A))
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(Signal.SIGNAL_A)
        i_net = get_nets()
        op.input_network = i_net
        op.right = SignalOperand(Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(Signal.SIGNAL_ANYTHING)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(Signal.SIGNAL_EVERYTHING)
        op.left = SignalOperand(Signal.SIGNAL_A)
        op.right = SignalOperand(Signal.SIGNAL_A)
        op.left = SignalOperand(Signal.SIGNAL_EACH)
        op.right = ConstantOperand(np.int32(10))
        op.left = SignalOperand(Signal.SIGNAL_EACH)
        op.result = SignalOperand(Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.left = SignalOperand(Signal.SIGNAL_A)

    def test_right(self):
        op = Operation(NumericOperator.ADD, SignalOperand(Signal.SIGNAL_A))
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(Signal.SIGNAL_A)
        i_net = get_nets()
        op.input_network = i_net
        op.left = SignalOperand(Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(Signal.SIGNAL_ANYTHING)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(Signal.SIGNAL_EVERYTHING)
        op.right = SignalOperand(Signal.SIGNAL_A)
        op.left = SignalOperand(Signal.SIGNAL_A)
        op.right = SignalOperand(Signal.SIGNAL_EACH)
        op.left = ConstantOperand(np.int32(10))
        op.right = SignalOperand(Signal.SIGNAL_EACH)
        op.result = SignalOperand(Signal.SIGNAL_EACH)
        with self.assertRaises(AssertionError):
            op.right = SignalOperand(Signal.SIGNAL_A)

    def test_set_result(self):
        i_net = get_nets()
        op = Operation(
            NumericOperator.ADD, SignalOperand(Signal.SIGNAL_A), input_network=i_net
        )
        with self.assertRaises(AssertionError):
            op.result = SignalOperand(Signal.SIGNAL_EACH)
        op.right = SignalOperand(Signal.SIGNAL_EACH)
        op.result = SignalOperand(Signal.SIGNAL_EACH)
        op.result = SignalOperand(Signal.SIGNAL_A)
        op.right = SignalOperand(Signal.SIGNAL_A)
        op.left = SignalOperand(Signal.SIGNAL_EACH)
        op.result = SignalOperand(Signal.SIGNAL_EACH)
        op.result = SignalOperand(Signal.SIGNAL_A)
        op.left = SignalOperand(Signal.SIGNAL_A)
        with self.assertRaises(AssertionError):
            op.result = SignalOperand(Signal.SIGNAL_EVERYTHING)
        with self.assertRaises(AssertionError):
            op.result = SignalOperand(Signal.SIGNAL_ANYTHING)

    def test_tick_constant(self):
        o_net = get_nets()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_A),
            o_net,
            left=ConstantOperand(np.int32(10)),
            right=ConstantOperand(np.int32(10)),
        )
        op.tick()
        o_net.red.tick()
        self.assertEqual(o_net.get_signal(Signal.SIGNAL_A), 20)
        self.assertEqual(op.previous_result, {Signal.SIGNAL_A: 20})

    def test_tick_left_each_and_output_each(self):
        o_net = get_nets()
        i_net = get_nets()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_EACH),
            o_net,
            i_net,
            SignalOperand(Signal.SIGNAL_EACH),
            ConstantOperand(np.int32(10)),
        )
        i_net.update_signal(Signal.WATER, np.int32(10))
        i_net.update_signal(Signal.SIGNAL_RED, np.int32(20))
        i_net.red.tick()
        op.tick()
        o_net.red.tick()
        self.assertEqual(o_net.get_signals(), {Signal.WATER: 20, Signal.SIGNAL_RED: 30})

    def test_tick_right_each_and_output_each(self):
        o_net = get_nets()
        i_net = get_nets()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_EACH),
            o_net,
            i_net,
            ConstantOperand(np.int32(10)),
            SignalOperand(Signal.SIGNAL_EACH),
        )
        i_net.update_signal(Signal.WATER, np.int32(10))
        i_net.update_signal(Signal.SIGNAL_RED, np.int32(20))
        i_net.red.tick()
        op.tick()
        o_net.red.tick()
        self.assertEqual(o_net.get_signals(), {Signal.WATER: 20, Signal.SIGNAL_RED: 30})

    def test_tick_no_each_and_output_each(self):
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_CYAN),
            left=ConstantOperand(np.int32(10)),
            right=ConstantOperand(np.int32(10)),
        )
        op.result.signal = Signal.SIGNAL_EACH
        with self.assertRaises(AssertionError):
            op.tick()

    def test_tick_left_each_and_output_no_each(self):
        o_net = get_nets()
        i_net = get_nets()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_PINK),
            o_net,
            i_net,
            SignalOperand(Signal.SIGNAL_EACH),
            ConstantOperand(np.int32(10)),
        )
        i_net.update_signal(Signal.WATER, np.int32(10))
        i_net.update_signal(Signal.SIGNAL_RED, np.int32(20))
        i_net.red.tick()
        op.tick()
        o_net.red.tick()
        self.assertEqual(o_net.get_signal(Signal.SIGNAL_PINK), 50)

    def test_tick_right_each_and_output_no_each(self):
        o_net = get_nets()
        i_net = get_nets()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_WHITE),
            o_net,
            i_net,
            ConstantOperand(np.int32(10)),
            SignalOperand(Signal.SIGNAL_EACH),
        )
        i_net.update_signal(Signal.WATER, np.int32(10))
        i_net.update_signal(Signal.SIGNAL_RED, np.int32(20))
        i_net.red.tick()
        op.tick()
        o_net.red.tick()
        self.assertEqual(o_net.get_signal(Signal.SIGNAL_WHITE), 50)

    def test_calculate_signals(self):
        o_net = get_nets()
        i_net = get_nets()
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_WHITE),
            o_net,
            i_net,
            ConstantOperand(np.int32(10)),
            SignalOperand(Signal.WATER),
        )
        i_net.update_signal(Signal.WATER, np.int32(10))
        i_net.update_signal(Signal.SIGNAL_RED, np.int32(20))
        i_net.red.tick()
        op.tick()
        o_net.red.tick()
        self.assertEqual(o_net.get_signal(Signal.SIGNAL_WHITE), 20)

    def test_no_output_net(self):
        op = Operation(
            NumericOperator.ADD,
            SignalOperand(Signal.SIGNAL_A),
            left=ConstantOperand(np.int32(10)),
        )
        op.tick()
        self.assertEqual(op.previous_result, {Signal.SIGNAL_A: 10})

    def test_cli_repr(self):
        o_net = get_nets()
        i_net = get_nets()
        op = Operation(NumericOperator.ADD, SignalOperand(Signal.SIGNAL_A))
        self.assertEqual(
            op.cli_repr(), "Operation input=- output=- (0 + 0) -> signal-A"
        )
        op = Operation(
            NumericOperator.DIVIDE,
            SignalOperand(Signal.SIGNAL_WHITE),
            o_net,
            i_net,
            ConstantOperand(np.int32(10)),
            SignalOperand(Signal.WATER),
        )
        self.assertEqual(
            op.cli_repr(),
            f"Operation input={i_net.cli_repr()} output={o_net.cli_repr()} (10 / water) -> signal-white",
        )

    def test_ir_repr(self):
        o_net = get_nets()
        i_net = get_nets()
        op = Operation(NumericOperator.ADD, SignalOperand(Signal.SIGNAL_A))
        self.assertEqual(op.to_ir(), "op op=add res=signal-A left=0 right=0")
        op = Operation(
            NumericOperator.DIVIDE,
            SignalOperand(Signal.SIGNAL_WHITE),
            o_net,
            i_net,
            ConstantOperand(np.int32(10)),
            SignalOperand(Signal.WATER),
        )
        self.assertEqual(
            op.to_ir(),
            f"op op=div res=signal-white left=10 right=water {i_net.ir_repr('in')[:-1]} {o_net.ir_repr('out')[:-1]}",
        )
