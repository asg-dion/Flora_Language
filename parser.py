"""Provide the parser that will validate Flora token sequences."""

from token_types import TokenType


class VarDeclNode:
    """Represent a Flora variable declaration."""

    def __init__(self, datatype, identifier, value_expr):
        self.datatype = datatype
        self.identifier = identifier
        self.value_expr = value_expr

    def __repr__(self):
        return (
            f"VarDeclNode(datatype={self.datatype!r}, "
            f"identifier={self.identifier!r}, value_expr={self.value_expr!r})"
        )


class AssignNode:
    """Represent an assignment statement."""

    def __init__(self, identifier, value_expr):
        self.identifier = identifier
        self.value_expr = value_expr

    def __repr__(self):
        return (
            f"AssignNode(identifier={self.identifier!r}, "
            f"value_expr={self.value_expr!r})"
        )


class BloomNode:
    """Represent a Flora output statement."""

    def __init__(self, value_expr):
        self.value_expr = value_expr

    def __repr__(self):
        return f"BloomNode(value_expr={self.value_expr!r})"


class BranchNode:
    """Represent a one-way branch with one following statement."""

    def __init__(self, condition_expr, statement):
        self.condition_expr = condition_expr
        self.statement = statement

    def __repr__(self):
        return (
            f"BranchNode(condition_expr={self.condition_expr!r}, "
            f"statement={self.statement!r})"
        )


class BinaryOpNode:
    """Represent an arithmetic binary operation."""

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryOpNode(left={self.left!r}, operator={self.operator!r}, "
            f"right={self.right!r})"
        )


class ComparisonNode:
    """Represent a comparison expression."""

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"ComparisonNode(left={self.left!r}, operator={self.operator!r}, "
            f"right={self.right!r})"
        )


class LiteralNode:
    """Represent an integer, floating-point, or string literal."""

    def __init__(self, value, flora_type):
        self.value = value
        self.flora_type = flora_type

    def __repr__(self):
        return f"LiteralNode(value={self.value!r}, flora_type={self.flora_type!r})"


class IdentifierNode:
    """Represent a variable reference."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode(name={self.name!r})"


class Parser:
    """Parse a token list into Flora statement nodes."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """Return the current token without consuming it."""
        if self.pos >= len(self.tokens):
            return TokenType.EOF, None
        return self.tokens[self.pos]

    def advance(self):
        """Return and consume the current token."""
        token = self.peek()
        if self.pos < len(self.tokens):
            self.pos += 1
        return token

    def expect(self, token_type):
        """Consume the expected token type or raise a positioned syntax error."""
        current_type, lexeme = self.peek()
        if current_type != token_type:
            raise SyntaxError(
                f"Syntax error at token position {self.pos}: expected "
                f"{token_type.name}, found {current_type.name} ({lexeme!r})"
            )
        return self.advance()

    def parse(self):
        """Parse statements until the end-of-file token is reached."""
        statements = []
        while self.peek()[0] != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        """Dispatch to the parser for the current statement type."""
        token_type, _ = self.peek()
        if token_type == TokenType.SPROUT:
            return self.parse_var_decl()
        if token_type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        if token_type == TokenType.BLOOM:
            return self.parse_bloom()
        if token_type == TokenType.BRANCH:
            return self.parse_branch()
        raise SyntaxError(
            f"Syntax error at token position {self.pos}: expected a statement, "
            f"found {token_type.name}"
        )

    def parse_expression(self):
        """Parse addition and subtraction, associating operators to the left."""
        expression = self.parse_term()
        while self.peek()[0] in (TokenType.PLUS, TokenType.MINUS):
            _, operator = self.advance()
            right = self.parse_term()
            expression = BinaryOpNode(expression, operator, right)
        return expression

    def parse_term(self):
        """Parse multiplication and division, associating operators to the left."""
        term = self.parse_factor()
        while self.peek()[0] in (TokenType.STAR, TokenType.SLASH):
            _, operator = self.advance()
            right = self.parse_factor()
            term = BinaryOpNode(term, operator, right)
        return term

    def parse_factor(self):
        """Parse a literal, identifier, or parenthesized expression."""
        token_type, lexeme = self.peek()
        if token_type == TokenType.INT_LITERAL:
            self.advance()
            return LiteralNode(int(lexeme), "root")
        if token_type == TokenType.FLOAT_LITERAL:
            self.advance()
            return LiteralNode(float(lexeme), "dew")
        if token_type == TokenType.STRING_LITERAL:
            self.advance()
            return LiteralNode(lexeme, "petal")
        if token_type == TokenType.IDENTIFIER:
            self.advance()
            return IdentifierNode(lexeme)
        if token_type == TokenType.LPAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expression

        raise SyntaxError(
            f"Syntax error at token position {self.pos}: expected a literal, "
            f"identifier, or '(', found {token_type.name} ({lexeme!r})"
        )

    def parse_comparison(self):
        """Parse a comparison between two arithmetic expressions."""
        left = self.parse_expression()
        if self.peek()[0] not in (
            TokenType.LT,
            TokenType.GT,
            TokenType.EQ,
            TokenType.NEQ,
        ):
            token_type, lexeme = self.peek()
            raise SyntaxError(
                f"Syntax error at token position {self.pos}: expected a comparison "
                f"operator, found {token_type.name} ({lexeme!r})"
            )

        _, operator = self.advance()
        right = self.parse_expression()
        return ComparisonNode(left, operator, right)

    def parse_var_decl(self):
        """Parse a variable declaration statement."""
        self.expect(TokenType.SPROUT)
        token_type, datatype = self.peek()
        if token_type not in (TokenType.ROOT, TokenType.DEW, TokenType.PETAL):
            raise SyntaxError(
                f"Syntax error at token position {self.pos}: expected ROOT, DEW, "
                f"or PETAL, found {token_type.name} ({datatype!r})"
            )
        self.advance()
        _, identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value_expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return VarDeclNode(datatype, identifier, value_expr)

    def parse_assignment(self):
        """Parse an assignment statement."""
        _, identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value_expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return AssignNode(identifier, value_expr)

    def parse_bloom(self):
        """Parse an output statement."""
        self.expect(TokenType.BLOOM)
        value_expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return BloomNode(value_expr)

    def parse_branch(self):
        """Parse a one-way branch statement."""
        self.expect(TokenType.BRANCH)
        self.expect(TokenType.LPAREN)
        condition_expr = self.parse_comparison()
        self.expect(TokenType.RPAREN)
        statement = self.parse_statement()
        return BranchNode(condition_expr, statement)