"""Tokenize a Flora source file and write stripped and reserved-token outputs."""

from pathlib import Path
import sys

from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from token_types import TokenType

_WORD_TOKEN_TYPES = {
    TokenType.SPROUT,
    TokenType.BLOOM,
    TokenType.BRANCH,
    TokenType.ROOT,
    TokenType.DEW,
    TokenType.PETAL,
    TokenType.IDENTIFIER,
    TokenType.INT_LITERAL,
    TokenType.FLOAT_LITERAL,
}

_RESERVED_TOKEN_TYPES = {
    TokenType.SPROUT,
    TokenType.BLOOM,
    TokenType.BRANCH,
    TokenType.ROOT,
    TokenType.DEW,
    TokenType.PETAL,
    TokenType.PLUS,
    TokenType.MINUS,
    TokenType.STAR,
    TokenType.SLASH,
    TokenType.ASSIGN,
    TokenType.LT,
    TokenType.GT,
    TokenType.EQ,
    TokenType.NEQ,
    TokenType.LPAREN,
    TokenType.RPAREN,
    TokenType.SEMICOLON,
}


def reconstruct_source(tokens):
    """Rebuild source with token boundaries and string contents preserved."""
    source_parts = []
    previous_type = None

    for token_type, lexeme in tokens:
        if token_type == TokenType.EOF:
            continue

        if source_parts and (
            (previous_type in _WORD_TOKEN_TYPES and token_type in _WORD_TOKEN_TYPES)
            or (
                previous_type == TokenType.ASSIGN
                and token_type in {TokenType.ASSIGN, TokenType.EQ}
            )
        ):
            source_parts.append(" ")

        if token_type == TokenType.STRING_LITERAL:
            source_parts.append(f'"{lexeme}"')
        else:
            source_parts.append(lexeme)
        previous_type = token_type

    return "".join(source_parts)


def main():
    """Run the Flora lexer, parser, and interpreter for a source file."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <source.flora>")
        return 2

    source_path = Path(sys.argv[1])
    source = source_path.read_text(encoding="utf-8")
    tokens = Lexer(source).tokenize()

    output_directory = source_path.resolve().parent
    stripped_source = reconstruct_source(tokens)
    reserved_words = [
        lexeme for token_type, lexeme in tokens
        if token_type in _RESERVED_TOKEN_TYPES
    ]

    (output_directory / "output_stripped.flora").write_text(
        stripped_source,
        encoding="utf-8",
    )
    (output_directory / "output_reserved_words.txt").write_text(
        "\n".join(reserved_words) + ("\n" if reserved_words else ""),
        encoding="utf-8",
    )

    try:
        statements = Parser(tokens).parse()
    except SyntaxError as error:
        print(f"Syntax Error: {error}")
        return 1

    try:
        Interpreter(statements).run()
    except (RuntimeError, TypeError, ArithmeticError) as error:
        print(f"Runtime Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())