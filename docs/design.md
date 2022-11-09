# Program Structure
A Sageleaf program is a list of statements which can be one of:

**Import Statement**
```sage
import ../module;
```

Imports all definitions from another file.

**Definition Statement**
```sage
def not = {True -> False, False -> True};
```

Defines a module-scope binding which is lazily evaluated when referenced.

**Expression Statement**
```sage
print "Hello, World!";
```

Expression which is eagerly evaluated and the value is discarded. (value is
printed when in REPL mode)

# Modules and Imports
Modules are simply other .sage files. When an import statement is evaluated,
all definition statements from the imported module are added to the current
module's namespace under a qualified name of the module.

```sage
import math

math.abs -8;
math.round 3.98;
```

# Definitions
Definitions are always module-scoped and can only exist at the top-level of
the module. They are used for binding any value to a name. Values include
"functions" and "types".

# Expressions and Expression Statements
Expressions are all eagerly evaluated to a value when encountered by the
interpreter unless they are inside a definition statement. Expressions can be:

**If Expression**
```sage
if < x 5
then "Hello"
else "Bye"
```

Conditionally evaluate to one sub-expression or another.

**Do Expression**
```sage
do print "Evaluating to Pie"
then 3.14
```

Evaluate one sub-expression and discard the value then evaluate to another
sub-expression.

**Let Expression**
```sage
let radius
be 7
in * 3.14 (* radius radius)
```

Locally bind a value to a name in a sub-expression. Can shadow module-level
bindings.

**Function Application**
```sage
not true
```

It's essentially one expression followed by another expression and evaluates by
applying the second expression to the first one recursively (currying).

Note: "Functions" in this case can be any of lambdas, maps and function defs.

```sage
{true -> false, false -> true} true
```

```sage
(\b -> if b is true then false else true) true
```

**Lambda Expression**
```sage
\x -> * x 2
```

Evaluates to an anonymous function. All lambdas have one argument and one
return value. The argument is bound to a locally-scoped identifier in the
sub-expression. Therefore currying is mandatory if we want functions with
multiple arguments:

```sage
\x -> \y -> + x y
```

**Literal Value**
```sage
10.9
```

Expressions can be any of the built-in literal values, including all
composite data structures, such as graphs:

```sage
{
  "cat"     -> "meow",
  "dog"     -> "woof",
  "wolf"    -> "woof",
  "pikachu" -- "pikachu"
}
```

# Literal Values
Literal values fall into two categories - primitive and composite. Composite
values (data structures) contain one or more of the primitive values.

Literal values are assigned the smallest possible built-in data type which
contains them. For example, the literal ```3``` would be assigned the *Natural*
number type.

Composite literals are also assigned the smallest possible type and also
subtypes. For example, the literal ```{0 -> 1}``` would be assigned the type
*Arc (and Natural Natural)*, while the type of the literal
```{0 -> 1, "Hello" -- "World"}``` would be
*MixedMultiGraph (and (or Natural String) (or Natural String))*

Bigger types are contagious in the sense that if we add a Natural number and a
Real number we would get a Real number rather than another Natural.

## Primitive Data Types
For the number types, the smallest possible set is used which can represent the
literal in question. Types are contagious in the sense that operations on
for example a float and a rational will result in a rational usually.

**Unit** = {Unit}

**Boolean** = {True False}

**Complex** = {0 1 -1 3.14 -3.09 22/7 1.3e8 1.9+6i -55-0.8i pi e ..}

**Imaginary** = {6i -0.8i ..}

**Real** = {0 1 -1 3.14 -3.09 22/7 1.3e8 pi e ..}

**Rational** = {0 1 -1 3.14 -3.09 22/7 1.3e8 ..}

**Integer** = {0 1 -1 8 ..}

**Float** = {1.0 3.14 -3.09 1.3e8 ..}

**Natural** = {0 1 8 ..}

**String** = {"a" "ab" "abc123./" ..}

# Composite Data Types
All built-in data structures are immutable. Lists are implemented as a Trie,
sets and maps as sparse vectors, etc. Graphs can have multiple of both directed
edges and undirected (bidirectional) edges and can thus be both undirected,
directed, mixed and multigraphs based on the elements. Maps are simply an alias
for sets of arcs. Ordered maps are sequences of arcs, etc. Graphs are sets of
arcs and edges, multigraphs are sequences of arcs or edges.

**Set**
```sage
{}
{1, 2, 3}
{{}, {1}, {1, 2}}
```

Unordered set of unique values.

**Sequence**
```sage
[]
[1, 2, 3]
["Hello", "World", [1, 0]]
```

Ordered sequence of values.

**Arc**
```sage
true -> false
unit -> 0
"cat" -> "meow"
(a -> b) -> (b -> a)
```

Directed relationship between two values.

**Edge**
```sage
true -- false
(a -> b) -- (0 -- 1)
```

Undirected (or bidirectional) relationship between two values.

# Function Data Types and Inference
Function types are represented by arrow notation on primitive types. Types
are not explicitly written, but are inferred based on the smallest set which
all operations in the definition can be run on. There is a type check step.

*Types are simply sets of values:*
(def true 1)
(def false 0)
(def Boolean {true false})

(def unit false)
(def Unit {unit})

(def Natural (map abs Integer))

*Functions are maps from values to values:*
(def not {true -> false, false -> true})

*Function types are arcs between sets:*
not :: {(Boolean -> Boolean)}