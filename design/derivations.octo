let myAdd: Real -> Real -> Real =
  \x y -> add x y;

// Parsed as:
Program = Module

Module = Binding ";"

Binding = "let" Identifier ":" Type "=" Expression

Identifier = "myAdd"

Type = PrimitiveType "->" Type2

PrimitiveType = "Real"

Type2 = PrimitiveType2 "->" Type3

PrimitiveType2 = "Real"

Type3 = PrimitiveType3

PrimitiveType3 = "Real"

Expression = "\\" Identifier2 Identifier3 "->" Expression2

Identifier2 = "x"

Identifier3 = "y"

Expression2 = Identifier4 Identifier5 Identifier6

Identifier4 = "add"

Identifier5 = "x"

Identifier6 = "y"