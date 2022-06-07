import unittest

from AST.Comparison import *
from AST.Network import Network, NetworkType
from AST.Signal import Signal


class TestDeciderOperator(unittest.TestCase):
    def test_calculate_greater_than(self):
        res = DeciderOperator.GREATER_THAN.calculate(np.int32(10), np.int32(20))
        self.assertEqual(res, False)
        self.assertIsInstance(res, np.int32)
        res = DeciderOperator.GREATER_THAN.calculate(np.int32(10), np.int32(10))
        self.assertEqual(res, False)

    def test_calculate_less_than(self):
        res = DeciderOperator.LESS_THAN.calculate(np.int32(10), np.int32(20))
        self.assertEqual(res, True)
        self.assertIsInstance(res, np.int32)
        res = DeciderOperator.LESS_THAN.calculate(np.int32(10), np.int32(10))
        self.assertEqual(res, False)

    def test_calculate_greater_or_equal(self):
        res = DeciderOperator.GREATER_OR_EQUAL.calculate(np.int32(10), np.int32(20))
        self.assertEqual(res, False)
        self.assertIsInstance(res, np.int32)
        res = DeciderOperator.GREATER_OR_EQUAL.calculate(np.int32(10), np.int32(10))
        self.assertEqual(res, True)

    def test_calculate_less_or_equal(self):
        res = DeciderOperator.LESS_OR_EQUAL.calculate(np.int32(10), np.int32(20))
        self.assertEqual(res, True)
        self.assertIsInstance(res, np.int32)
        res = DeciderOperator.LESS_OR_EQUAL.calculate(np.int32(10), np.int32(10))
        self.assertEqual(res, True)

    def test_calculate_equal(self):
        res = DeciderOperator.EQUAL.calculate(np.int32(10), np.int32(20))
        self.assertEqual(res, False)
        self.assertIsInstance(res, np.int32)
        res = DeciderOperator.EQUAL.calculate(np.int32(10), np.int32(10))
        self.assertEqual(res, True)

    def test_calculate_not_equal(self):
        res = DeciderOperator.NOT_EQUAL.calculate(np.int32(10), np.int32(20))
        self.assertEqual(res, True)
        self.assertIsInstance(res, np.int32)
        res = DeciderOperator.NOT_EQUAL.calculate(np.int32(10), np.int32(10))
        self.assertEqual(res, False)


def get_nets() -> DoubleNetwork:
    r_net = Network(network=NetworkType.RED)
    g_net = Network(network=NetworkType.GREEN)
    d_net = DoubleNetwork(r_net, g_net)
    return d_net


