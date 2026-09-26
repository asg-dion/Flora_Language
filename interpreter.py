"""Provide the interpreter that will execute valid Flora statements."""

import operator

from parser import (
    AssignNode,
    BinaryOpNode,
    BloomNode,
    BranchNode,
    ComparisonNode,
    IdentifierNode,
    LiteralNode,
    VarDeclNode,
)


class Interpreter:
    """Dispatch Flora statement nodes for execution."""

    def __init__(self, statements):
        self.statements = statements
        self.symbol_table = {}

    def run(self):
        """Execute each statement in the program in order."""
        for statement in self.statements:
            self.execute_statement(statement)

    def evaluate_expression(self, node):
        """Evaluate an expression node and return its value and Flora type."""
        if isinstance(node, LiteralNode):
            return node.value, node.flora_type
        if isinstance(node, IdentifierNode):
            if node.name not in self.symbol_table:
                raise RuntimeError(f"undefined variable: {node.name}")
            value, flora_type = self.symbol_table[node.name]
            return value, flora_type
        if isinstance(node, BinaryOpNode):
            left_value, left_type = self.evaluate_expression(node.left)
            right_value, right_type = self.evaluate_expression(node.right)

            if left_type == "petal" or right_type == "petal":
                if (
                    node.operator == "+"
                    and left_type == "petal"
                    and right_type == "petal"
                ):
                    return left_value + right_value, "petal"
                raise TypeError("petal values only support '+' concatenation")

            if left_type not in ("root", "dew") or right_type not in (
                "root",
                "dew",
            ):
                raise TypeError(
                    f"operator {node.operator!r} requires numeric operands"
                )

            operations = {
                "+": operator.add,
                "-": operator.sub,
                "*": operator.mul,
                "/": operator.truediv,
            }
            if node.operator not in operations:
                raise TypeError(f"unsupported arithmetic operator: {node.operator!r}")

            value = operations[node.operator](left_value, right_value)
            flora_type = "dew" if "dew" in (left_type, right_type) else "root"
            if flora_type == "dew":
                value = float(value)
            elif node.operator == "/":
                value = int(value)
            return value, flora_type
        if isinstance(node, ComparisonNode):
            left_value, _ = self.evaluate_expression(node.left)
            right_value, _ = self.evaluate_expression(node.right)
            comparisons = {
                "<": operator.lt,
                ">": operator.gt,
                "==": operator.eq,
                "!=": operator.ne,
            }
            if node.operator not in comparisons:
                raise RuntimeError(
                    f"unsupported comparison operator: {node.operator!r}"
                )
            return comparisons[node.operator](left_value, right_value), "bool"
        raise RuntimeError(
            f"Unsupported expression node type: {type(node).__name__}"
        )

    def _coerce_value(self, value, flora_type, declared_type, identifier):
        if (
            declared_type == "root"
            and flora_type == "root"
            and type(value) is int
        ):
            return value
        if (
            declared_type == "dew"
            and flora_type in ("root", "dew")
            and type(value) in (int, float)
        ):
            return float(value)
        if (
            declared_type == "petal"
            and flora_type == "petal"
            and isinstance(value, str)
        ):
            return value
        raise TypeError(
            f"Cannot assign {flora_type} value to {declared_type} variable "
            f"{identifier!r}"
        )

    def execute_statement(self, node):
        """Dispatch a statement node to its corresponding executor."""
        if isinstance(node, VarDeclNode):
            return self.execute_var_decl(node)
        if isinstance(node, AssignNode):
            return self.execute_assignment(node)
        if isinstance(node, BloomNode):
            return self.execute_bloom(node)
        if isinstance(node, BranchNode):
            return self.execute_branch(node)
        raise RuntimeError(f"Unsupported AST node type: {type(node).__name__}")

    def execute_var_decl(self, node):
        """Execute a variable declaration."""
        value, flora_type = self.evaluate_expression(node.value_expr)
        value = self._coerce_value(
            value,
            flora_type,
            node.datatype,
            node.identifier,
        )
        self.symbol_table[node.identifier] = (value, node.datatype)

    def execute_assignment(self, node):
        """Execute an assignment."""
        if node.identifier not in self.symbol_table:
            raise RuntimeError(f"undefined variable: {node.identifier}")

        _, declared_type = self.symbol_table[node.identifier]
        value, flora_type = self.evaluate_expression(node.value_expr)
        value = self._coerce_value(
            value,
            flora_type,
            declared_type,
            node.identifier,
        )
        self.symbol_table[node.identifier] = (value, declared_type)

    def execute_bloom(self, node):
        """Execute an output statement."""
        value, _ = self.evaluate_expression(node.value_expr)
        print(value)

    def execute_branch(self, node):
        """Execute a one-way branch statement."""
        value, flora_type = self.evaluate_expression(node.condition_expr)
        if flora_type != "bool" or not isinstance(value, bool):
            raise TypeError("branch condition must evaluate to bool")
        if value:
            self.execute_statement(node.statement)