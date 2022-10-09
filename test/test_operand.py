import unittest

from factorio_circuit_ast.Operand import *


class TestSignalOperand(unittest.TestCase):
    def test_constructor(self):
        sig = Signal.SIGNAL_A
        op = SignalOperand(sig)
        self.assertEqual(op.signal, sig)

    def test_eq(self):
        op1 = SignalOperand(Signal.SIGNAL_A)
        op2 = SignalOperand(Signal.SIGNAL_B)
        self.assertNotEqual(op1, op2)
        op2.signal = Signal.SIGNAL_A
        self.assertNotEqual(op1, None)
        self.assertEqual(op1, op2)

    def test_abstract(self):
        op = SignalOperand(Signal.SIGNAL_A)
        self.assertEqual(op.wildcard(), False)
        op.signal = Signal.SIGNAL_EACH
        self.assertEqual(op.wildcard(), True)
        op.signal = Signal.SIGNAL_EVERYTHING
        self.assertEqual(op.wildcard(), True)
        op.signal = Signal.SIGNAL_ANYTHING
        self.assertEqual(op.wildcard(), True)
        op.signal = Signal.WATER
        self.assertEqual(op.wildcard(), False)

    def test_each(self):
        op = SignalOperand(Signal.SIGNAL_A)
        self.assertEqual(op.is_each(), False)
        op.signal = Signal.SIGNAL_EACH
        self.assertEqual(op.is_each(), True)
        op.signal = Signal.SIGNAL_EVERYTHING
        self.assertEqual(op.is_each(), False)
        op.signal = Signal.SIGNAL_ANYTHING
        self.assertEqual(op.is_each(), False)
        op.signal = Signal.WATER
        self.assertEqual(op.is_each(), False)

    def test_anything(self):
        op = SignalOperand(Signal.SIGNAL_A)
        self.assertEqual(op.is_anything(), False)
        op.signal = Signal.SIGNAL_EACH
        self.assertEqual(op.is_anything(), False)
        op.signal = Signal.SIGNAL_EVERYTHING
        self.assertEqual(op.is_anything(), False)
        op.signal = Signal.SIGNAL_ANYTHING
        self.assertEqual(op.is_anything(), True)
        op.signal = Signal.WATER
        self.assertEqual(op.is_anything(), False)

    def test_everything(self):
        op = SignalOperand(Signal.SIGNAL_A)
        self.assertEqual(op.is_everything(), False)
        op.signal = Signal.SIGNAL_EACH
        self.assertEqual(op.is_everything(), False)
        op.signal = Signal.SIGNAL_EVERYTHING
        self.assertEqual(op.is_everything(), True)
        op.signal = Signal.SIGNAL_ANYTHING
        self.assertEqual(op.is_everything(), False)
        op.signal = Signal.WATER
        self.assertEqual(op.is_everything(), False)


class TestConstantOperand(unittest.TestCase):
    def test_constructor(self):
        op = ConstantOperand(np.int32(10))
        self.assertEqual(op.constant, 10)

    def test_eq(self):
        op1 = ConstantOperand(np.int32(10))
        op2 = ConstantOperand(np.int32(20))
        self.assertNotEqual(op1, op2)
        op3 = SignalOperand(Signal.SIGNAL_A)
        self.assertNotEqual(op1, op3)
        op2.constant = 10
        self.assertEqual(op1, op2)

    def test_abstract(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.wildcard(), False)

    def test_each(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.is_each(), False)

    def test_anything(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.is_anything(), False)

    def test_everything(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.is_everything(), False)
