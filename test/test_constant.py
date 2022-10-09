import unittest

import numpy as np

from factorio_circuit_ast.Constant import *
from factorio_circuit_ast.NetworkLibrary import NetworkLibrary, NetworkType
from factorio_circuit_ast.Signal import Signal

lib: NetworkLibrary = NetworkLibrary()


def get_nets() -> DoubleNetwork:
    r_net = lib.add_network(NetworkType.RED)
    g_net = lib.add_network(NetworkType.GREEN)
    d_net = DoubleNetwork(r_net, g_net)
    return d_net


class TestConstant(unittest.TestCase):
    def test_constructor(self):
        net = get_nets()
        const = Constant(net, {Signal.SIGNAL_A: np.int32(10)}, False)
        self.assertEqual(const.is_on, False)
        self.assertEqual(const.output_network, net)
        self.assertEqual(const.signals, {Signal.SIGNAL_A: 10})
        const = Constant()
        self.assertEqual(const.is_on, True)
        self.assertEqual(const.output_network, None)
        self.assertEqual(const.signals, {})

    def test_signals_setter(self):
        with self.assertRaises(AssertionError):
            Constant(signals={Signal.SIGNAL_EVERYTHING: np.int32(10)})

    def test_tick_on(self):
        net = get_nets()
        sig: Signals = {
            Signal.SIGNAL_A: np.int32(10),
            Signal.RAIL_SIGNAL: np.int32(20),
        }
        const = Constant(net, sig)
        const.tick()
        self.assertEqual(const.previous_result, sig)
        net.red.tick()
        self.assertEqual(net.get_signals(), sig)
        const.output_network = None
        const.tick()
        self.assertEqual(const.previous_result, sig)
        const.is_on = False
        const.tick()
        self.assertEqual(const.previous_result, {})

    def test_tick_off(self):
        net = get_nets()
        sig: Signals = {
            Signal.SIGNAL_A: np.int32(10),
            Signal.RAIL_SIGNAL: np.int32(20),
        }
        const = Constant(net, sig, False)
        const.tick()
        self.assertEqual(const.previous_result, {})
        net.red.tick()
        self.assertEqual(net.get_signals(), {})

    def test_cli_repr(self):
        net = get_nets()
        sig: Signals = {
            Signal.SIGNAL_A: np.int32(10),
            Signal.RAIL_SIGNAL: np.int32(20),
        }
        const = Constant(net, sig, False)
        self.assertEqual(
            const.cli_repr(),
            f"Constant output={net.cli_repr()} [signal-A: 10, rail-signal: 20] (off)",
        )
        const = Constant()
        self.assertEqual(const.cli_repr(), f"Constant output=- [] (on)")

    def test_ir_repr(self):
        net = get_nets()
        sig: Signals = {
            Signal.SIGNAL_A: np.int32(10),
            Signal.RAIL_SIGNAL: np.int32(20),
            Signal.ACCUMULATOR: np.int32(-10),
        }
        const = Constant(net, sig, False)
        self.assertEqual(
            const.to_ir(),
            f"const sig=signal-A=10 sig=rail-signal=20 sig=accumulator=-10 {net.ir_repr('out')[:-1]}",
        )
        const = Constant()
        self.assertEqual(const.to_ir(), f"const on")
