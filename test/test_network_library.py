import unittest

from factorio_circuit_ast.Network.NetworkLibrary import *


class TestNetworkLibrary(unittest.TestCase):
    def test_constructor(self):
        lib = NetworkLibrary()
        self.assertEqual(lib.networks, {})

    def test_add_network(self):
        lib = NetworkLibrary()
        net = lib.add_network(NetworkType.RED)
        self.assertEqual(net.id, 1)
        self.assertIs(lib.networks[1], net)
        self.assertEqual(net.type, NetworkType.RED)
        net = lib.add_network(NetworkType.GREEN)
        self.assertEqual(net.id, 2)
        self.assertIs(lib.networks[2], net)
        self.assertEqual(net.type, NetworkType.GREEN)

    def test_contains(self):
        lib = NetworkLibrary()
        net = lib.add_network(NetworkType.RED)
        self.assertTrue(net in lib)
        net2 = Network(1, NetworkType.RED)
        self.assertFalse(net2 in lib)

    def test_getitem(self):
        lib = NetworkLibrary()
        net = lib.add_network(NetworkType.RED)
        self.assertIs(net, lib[1])

    def test_get_or_create(self):
        lib = NetworkLibrary()
        net = lib.add_network(NetworkType.RED)
        self.assertIs(lib.get_or_create_network(1, NetworkType.RED), net)
        with self.assertRaises(AssertionError):
            lib.get_or_create_network(1, NetworkType.GREEN)
        self.assertIsInstance(lib.get_or_create_network(2, NetworkType.GREEN), Network)
