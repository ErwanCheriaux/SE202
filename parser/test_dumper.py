import unittest

from parser.dumper import Dumper
from parser.parser import parse

class TestDumper(unittest.TestCase):

    def parse_dump(self, text):
        tree = parse(text)
        return tree.accept(Dumper(semantics=False))

    def check(self, text, expected):
        self.assertEqual(self.parse_dump(text), expected)

    def test_literal(self):
        self.check("42", "42")

    def test_priority(self):
        self.check("3+1-2", "((3 + 1) - 2)")
        self.check("3-1+2", "((3 - 1) + 2)")
        self.check("3-1-2", "((3 - 1) - 2)")

        self.check("1+2*3", "(1 + (2 * 3))")
        self.check("2*3+1", "((2 * 3) + 1)")

        self.check("1+2/3", "(1 + (2 / 3))")
        self.check("2/3+1", "((2 / 3) + 1)")

        self.check("6|3+1", "(6 | (3 + 1))")
        self.check("3+1|6", "((3 + 1) | 6)")

        self.check("6&3+1", "(6 & (3 + 1))")
        self.check("3+1&6", "((3 + 1) & 6)")

        self.check("6|3&1", "(6 | (3 & 1))")
        self.check("3&1|6", "((3 & 1) | 6)")

        self.check("1+2<3", "((1 + 2) < 3)")
        self.check("2<3+1", "(2 < (3 + 1))")

        self.check("1+2>3", "((1 + 2) > 3)")
        self.check("2>3+1", "(2 > (3 + 1))")

        self.check("1+2<=3", "((1 + 2) <= 3)")
        self.check("2<=3+1", "(2 <= (3 + 1))")

        self.check("1+2>=3", "((1 + 2) >= 3)")
        self.check("2>=3+1", "(2 >= (3 + 1))")

        self.check("1+2=3", "((1 + 2) = 3)")
        self.check("2=3+1", "(2 = (3 + 1))")

        self.check("1+2<>3", "((1 + 2) <> 3)")
        self.check("2<>3+1", "(2 <> (3 + 1))")

        self.check("if 5=5 then 2 else 3", "if (5 = 5) then 2 else 3")
        self.check("if 5<>5 then 2+5 else 5+5", "if (5 <> 5) then (2 + 5) else (5 + 5)")

        self.check("let var a := 5 in a end", "let var a := 5 in a end")
        self.check("let var a: int := 5 in a end", "let var a: int := 5 in a end")
        self.check("let var a := 5 var b := 5 in a+b end", "let var a := 5var b := 5 in (a + b) end")

        self.check("let function f() = 1+2 in 1 end", "let function f() = (1 + 2) in 1 end")
        self.check("let function f(): int = 1+2 in 1 end", "let function f(): int = (1 + 2) in 1 end")

if __name__ == '__main__':
    unittest.main()
