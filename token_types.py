"""Define the token kinds recognized by the Flora language."""

from enum import Enum, auto


class TokenType(Enum):
    """Token categories used by Flora's lexer and parser."""

    SPROUT = auto()
    BLOOM = auto()
    BRANCH = auto()
    ROOT = auto()
    DEW = auto()
    PETAL = auto()
    IDENTIFIER = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    LT = auto()
    GT = auto()
    EQ = auto()
    NEQ = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    EOF = auto()