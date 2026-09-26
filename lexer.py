"""Provide the lexer that will turn Flora source into tokens."""

from token_types import TokenType

_KEYWORDS = {
    "sprout": TokenType.SPROUT,
    "bloom": TokenType.BLOOM,
    "branch": TokenType.BRANCH,
    "root": TokenType.ROOT,
    "dew": TokenType.DEW,
    "petal": TokenType.PETAL,
}

_SINGLE_CHARACTER_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "=": TokenType.ASSIGN,
    "<": TokenType.LT,
    ">": TokenType.GT,
    ";": TokenType.SEMICOLON,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
}


class Lexer:
    """Hold Flora source and the current scanning position."""

    def __init__(self, source):
        """Initialize the lexer with source text and a starting position."""
        self.source = source
        self.pos = 0

    def peek(self):
        """Return the current character, or None when the source is exhausted."""
        if self.is_at_end():
            return None
        return self.source[self.pos]

    def advance(self):
        """Return the current character and advance, or None at end of source."""
        character = self.peek()
        if character is not None:
            self.pos += 1
        return character

    def is_at_end(self):
        """Return whether the scanning position has reached the source length."""
        return self.pos >= len(self.source)

    def _scan_string(self):
        """Return a string literal token, preserving its contents verbatim."""
        self.advance()
        string_start = self.pos
        while not self.is_at_end() and self.peek() != '"':
            self.advance()
        string_value = self.source[string_start:self.pos]
        if self.peek() == '"':
            self.advance()
        return TokenType.STRING_LITERAL, string_value

    def _scan_word(self):
        """Return a keyword or identifier beginning with a letter."""
        word_start = self.pos
        self.advance()
        while (
            self.peek() is not None
            and (self.peek().isalnum() or self.peek() == "_")
        ):
            self.advance()
        word = self.source[word_start:self.pos]
        return _KEYWORDS.get(word, TokenType.IDENTIFIER), word

    def _scan_number(self):
        """Return an integer or floating-point numeric token."""
        number_start = self.pos
        while self.peek() is not None and self.peek() in "0123456789":
            self.advance()

        token_type = TokenType.INT_LITERAL
        if self.peek() == ".":
            dot_position = self.pos
            self.advance()
            if self.peek() is None or self.peek() not in "0123456789":
                raise ValueError(
                    "Malformed number at character position "
                    f"{dot_position + 1}: expected a digit after '.'"
                )
            while self.peek() is not None and self.peek() in "0123456789":
                self.advance()
            token_type = TokenType.FLOAT_LITERAL

        return token_type, self.source[number_start:self.pos]

    def _scan_symbol(self):
        """Return a supported symbol token, or None for an unsupported symbol."""
        symbol = self.advance()
        if symbol == "=":
            if self.peek() == "=":
                self.advance()
                return TokenType.EQ, "=="
            return TokenType.ASSIGN, symbol
        if symbol == "!":
            if self.peek() == "=":
                self.advance()
                return TokenType.NEQ, "!=" 
            return None

        token_type = _SINGLE_CHARACTER_TOKENS.get(symbol)
        if token_type is None:
            return None
        return token_type, symbol

    def tokenize(self):
        """Scan source through a single dispatch loop and return all tokens."""
        tokens = []

        while not self.is_at_end():
            character = self.peek()
            if character in (" ", "\t", "\n"):
                self.advance()
            elif character == '"':
                tokens.append(self._scan_string())
            elif character in "0123456789":
                tokens.append(self._scan_number())
            elif character.isalpha():
                tokens.append(self._scan_word())
            else:
                token = self._scan_symbol()
                if token is not None:
                    tokens.append(token)

        tokens.append((TokenType.EOF, None))
        return tokens


if __name__ == "__main__":
    sample_source = """\
sprout root trees = 10;
sprout dew temperature = 28.5;
sprout petal biome = "Rainforest";
sprout root saplings = 5;
trees = trees + saplings;
sprout dew rainfall = 20.5;
rainfall = rainfall - 5.0;
sprout root area = 4;
area = area * 2;
sprout dew water = 100.0;
water = water / 2;
branch(trees > 5)
bloom "Forest is thriving";
bloom trees;
bloom "Welcome to Flora";
bloom trees + saplings;
"""
    for token_type, value in Lexer(sample_source).tokenize():
        print(f"{token_type.name}({value!r})")