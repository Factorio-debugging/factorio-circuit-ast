import unittest

from AST.Network import *
from AST.Signal import Signals


class TestNetwork(unittest.TestCase):
    def test_constructor(self):
        net = Network()
        self.assertEqual(net._depends, [])
        self.assertEqual(net._dependants, [])
        self.assertEqual(net._previous_state, {})
        self.assertEqual(net._current_state, {})
        self.assertIsInstance(net.id, int)
        self.assertIs(networks[net.id], net)
        self.assertEqual(net.type, NetworkType.RED)
        net = Network(nid=1024, network=NetworkType.GREEN)
        self.assertEqual(net.id, 1024)
        self.assertIs(networks[1024], net)
        self.assertEqual(net.type, NetworkType.GREEN)

    def test_get_signal(self):
        net = Network()
        self.assertEqual(net.get_signal(Signal.ADVANCED_CIRCUIT), 0)
        with self.assertRaises(AssertionError):
            net.get_signal(Signal.SIGNAL_ANYTHING)

    def test_tick(self):
        net = Network()
        net._current_state[Signal.ADVANCED_CIRCUIT] = np.int32(10)
        net.tick()
        self.assertEqual(net.get_signal(Signal.ADVANCED_CIRCUIT), 10)

    def test_update_signal(self):
        net = Network()
        net.update_signal(Signal.SIGNAL_A, np.int32(10))
        with self.assertRaises(AssertionError):
            net.update_signal(Signal.SIGNAL_EVERYTHING, np.int32(0))
        self.assertEqual(net.get_signal(Signal.SIGNAL_A), 0)
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 10)
        net.tick()
        self.assertEqual(net.get_signal(Signal.SIGNAL_A), 10)
        self.assertNotIn(Signal.SIGNAL_A, net._current_state)
        net.update_signal(Signal.SIGNAL_A, np.int32(10))
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 10)
        net.update_signal(Signal.SIGNAL_A, np.int32(20))
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 30)
        net.update_signal(Signal.ADVANCED_CIRCUIT, np.int32(500))
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 30)
        self.assertEqual(net._current_state[Signal.ADVANCED_CIRCUIT], 500)
        net.tick()
        self.assertEqual(net.get_signal(Signal.SIGNAL_A), 30)
        self.assertEqual(net.get_signal(Signal.ADVANCED_CIRCUIT), 500)
        net.update_signal(Signal.SIGNAL_A, np.int32(2**31 - 1))
        net.update_signal(Signal.SIGNAL_A, np.int32(1))
        net.tick()
        self.assertEqual(net.get_signal(Signal.SIGNAL_A), -(2**31))
        self.assertIsInstance(net.get_signal(Signal.SIGNAL_A), np.int32)

    def test_get_signals(self):
        net = Network()
        self.assertEqual(net.get_signals(), {})
        net.update_signal(Signal.SIGNAL_A, np.int32(10))
        net.update_signal(Signal.SIGNAL_B, np.int32(30))
        self.assertEqual(net.get_signals(), {})
        net.tick()
        self.assertEqual(net.get_signals(), {Signal.SIGNAL_A: 10, Signal.SIGNAL_B: 30})
        self.assertTrue(
            all(isinstance(i, np.int32) for i in net.get_signals().values())
        )
        net.tick()
        self.assertEqual(net.get_signals(), {})

    def test_update_signals(self):
        net = Network()
        with self.assertRaises(AssertionError):
            net.update_signals({Signal.SIGNAL_EACH: 10})
        with self.assertRaises(AssertionError):
            net.update_signals({Signal.SIGNAL_EVERYTHING: 10})
        with self.assertRaises(AssertionError):
            net.update_signals({Signal.SIGNAL_ANYTHING: 10})
        values: Signals = {
            Signal.SIGNAL_A: 20,
            Signal.SIGNAL_B: 50,
        }
        net.update_signals(values)
        self.assertEqual(net.get_signals(), {})
        net.tick()
        self.assertEqual(net.get_signals(), values)

    def test_cli_repr(self):
        net = Network()
        self.assertEqual(net.cli_repr(), f"n{net.id}")
