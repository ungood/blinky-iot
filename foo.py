from decimal import Decimal
import pyparsing as pp

sign = pp.oneOf(['+', '-'])
point = pp.Literal('.')
lparen = pp.Literal('(')
rparen = pp.Literal(')')
separator = pp.Literal(',')

digits = pp.Word(pp.nums)
decimal_part = pp.Combine(digits + point + pp.Optional(digits)) | pp.Combine(pp.Optional(point) + digits)
decimal = pp.Combine(pp.Optional(sign) + decimal_part).setParseAction(lambda t: Decimal(t[0]))

identifier = pp.Word(pp.alphas)

expr = pp.Forward()
argument = expr
arglist = pp.Zero
function_call = pp.Combine(identifier + lparen + )

grammar = pp.ZeroOrMore(decimal)

test_data = """
1.3 -1.3
0
10
0000003
-1
+1
1.3
0.3
00.04
00.30
"""

for d in grammar.parseString(test_data):
    print(str(d))