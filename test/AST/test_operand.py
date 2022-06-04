import unittest

from AST.Operand import *


class TestSignalOperand(unittest.TestCase):
    def test_constructor(self):
        net = Network()
        sig = Signal.SIGNAL_A
        op = SignalOperand(net, sig)
        self.assertEqual(op.signal, sig)
        self.assertIs(op.network, net)
        self.assertIsInstance(op._network, ReferenceType)

    def test_network_dropped(self):
        net = Network()
        op = SignalOperand(net, Signal.SIGNAL_A)
        del net
        with self.assertRaises(RuntimeError):
            op.value()

    def test_value(self):
        net = Network()
        sig = Signal.SIGNAL_A
        op = SignalOperand(net, sig)
        self.assertEqual(op.value(), 0)
        net.update_signal(sig, np.int32(10))
        net.tick()
        self.assertEqual(op.value(), 10)
        net.update_signal(Signal.SIGNAL_B, np.int32(10))
        net.tick()
        self.assertEqual(op.value(), 0)
        op.signal = Signal.SIGNAL_EACH
        with self.assertRaises(AssertionError):
            op.value()

    def test_eq(self):
        net = Network()
        op1 = SignalOperand(net, Signal.SIGNAL_A)
        op2 = SignalOperand(net, Signal.SIGNAL_B)
        self.assertNotEqual(op1, op2)
        net2 = Network()
        op1.network = net2
        op2.signal = Signal.SIGNAL_A
        self.assertNotEqual(op1, op2)
        self.assertNotEqual(op1, net)
        op1.network = net
        self.assertEqual(op1, op2)

    def test_abstract(self):
        net = Network()
        op = SignalOperand(net, Signal.SIGNAL_A)
        self.assertEqual(op.abstract(), False)
        op.signal = Signal.SIGNAL_EACH
        self.assertEqual(op.abstract(), True)
        op.signal = Signal.SIGNAL_EVERYTHING
        self.assertEqual(op.abstract(), True)
        op.signal = Signal.SIGNAL_ANYTHING
        self.assertEqual(op.abstract(), True)
        op.signal = Signal.WATER
        self.assertEqual(op.abstract(), False)

    def test_each(self):
        net = Network()
        op = SignalOperand(net, Signal.SIGNAL_A)
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
        net = Network()
        op = SignalOperand(net, Signal.SIGNAL_A)
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
        net = Network()
        op = SignalOperand(net, Signal.SIGNAL_A)
        self.assertEqual(op.is_everything(), False)
        op.signal = Signal.SIGNAL_EACH
        self.assertEqual(op.is_everything(), False)
        op.signal = Signal.SIGNAL_EVERYTHING
        self.assertEqual(op.is_everything(), True)
        op.signal = Signal.SIGNAL_ANYTHING
        self.assertEqual(op.is_everything(), False)
        op.signal = Signal.WATER
        self.assertEqual(op.is_everything(), False)

    def test_update_self(self):
        net = Network()
        op = SignalOperand(net, Signal.SIGNAL_EVERYTHING)
        with self.assertRaises(AssertionError):
            op.update_self(np.int32(10))
        op.signal = Signal.WATER
        op.update_self(np.int32(10))
        net.tick()
        self.assertEqual(net.get_signal(Signal.WATER), 10)
        del net
        with self.assertRaises(RuntimeError):
            op.update_self(np.int32(10))


class TestConstantOperand(unittest.TestCase):
    def test_constructo(self):
        op = ConstantOperand(np.int32(10))
        self.assertEqual(op.constant, 10)

    def test_value(self):
        op = ConstantOperand(np.int32(20))
        self.assertEqual(op.value(), 20)

    def test_eq(self):
        op1 = ConstantOperand(np.int32(10))
        op2 = ConstantOperand(np.int32(20))
        self.assertNotEqual(op1, op2)
        op3 = SignalOperand(Network(), Signal.SIGNAL_A)
        self.assertNotEqual(op1, op3)
        op2.constant = 10
        self.assertEqual(op1, op2)

    def test_abstract(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.abstract(), False)

    def test_each(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.is_each(), False)

    def test_anything(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.is_anything(), False)

    def test_everything(self):
        op = ConstantOperand(np.int32(12))
        self.assertEqual(op.is_everything(), False)
