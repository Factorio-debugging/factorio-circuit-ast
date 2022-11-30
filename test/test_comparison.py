import unittest

from factorio_circuit_ast.AST.Comparison import *
from factorio_circuit_ast.AST.Signal import Signal, Signals
from factorio_circuit_ast.Network.NetworkLibrary import NetworkLibrary, NetworkType

lib: NetworkLibrary = NetworkLibrary()


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

    def test_ir_repr(self):
        self.assertEqual(DeciderOperator.EQUAL.to_ir(), "eq")
        self.assertEqual(DeciderOperator.NOT_EQUAL.to_ir(), "nq")
        self.assertEqual(DeciderOperator.GREATER_OR_EQUAL.to_ir(), "gq")
        self.assertEqual(DeciderOperator.GREATER_THAN.to_ir(), "gt")
        self.assertEqual(DeciderOperator.LESS_OR_EQUAL.to_ir(), "lq")
        self.assertEqual(DeciderOperator.LESS_THAN.to_ir(), "lt")


def get_nets() -> DoubleNetwork:
    r_net = lib.add_network(NetworkType.RED)
    g_net = lib.add_network(NetworkType.GREEN)
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
        self.assertEqual(cmp, i_net.red.dependants[0]())
        self.assertEqual(cmp, i_net.green.dependants[0]())
        self.assertEqual(cmp, o_net.red.depends[0]())
        self.assertEqual(cmp, o_net.green.depends[0]())
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
            if input_o.wildcard():
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

    def test_result_setter_no_network(self):
        with self.assertRaises(AssertionError):
            Comparison(DeciderOperator.EQUAL, SignalOperand(Signal.SIGNAL_EVERYTHING))

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

    def test_previous_result_after_tick(self):
        o_net = get_nets()
        cmp = Comparison(DeciderOperator.EQUAL, SignalOperand(Signal.SIGNAL_A), o_net)
        cmp.tick()
        o_net.red.tick()
        self.assertEqual(cmp.previous_result, o_net.get_signals())

    def test_compare_constant(self):
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
            left=ConstantOperand(np.int32(10)),
            right=ConstantOperand(np.int32(20)),
            copy_count_from_input=False,
        )
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})
        cmp.right = ConstantOperand(np.int32(10))
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})

    def test_compare_constant_result_everything(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_EVERYTHING),
            o_net,
            i_net,
            left=ConstantOperand(np.int32(10)),
            right=ConstantOperand(np.int32(10)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: 20,
            Signal.SIGNAL_E: 30,
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {s: 1 for s in sig.keys()})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(cmp.previous_result, sig)

    def test_compare_everything(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.GREATER_THAN,
            SignalOperand(Signal.SIGNAL_A),
            o_net,
            i_net,
            left=SignalOperand(Signal.SIGNAL_EVERYTHING),
            right=ConstantOperand(np.int32(5)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: 10,
            Signal.SIGNAL_R: 20,
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1})
        cmp.result.signal = Signal.SIGNAL_R
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 1})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 20})
        cmp.result.signal = Signal.SIGNAL_A
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 10})
        cmp.operation = DeciderOperator.EQUAL
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})

    def test_compare_everything_result_everything(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.GREATER_THAN,
            SignalOperand(Signal.SIGNAL_EVERYTHING),
            o_net,
            i_net,
            left=SignalOperand(Signal.SIGNAL_EVERYTHING),
            right=ConstantOperand(np.int32(5)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: 10,
            Signal.SIGNAL_R: 20,
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {s: 1 for s in sig.keys()})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(cmp.previous_result, sig)
        cmp.operation = DeciderOperator.EQUAL
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})
        cmp.operation = DeciderOperator.GREATER_THAN
        cmp.right = SignalOperand(Signal.SIGNAL_A)
        cmp.tick()
        self.assertEqual(cmp.previous_result, sig)

    def test_compare_anything(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
            o_net,
            i_net,
            left=SignalOperand(Signal.SIGNAL_ANYTHING),
            right=ConstantOperand(np.int32(10)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: 10,
            Signal.SIGNAL_R: 20,
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1})
        cmp.result.signal = Signal.SIGNAL_R
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 1})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 20})
        cmp.right = ConstantOperand(np.int32(5))
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})
        i_net.update_signal(Signal.SIGNAL_A, np.int32(10))
        i_net.red.tick()
        cmp.right = SignalOperand(Signal.SIGNAL_A)
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})

    def test_compare_anything_result_anything(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_ANYTHING),
            o_net,
            i_net,
            left=SignalOperand(Signal.SIGNAL_ANYTHING),
            right=ConstantOperand(np.int32(10)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: 10,
            Signal.SIGNAL_R: 20,
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1})
        # TODO: Implement deterministic order and test order
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 10})
        cmp.right = ConstantOperand(np.int32(5))
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})

    def test_compare_anything_result_everything(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_EVERYTHING),
            o_net,
            i_net,
            left=SignalOperand(Signal.SIGNAL_ANYTHING),
            right=ConstantOperand(np.int32(10)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: 10,
            Signal.SIGNAL_R: 20,
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1, Signal.SIGNAL_R: 1})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(
            cmp.previous_result, {Signal.SIGNAL_A: 10, Signal.SIGNAL_R: 20}
        )
        cmp.right = ConstantOperand(np.int32(5))
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})

    def test_compare_each(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
            o_net,
            i_net,
            left=SignalOperand(Signal.SIGNAL_EACH),
            right=ConstantOperand(np.int32(10)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: np.int32(10),
            Signal.SIGNAL_R: np.int32(20),
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1})
        cmp.result.signal = Signal.SIGNAL_R
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 1})
        sig[Signal.SIGNAL_E] = np.int32(10)
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 2})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 20})
        cmp.right = ConstantOperand(np.int32(5))
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})
        cmp.right = SignalOperand(Signal.SIGNAL_A)
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_R: 20})

    def test_compare_each_result_each(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_EACH),
            o_net,
            i_net,
            left=SignalOperand(Signal.SIGNAL_EACH),
            right=ConstantOperand(np.int32(10)),
            copy_count_from_input=False,
        )
        sig: Signals = {
            Signal.SIGNAL_A: np.int32(10),
            Signal.SIGNAL_R: np.int32(20),
        }
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1})
        sig[Signal.SIGNAL_E] = np.int32(10)
        i_net.update_signals(sig)
        i_net.red.tick()
        cmp.tick()
        self.assertEqual(cmp.previous_result, {Signal.SIGNAL_A: 1, Signal.SIGNAL_E: 1})
        cmp.copy_count_from_input = True
        cmp.tick()
        self.assertEqual(
            cmp.previous_result, {Signal.SIGNAL_A: 10, Signal.SIGNAL_E: 10}
        )
        cmp.right = ConstantOperand(np.int32(5))
        cmp.tick()
        self.assertEqual(cmp.previous_result, {})

    def test_cli_repr(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
        )
        self.assertEqual(
            cmp.cli_repr(), "Comparison input=- output=- (0 = 0) -> signal-A (copy)"
        )
        cmp = Comparison(
            DeciderOperator.GREATER_THAN,
            SignalOperand(Signal.SIGNAL_R),
            o_net,
            i_net,
            SignalOperand(Signal.SIGNAL_B),
            ConstantOperand(np.int32(5)),
            False,
        )
        self.assertEqual(
            cmp.cli_repr(),
            f"Comparison input={i_net.cli_repr()} output={o_net.cli_repr()} (signal-B > 5) -> signal-R (no_copy)",
        )

    def test_ir_repr(self):
        o_net = get_nets()
        i_net = get_nets()
        cmp = Comparison(
            DeciderOperator.EQUAL,
            SignalOperand(Signal.SIGNAL_A),
        )
        self.assertEqual(
            cmp._inner_to_ir(), "comp op=eq res=signal-A left=0 right=0 cpy"
        )
        cmp = Comparison(
            DeciderOperator.GREATER_THAN,
            SignalOperand(Signal.SIGNAL_R),
            o_net,
            i_net,
            SignalOperand(Signal.SIGNAL_B),
            ConstantOperand(np.int32(5)),
            False,
        )
        self.assertEqual(
            cmp._inner_to_ir(),
            f"comp op=gt res=signal-R left=signal-B right=5 {i_net.ir_repr('in')[:-1]} {o_net.ir_repr('out')[:-1]}",
        )
