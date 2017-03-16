import unittest

from parser.dumper    import Dumper
from parser.parser    import parse
from semantics.binder import Binder
from typer.typer      import Typer

class TestDumper(unittest.TestCase):

    def parse_dump(self, text):
        tree = parse(text)
        tree.accept(Binder())
        tree.accept(Typer())
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

    def test_ifthenelse(self):
        self.check("if 5=5 then 2 else 3", "if (5 = 5) then 2 else 3")
        self.check("if 5<>5 then 2+5 else 5+5", "if (5 <> 5) then (2 + 5) else (5 + 5)")

    def test_ifthenelse(self):
        self.check("let var a := 12 in if 1 then a := 3 end", "let var a: int := 12 in if 1 then a := 3 end")

    def test_let_var(self):
        self.check("let var a := 5 in a end", "let var a: int := 5 in a end")
        self.check("let var a: int := 5 in a end", "let var a: int := 5 in a end")
        self.check("let var a := 5 var b := a in a+b end", "let var a: int := 5 var b: int := a in (a + b) end")

    def test_let_function(self):
        self.check("let function f() = 1+2 in 1 end", "let function f(): int = (1 + 2) in 1 end")
        self.check("let function f() = f() in f() end", "let function f() = f() in f() end")
        self.check("let function f(a:int, b:int) = a+b in f(4,5) end", "let function f(a: int, b: int): int = (a + b) in f(4, 5) end")
        self.check("let function f(): int = 1 + 2 in 1 end", "let function f(): int = (1 + 2) in 1 end")
        self.check("let function f(a: int, b: int, c: int) = 1 in f(1,2,3) end", "let function f(a: int, b: int, c: int): int = 1 in f(1, 2, 3) end")

    def test_code(self):
        self.check("let\n\
                        var a := 3\n\
                        var b : int := 4\n\
                        function f(c: int, d: int) = c + d\n\
                        var e : int := 5\n\
                    in\n\
                        e\n\
                    end", "let var a: int := 3 var b: int := 4 function f(c: int, d: int): int = (c + d) var e: int := 5 in e end")

        self.check("let\n\
                        var a := 3\n\
                        function f(b: int) = a + b\n\
                    in\n\
                        f(10)\n\
                    end", "let var a/*e*/: int := 3 function f(b: int): int = (a/*1*/ + b) in f(10) end")

    def test_comment(self):
        self.check("1+3 // clqjzdi&é678 dzo!!", "(1 + 3)")
        self.check("1+3 /* duh789 edeu /* clqjzdi&é678 dzo!! */ ùùùù */", "(1 + 3)")

    def test_seqexp(self):
        self.check("let var a := 1 in end", "let var a: int := 1 in () end")
        self.check("let var a := 1 in a end", "let var a: int := 1 in a end")
        self.check("let var a := 1 in (a) end", "let var a: int := 1 in a end")
        self.check("let var a := 1 in a; a; a; a; a end", "let var a: int := 1 in (a; a; a; a; a) end")

    def test_assignment(self):
        self.check("let var a := 3 function f(b: int) = (b := b + 1; a := a + b * 2) in f(5) end", \
                   "let var a/*e*/: int := 3 function f(b: int) = (b := (b + 1); a/*1*/ := (a/*1*/ + (b * 2))) in f(5) end")

    def test_while(self):
        self.check("let\n\
                        function fact(n: int) =\n\
                            let var result := 1 in\n\
                                while n > 0 do (result := result * n; n := n - 1);\n\
                                result\n\
                            end\n\
                    in\n\
                        fact(5)\n\
                    end", "let function fact(n: int): int = let var result: int := 1 in while n > 0 do (result := result * n; n := n - 1); result end in fact(5) end")

if __name__ == '__main__':
    unittest.main()
