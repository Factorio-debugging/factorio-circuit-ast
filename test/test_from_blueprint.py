import unittest
from draftsman.classes.blueprint import Blueprint
from factorio_circuit_ast.from_blueprint import *


def get_bp(using: str) -> Blueprint:
    blueprint = Blueprint()
    blueprint.load_from_string(using)
    return blueprint


class TestGetNetworkForEntity(unittest.TestCase):
    def test_no_network(self):
        const = ConstantCombinator()
        decider = DeciderCombinator()
        arithmetic = ArithmeticCombinator()
        self.assertEqual(get_network_for_entity(const, "red"), None)
        self.assertEqual(get_network_for_entity(const, "green"), None)
        self.assertEqual(get_network_for_entity(const, "red", 2), None)
        self.assertEqual(get_network_for_entity(const, "green", 2), None)
        self.assertEqual(get_network_for_entity(decider, "red"), None)
        self.assertEqual(get_network_for_entity(decider, "green"), None)
        self.assertEqual(get_network_for_entity(decider, "red", 2), None)
        self.assertEqual(get_network_for_entity(decider, "green", 2), None)
        self.assertEqual(get_network_for_entity(arithmetic, "red"), None)
        self.assertEqual(get_network_for_entity(arithmetic, "green"), None)
        self.assertEqual(get_network_for_entity(arithmetic, "red", 2), None)
        self.assertEqual(get_network_for_entity(arithmetic, "green", 2), None)

    def test_wrong_color(self):
        const = ConstantCombinator()
        with self.assertRaises(AssertionError):
            get_network_for_entity(const, "blue")
        with self.assertRaises(AssertionError):
            get_network_for_entity(const, "yellow")
        get_network_for_entity(const, "red")
        get_network_for_entity(const, "green")

    def test_constant_constant(self):
        # two constant combinators combined with red and green
        bp = get_bp(
            "0eNqdkc1qwzAQhN9lzkpArhUnepVSin+WsBCvjCSXGqN3j2RfAkl7yEUwmt2ZD3ZFd5tp8iwRdgX3TgLs54rAV2lv5S8uE8GCI41QkHYsqszFVuKhd2PH0kbnkRRYBvqF1elLgSRyZNrjNrF8yzx25PPAv0EKkwt510npz3kfR6OwwB50fTS5ZmBP/e5XqkTILkOZ1+XxNDz2clZVgbp6InnhpJTUE2X1LqV5n1L/Sak3yuxul7APh1P4IR/2orOum0vVGFPXpjmldAcZl6FB"
        )
        const1 = bp.entities[0]
        self.assertIsInstance(const1, ConstantCombinator)
        const2 = bp.entities[1]
        self.assertIsInstance(const2, ConstantCombinator)
