from AST.Network import *
import unittest


class TestNetwork(unittest.TestCase):
    def test_constructor(self):
        net = Network()
        self.assertEqual(net._depends, [])
        self.assertEqual(net._dependants, [])
        self.assertEqual(net._previous_state, {})
        self.assertEqual(net._current_state, {})
        self.assertIsInstance(net.id, int)
        self.assertIs(networks[net.id](), net)
        net = Network(nid=1024)
        self.assertEqual(net.id, 1024)
        self.assertIs(networks[1024](), net)

    def test_get_signal(self):
        net = Network()
        self.assertEqual(net.get_signal_value(Signal.ADVANCED_CIRCUIT), 0)

    def test_tick(self):
        net = Network()
        net._current_state[Signal.ADVANCED_CIRCUIT] = 10
        net.tick()
        self.assertEqual(net.get_signal_value(Signal.ADVANCED_CIRCUIT), 10)

    def test_update_value(self):
        net = Network()
        net.update_value(Signal.SIGNAL_A, 10)
        self.assertEqual(net.get_signal_value(Signal.SIGNAL_A), 0)
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 10)
        net.tick()
        self.assertEqual(net.get_signal_value(Signal.SIGNAL_A), 10)
        self.assertNotIn(Signal.SIGNAL_A, net._current_state)
        net.update_value(Signal.SIGNAL_A, 10)
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 10)
        net.update_value(Signal.SIGNAL_A, 20)
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 30)
        net.update_value(Signal.ADVANCED_CIRCUIT, 500)
        self.assertEqual(net._current_state[Signal.SIGNAL_A], 30)
        self.assertEqual(net._current_state[Signal.ADVANCED_CIRCUIT], 500)
        net.tick()
        self.assertEqual(net.get_signal_value(Signal.SIGNAL_A), 30)
        self.assertEqual(net.get_signal_value(Signal.ADVANCED_CIRCUIT), 500)

