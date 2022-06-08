import unittest

from AST.DoubleNetwork import *
from AST.Signal import Signals


class TestDoubleNetwork(unittest.TestCase):
    def test_constructor(self):
        d_net = DoubleNetwork()
        self.assertIsNone(d_net.red)
        self.assertIsNone(d_net.green)
        r_net = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        d_net = DoubleNetwork(r_net, g_net)
        self.assertIs(d_net.red, r_net)
        self.assertIs(d_net.green, g_net)
        with self.assertRaises(TypeError):
            DoubleNetwork(red=g_net)
        with self.assertRaises(TypeError):
            DoubleNetwork(green=r_net)

    def test_set_red(self):
        d_net = DoubleNetwork()
        with self.assertRaises(TypeError):
            d_net.red = Network(network=NetworkType.GREEN)
        r_net = Network(network=NetworkType.RED)
        d_net.red = r_net
        self.assertIs(d_net.red, r_net)
        d_net.red = None
        self.assertIsNone(d_net.red)

    def test_set_green(self):
        d_net = DoubleNetwork()
        with self.assertRaises(TypeError):
            d_net.green = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        d_net.green = g_net
        self.assertIs(d_net.green, g_net)
        d_net.green = None
        self.assertIsNone(d_net.green)

    def test_get_signal(self):
        d_net = DoubleNetwork()
        r_net = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        with self.assertRaises(AssertionError):
            d_net.get_signal(Signal.SIGNAL_EACH)
        self.assertEqual(d_net.get_signal(Signal.SIGNAL_A), 0)
        d_net.red = r_net
        d_net.green = g_net
        self.assertEqual(d_net.get_signal(Signal.SIGNAL_A), 0)
        r_net.update_signal(Signal.SIGNAL_A, np.int32(10))
        g_net.update_signal(Signal.SIGNAL_A, np.int32(20))
        g_net.update_signal(Signal.SIGNAL_B, np.int32(100))
        r_net.tick()
        g_net.tick()
        self.assertEqual(d_net.get_signal(Signal.SIGNAL_A), 30)
        self.assertIs(type(d_net.get_signal(Signal.SIGNAL_A)), np.int32)
        self.assertEqual(d_net.get_signal(Signal.SIGNAL_B), 100)
        self.assertIs(type(d_net.get_signal(Signal.SIGNAL_B)), np.int32)

    def test_get_signals(self):
        d_net = DoubleNetwork()
        r_net = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        self.assertEqual(d_net.get_signals(), {})
        d_net.red = r_net
        d_net.green = g_net
        self.assertEqual(d_net.get_signals(), {})
        r_net.update_signal(Signal.SIGNAL_A, np.int32(10))
        g_net.update_signal(Signal.SIGNAL_A, np.int32(20))
        g_net.update_signal(Signal.SIGNAL_B, np.int32(100))
        r_net.tick()
        g_net.tick()
        self.assertEqual(
            d_net.get_signals(), {Signal.SIGNAL_A: 30, Signal.SIGNAL_B: 100}
        )
        self.assertTrue(
            all(isinstance(i, np.int32) for i in d_net.get_signals().values())
        )

    def test_update_signal(self):
        r_net = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        d_net = DoubleNetwork(r_net, g_net)
        with self.assertRaises(AssertionError):
            d_net.update_signal(Signal.SIGNAL_EACH, np.int32(10))
        d_net.update_signal(Signal.ACCUMULATOR, np.int32(10))
        r_net.tick()
        g_net.tick()
        self.assertEqual(r_net.get_signal(Signal.ACCUMULATOR), 10)
        self.assertEqual(g_net.get_signal(Signal.ACCUMULATOR), 10)
        d_net.red = None
        d_net.update_signal(Signal.SIGNAL_A, np.int32(30))
        g_net.tick()
        self.assertEqual(g_net.get_signal(Signal.SIGNAL_A), 30)
        d_net.red = r_net
        d_net.green = None
        d_net.update_signal(Signal.SIGNAL_A, np.int32(50))
        r_net.tick()
        self.assertEqual(r_net.get_signal(Signal.SIGNAL_A), 50)

    def test_update_signals(self):
        r_net = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        d_net = DoubleNetwork(r_net, g_net)
        with self.assertRaises(AssertionError):
            d_net.update_signals({Signal.SIGNAL_EACH: np.int32(10)})
        signals: Signals = {
            Signal.SIGNAL_A: 10,
            Signal.SIGNAL_B: 30,
        }
        d_net.update_signals(signals)
        r_net.tick()
        g_net.tick()
        self.assertEqual(r_net.get_signals(), signals)
        self.assertEqual(g_net.get_signals(), signals)
        d_net.red = None
        d_net.update_signals(signals)
        g_net.tick()
        self.assertEqual(g_net.get_signals(), signals)
        d_net.red = r_net
        d_net.green = None
        d_net.update_signals(signals)
        r_net.tick()
        self.assertEqual(r_net.get_signals(), signals)

    def test_eq(self):
        r_net = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        net1 = DoubleNetwork()
        net2 = DoubleNetwork()
        self.assertNotEqual(net1, r_net)
        self.assertEqual(net1, net2)
        net1.red = r_net
        self.assertNotEqual(net1, net2)
        net2.red = r_net
        self.assertEqual(net1, net2)
        net2.green = g_net
        self.assertNotEqual(net1, net2)
        net1.green = g_net
        self.assertEqual(net1, net2)

    def test_cli_repr(self):
        r_net = Network(network=NetworkType.RED)
        g_net = Network(network=NetworkType.GREEN)
        net = DoubleNetwork()
        self.assertEqual(net.cli_repr(), "[r=-,g=-]")
        net.red = r_net
        self.assertEqual(net.cli_repr(), f"[r=n{r_net.id},g=-]")
        net.green = g_net
        self.assertEqual(net.cli_repr(), f"[r=n{r_net.id},g=n{g_net.id}]")
