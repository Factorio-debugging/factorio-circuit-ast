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
        net.update_value(sig, np.int32(10))
        net.tick()
        self.assertEqual(op.value(), 10)
        net.update_value(Signal.SIGNAL_B, np.int32(10))
        net.tick()
        self.assertEqual(op.value(), 0)

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
