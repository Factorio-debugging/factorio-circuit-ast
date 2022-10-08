import unittest

from draftsman.classes.blueprint import Blueprint
from draftsman.classes.collection import EntityLike
from draftsman.prototypes.constant_combinator import ConstantCombinator

from factorio_circuit_ast.from_blueprint import *


def get_bp(using: str) -> Blueprint:
    blueprint = Blueprint()
    blueprint.load_from_string(using)
    return blueprint


class TestGetNetworkForEntity(unittest.TestCase):
    def test_get_all_connections(self):
        const = ConstantCombinator()
        with self.assertRaises(AssertionError):
            get_all_connections(const, "blue")
        with self.assertRaises(AssertionError):
            get_all_connections(const, "red", "3")
        with self.assertRaises(AssertionError):
            get_all_connections(const, "2", "blue")
        bp = Blueprint()
        bp.entities.append("constant-combinator", id="const1")
        const1: EntityLike = bp.entities["const1"]
        assert isinstance(const1, CircuitConnectableMixin)
        bp.entities.append("constant-combinator", id="const2")
        const2: EntityLike = bp.entities["const2"]
        assert isinstance(const2, CircuitConnectableMixin)
        bp.entities.append("arithmetic-combinator", id="arith")
        arith: EntityLike = bp.entities["arith"]
        assert isinstance(arith, CircuitConnectableMixin)
        bp.add_circuit_connection("red", "const1", "const2")
        bp.add_circuit_connection("red", "arith", "const1", 1, 1)
        bp.add_circuit_connection("green", "arith", "const2", 2, 1)
        self.assertEqual(get_all_connections(const1, "red"), [(const2, 1), (arith, 1)])
        self.assertEqual(get_all_connections(const1, "green"), [])
        self.assertEqual(get_all_connections(const2, "red"), [(const1, 1)])
        self.assertEqual(get_all_connections(const2, "green"), [(arith, 2)])
        self.assertEqual(get_all_connections(arith, "green", "2"), [(const2, 1)])
        self.assertEqual(get_all_connections(arith, "green"), [])
        self.assertEqual(get_all_connections(const2, "green", "2"), [])
