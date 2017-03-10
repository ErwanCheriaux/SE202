import unittest

from parser.dumper    import Dumper
from parser.parser    import parse
from semantics.binder import Binder

class TestDumper(unittest.TestCase):

    def parse_dump(self, text):
        tree = parse(text)
        tree.accept(Binder())
        return tree.accept(Dumper(semantics=True))

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
        self.check("let var a := 5 var b := 5 in a+b end", "let var a := 5 var b := 5 in (a + b) end")

        self.check("let function f() = 1+2 in 1 end", "let function f() = (1 + 2) in 1 end")
        self.check("let function f() = 1 in f() end", "let function f() = 1 in f() end")
        self.check("let function f(a:int, b:int) = a+b in f(4,5) end", "let function f(a: int, b: int) = (a + b) in f(4, 5) end")
        self.check("let function f(): int = 1 + 2 in 1 end", "let function f(): int = (1 + 2) in 1 end")
        self.check("let function f(a: int, b: int, c: int) = 1 in f(1,2,3) end", "let function f(a: int, b: int, c: int) = 1 in f(1, 2, 3) end")

        self.check("let\n\
                        var a := 3\n\
                        var b : int := 4\n\
                        function f(c: int, d: int) = c + d\n\
                        var e : int := 5\n\
                    in\n\
                        e\n\
                    end", "let var a := 3 var b: int := 4 function f(c: int, d: int) = (c + d) var e: int := 5 in e end")

        self.check("let\n\
                        var a := 3\n\
                        function f(b: int) = a + b\n\
                    in\n\
                        f(10)\n\
                    end", "let var a/*e*/ := 3 function f(b: int) = (a/*1*/ + b) in f(10) end")
        
if __name__ == '__main__':
    unittest.main()
