import unittest

from ast.evaluator import Evaluator
from ast.nodes import IntegerLiteral, BinaryOperator
from parser.parser import parse

class TestEvaluator(unittest.TestCase):

    def check(self, ast, expected):
        self.assertEqual(ast.accept(Evaluator()), expected)

    def parse_check(self, str, expected):
        self.assertEqual(parse(str).accept(Evaluator()), expected)

    def test_literal(self):
        self.check(IntegerLiteral(42), 42)

    def test_basic_operator(self):
        self.check(BinaryOperator('+', IntegerLiteral(10), IntegerLiteral(20)), 30)
        self.check(BinaryOperator('-', IntegerLiteral(10), IntegerLiteral(20)), -10)
        self.check(BinaryOperator('-', IntegerLiteral(20), IntegerLiteral(10)), 10)
        self.check(BinaryOperator('*', IntegerLiteral(10), IntegerLiteral(20)), 200)
        self.check(BinaryOperator('/', IntegerLiteral(20), IntegerLiteral(10)), 2)
        self.check(BinaryOperator('|', IntegerLiteral(10), IntegerLiteral(25)), 27)
        self.check(BinaryOperator('&', IntegerLiteral(10), IntegerLiteral(25)), 8)

        self.check(BinaryOperator('<',  IntegerLiteral(10), IntegerLiteral(25)), 1)
        self.check(BinaryOperator('>',  IntegerLiteral(10), IntegerLiteral(25)), 0)
        self.check(BinaryOperator('<=', IntegerLiteral(10), IntegerLiteral(25)), 1)
        self.check(BinaryOperator('>=', IntegerLiteral(10), IntegerLiteral(25)), 0)
        self.check(BinaryOperator('=',  IntegerLiteral(10), IntegerLiteral(25)), 0)
        self.check(BinaryOperator('<>', IntegerLiteral(10), IntegerLiteral(25)), 1)

    def test_priorities(self):
        self.check(BinaryOperator('+', IntegerLiteral(1), BinaryOperator('*', IntegerLiteral(2),  IntegerLiteral(3))), 7)
        self.check(BinaryOperator('+', IntegerLiteral(1), BinaryOperator('*', IntegerLiteral(-2), IntegerLiteral(3))), -5)
        self.check(BinaryOperator('-', IntegerLiteral(1), BinaryOperator('*', IntegerLiteral(2),  IntegerLiteral(3))), -5)
        self.check(BinaryOperator('+', IntegerLiteral(1), BinaryOperator('/', IntegerLiteral(6),  IntegerLiteral(3))), 3)

        self.check(BinaryOperator('<',  IntegerLiteral(21), BinaryOperator('+', IntegerLiteral(10),  IntegerLiteral(5))), 0)
        self.check(BinaryOperator('<=', IntegerLiteral(21), BinaryOperator('+', IntegerLiteral(10),  IntegerLiteral(5))), 0)
        self.check(BinaryOperator('>',  IntegerLiteral(21), BinaryOperator('+', IntegerLiteral(10),  IntegerLiteral(5))), 1)
        self.check(BinaryOperator('>=', IntegerLiteral(21), BinaryOperator('+', IntegerLiteral(10),  IntegerLiteral(5))), 1)
        self.check(BinaryOperator('=',  IntegerLiteral(21), BinaryOperator('+', IntegerLiteral(10),  IntegerLiteral(5))), 0)
        self.check(BinaryOperator('<>', IntegerLiteral(21), BinaryOperator('+', IntegerLiteral(10),  IntegerLiteral(5))), 1)

        self.check(BinaryOperator('|', IntegerLiteral(10), BinaryOperator('*', IntegerLiteral(5), IntegerLiteral(5))),   27)
        self.check(BinaryOperator('|', IntegerLiteral(10), BinaryOperator('<', IntegerLiteral(5), IntegerLiteral(5))),   10)
        self.check(BinaryOperator('&', IntegerLiteral(10), BinaryOperator('*', IntegerLiteral(5), IntegerLiteral(5))),   8)
        self.check(BinaryOperator('&', IntegerLiteral(10), BinaryOperator('<', IntegerLiteral(5), IntegerLiteral(5))),   0)
        self.check(BinaryOperator('|', IntegerLiteral(10), BinaryOperator('&', IntegerLiteral(57), IntegerLiteral(29))), 27)

    def test_parse_literal(self):
        self.parse_check('42', 42)

    def test_parse_sequence(self):
        self.parse_check('1+(2+3)+4', 10)
        self.parse_check('1+(2+3)*4', 21)
        self.parse_check('1+(2+2)/4', 2)
        self.parse_check('1+(2<2)+50', 51)
        self.parse_check('1+(2=2)+50', 52)
        self.parse_check('1+(3|4)+50', 58)

    def test_precedence(self):
        self.parse_check('1 + 2 * 3', 7)
        self.parse_check('2 * 3 + 1', 7)
        self.parse_check('1 + 6 / 3', 3)
        self.parse_check('6 / 3 + 1', 3)
        self.parse_check('6 | 3 + 1', 6)
        self.parse_check('6 & 3 + 1', 4)
        self.parse_check('6 < 3 + 9', 1)

if __name__ == '__main__':
    unittest.main()