class TestComparison(unittest.TestCase):
    def test_constructor(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
        )
        self.assertEqual(cmp.result, SignalOperand(Signal.SIGNAL_A))
        self.assertEqual(cmp.operation, DeciderOperator.EQUAL)
        self.assertEqual(cmp.left, ConstantOperand(np.int32(0)))
        self.assertEqual(cmp.right, ConstantOperand(np.int32(0)))
        self.assertEqual(cmp.copy_count_from_input, True)
        self.assertEqual(cmp.input_network, None)
        self.assertEqual(cmp.output_network, None)
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
            o_net,
            i_net,
            SignalOperand(Signal.SIGNAL_RED),
            SignalOperand(Signal.SIGNAL_R),
            False,
        )
        self.assertEqual(cmp.result, SignalOperand(Signal.SIGNAL_A))
        self.assertEqual(cmp.operation, DeciderOperator.EQUAL)
        self.assertEqual(cmp.left, SignalOperand(Signal.SIGNAL_RED))
        self.assertEqual(cmp.right, SignalOperand(Signal.SIGNAL_R))
        self.assertEqual(cmp.copy_count_from_input, False)
        self.assertIs(cmp.input_network, i_net)
        self.assertIs(cmp.output_network, o_net)

    @staticmethod
    def setter_left_auto(input_o: Operand, output_o: SignalOperand):
        i_net = get_nets()
        o_net = get_nets()
        Comparison(
            DeciderOperator.EQUAL,
            output_o,
            o_net,
            i_net,
            left=input_o,
        )

    @staticmethod
    def setter_right_auto(input_o: Operand, output_o: SignalOperand):
        i_net = get_nets()
        o_net = get_nets()
        Comparison(
            DeciderOperator.EQUAL,
            output_o,
            o_net,
            i_net,
            right=input_o,
        )

    @staticmethod
    def setter_result_auto(input_o: Operand, output_o: SignalOperand):
        i_net = get_nets()
        o_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
            o_net,
            i_net,
            input_o,
        )
        cmp.result = output_o

    def setter_test_auto(self, input_o: Operand, output: Signal, is_ok: bool):
        output_o = SignalOperand(output)
        if not is_ok:
            with self.assertRaises(AssertionError):
                self.setter_left_auto(input_o, output_o)
            with self.assertRaises(AssertionError):
                self.setter_right_auto(input_o, output_o)
            with self.assertRaises(AssertionError):
                self.setter_result_auto(input_o, output_o)
        else:
            self.setter_left_auto(input_o, output_o)
            if input_o.abstract():
                with self.assertRaises(AssertionError):
                    self.setter_right_auto(input_o, output_o)
            else:
                self.setter_right_auto(input_o, output_o)
            self.setter_result_auto(input_o, output_o)

    def test_setter_output_everything(self):
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EACH), Signal.SIGNAL_EVERYTHING, False
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_ANYTHING), Signal.SIGNAL_EVERYTHING, True
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EVERYTHING), Signal.SIGNAL_EVERYTHING, True
        )
        self.setter_test_auto(
            ConstantOperand(np.int32(10)), Signal.SIGNAL_EVERYTHING, True
        )

    def test_setter_output_anything(self):
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EACH), Signal.SIGNAL_ANYTHING, False
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EVERYTHING), Signal.SIGNAL_ANYTHING, False
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_ANYTHING), Signal.SIGNAL_ANYTHING, True
        )
        self.setter_test_auto(
            ConstantOperand(np.int32(10)), Signal.SIGNAL_ANYTHING, False
        )

    def test_setter_output_each(self):
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EACH), Signal.SIGNAL_EACH, True
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EVERYTHING), Signal.SIGNAL_EACH, False
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_ANYTHING), Signal.SIGNAL_EACH, False
        )
        self.setter_test_auto(ConstantOperand(np.int32(10)), Signal.SIGNAL_EACH, False)

    def test_setter_output_normal(self):
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EACH), Signal.ACCUMULATOR, True
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_EVERYTHING), Signal.ACCUMULATOR, True
        )
        self.setter_test_auto(
            SignalOperand(Signal.SIGNAL_ANYTHING), Signal.ACCUMULATOR, True
        )
        self.setter_test_auto(ConstantOperand(np.int32(10)), Signal.ACCUMULATOR, True)

    def test_left_setter_no_network(self):
        with self.assertRaises(AssertionError):
            Comparison(
                DeciderOperator.EQUAL,
                SignalOperand(Signal.SIGNAL_A),
                left=SignalOperand(Signal.SIGNAL_RED),
            )

    def test_right_setter_no_network(self):
        with self.assertRaises(AssertionError):
            Comparison(
                DeciderOperator.EQUAL,
                SignalOperand(Signal.SIGNAL_A),
                right=SignalOperand(Signal.SIGNAL_A),
            )

    def test_eq(self):
        i_net = get_nets()
        o_net = get_nets()
        op1 = Comparison(DeciderOperator.EQUAL, SignalOperand(Signal.SIGNAL_A))
        op2 = Comparison(DeciderOperator.NOT_EQUAL, SignalOperand(Signal.SIGNAL_A))
        self.assertNotEqual(op1, ConstantOperand(np.int32(2)))
        self.assertNotEqual(op1, op2)
        op2.operation = DeciderOperator.EQUAL
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
        op2.copy_count_from_input = False
        self.assertNotEqual(op1, op2)
        op1.copy_count_from_input = False
        self.assertEqual(op1, op2)
