import unittest

from factorio_circuit_ast.ASTNode import *


class ASTNodeImpl(ASTNode):
    def cli_repr(self) -> str:
        ...

    def _inner_to_ir(self) -> str:
        return "from node"

    def tick(self) -> None:
        ...


class TestASTNode(unittest.TestCase):
    def test_set_alias(self):
        with self.assertRaises(ValueError):
            ASTNodeImpl("something", alias="sad fox")
        with self.assertRaises(ValueError):
            ASTNodeImpl("something", alias="dotted.name")
        ASTNodeImpl("something", alias="testing_all_1_special_characters")

    def test_to_ir(self):
        node = ASTNodeImpl("something", nid=1000)
        self.assertEqual(node.id, 1000)
        self.assertEqual(node.to_ir(), "id=1000:from node")
        node = ASTNodeImpl("something", nid=10000, alias="descriptive_alias")
        self.assertEqual(node.alias, "descriptive_alias")
        self.assertEqual(node.to_ir(), "id=10000 alias=descriptive_alias:from node")
