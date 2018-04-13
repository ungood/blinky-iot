"""
Blong - "Blinky Light Object Notation": An extension to JSON that can describe animations to display on a 1-D LED strip.

All valid Blong strings are valid JSON strings, although the reverse is not true.

A blong can be:
    a single, solid color
    a texture - an array of colors
    an object - which can be interpreted as a function that produces textures.
"""

blong_bnf = """
blong : color | texture | object
color : hex_color | rgb_color | hsl_color
texture:  
"""

import pyparsing as pp
import numpy as np

def rgb256(r, g, b):
    return (r, g, b)
    
def json_string(expr):
    """Helper to define an expression quoted as a JSON string."""
    return pp.Suppress("\"") + expr + pp.Suppress("\"")
    
def json_list(element):
    """Helper to define a comma-separated list, enclosed in JSON brackets."""
    return pp.Group(pp.Suppress('[') + pp.Optional(pp.delimitedList(element)) + pp.Suppress(']'))

# Constants
TRUE = pp.Keyword("true").setParseAction(pp.replaceWith(True))
FALSE = pp.Keyword("false").setParseAction(pp.replaceWith(False))
NULL = pp.Keyword("null").setParseAction(pp.replaceWith(None))

# Future Enhancment
number = pp.Combine(
    pp.Optional('-') +
    ('0' | pp.Word('123456789', pp.nums)) +
    pp.Optional('.' + pp.Word(pp.nums)) +
    pp.Optional(pp.Word('eE', exact=1) + pp.Word(pp.nums + '+-', pp.nums)))
number.setParseAction(lambda tokens: float(tokens[0]))

# Future enhancement
def parseNumpyArray(tokens):
    return np.array(list(tokens[0]))

array = pp.Forward()
element = ( number | array )
array << pp.Group(pp.Suppress('[') + pp.Optional(pp.delimitedList(element)) + pp.Suppress(']'))
array.setParseAction(parseNumpyArray)

hex1 = pp.Word(pp.hexnums, exact=1).setParseAction(lambda tokens: int(tokens[0] + tokens[0], 16))
hex2 = pp.Word(pp.hexnums, exact=2).setParseAction(lambda tokens: int(tokens[0], 16))
hex_color = pp.Suppress('#') + (hex1 * 3 | hex2 * 3)
hex_color.setParseAction(lambda tokens: (tokens[0], tokens[1], tokens[2]))
color = quote(hex_color)  # TODO: rgb and hsl colors

texture = json_list(color)

identifier = pp.Word(pp.alphas + "_")

string = pp.quotedString
name = string
value = ( string | number | array | TRUE | FALSE | NULL )
definition = pp.Group(name + pp.Suppress(':') + value)
definitions = pp.delimitedList(definition)

blong = hex_color | texture | dictionary
#pp.Dict(pp.Suppress('{') + pp.Optional(definitions) + pp.Suppress('}'))
    
if __name__ == "__main__":
    hex_color.runTests(["#000", "#abc", "#fff", "#abc123")
    
    color.runTests("""
        #000
        #fff
        #000000
        #ff0000
        #00ff00
        #123456
        #abcdef

        invalid
        #invalid
        000
        """)
    
    # testdata = """
#     {
#         "zero": 0,
#         "zero_vec": [0],
#         "zero_mat": [[0]],
#         "empty_vec": [],
#         "empty_mat": [[]],
#         "foo": [[[[[0]]]]],
#         "vec3": [1, 2, 3],
#         "mat3": [[1, 2, 3],
#                  [4, 5, 6],
#                  [7, 8, 9]],
#         "red": [1, 0, 0],
#         "green": [0, 1, 0],
#         "blue": [0, 0, 1],
#         "lerp": "left, right, alpha -> (left * alpha) + (right * (1-alpha))",
#         "purple": "lerp(red, blue)"
#     }
#     """
#
#     from pprint import pprint
#     results = blong.parseString(testdata)
#
#     pprint(results.asList())
#     print("----")
#     pprint(results.red + results.blue)

