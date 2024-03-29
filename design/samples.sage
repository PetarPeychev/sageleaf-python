# Bindings --------------------------------------------------------------------

let x = 42;

let add: Real -> Real -> Real =
   \x -> y -> x + y;

let increment: Real -> Real =
   add 1;

let result: Real =
   add 7 (increment 5);


# Blocks ----------------------------------------------------------------------

Programs are expressions. They evaluate to a single value. In order to have multiple
statements inside an expression, you need to use a block. Blocks evaluate to the last
expression statement in the block, but can contain other intermediate bindings or
expressions, including effectful expressions:

let name: String* = {
   let greeting: String = "Hello!";
   print greeting;
   let name: String* = promptInput "What is your name?";
   name;
};

If a block contains any effectful expressions (of type A -> B*), then the evaluated type
of the block will always be effectful:

let pi: Real* = {
   print "Cooking some delicious Pi...";
   3.1415;
};

This ensures effectful computation is tracked and propagated.

Blocks should generally be avoided if a point-free expression suffices, but may be used
to simplify some large expressions or do effectful composition.

# Do-style IO -----------------------------------------------------------------

# Do structure evaluates an expression once non-lazily in order.


let prompt: String = "Tell me your name: ";

let print: String -> Unit*;

let sayHello: Unit* = print "Hello!" # this will be evaluated only when used

sayHello; # this forces sequential evaluation when encountered by the interpreter once and only once

let getInput: Unit -> String*;

# do-then-then... construction is basically a pipe operator. It chains
# consecutive functions by passing in outputs back into the next inputs
let promptTwoInputs: String -> Pair[String*] =
   \prompt -> {
      # TODO: Perhaps blocks can be useful?
   }


let a : X -> Y

do a;


let printLine: String -> Unit =
   \s ->
      do print s
      then do print "\n";

let name: String = "Petar"

do printLine "Hello, World!";
do print "My name is ";
do print name;

# Algebraic Data Types --------------------------------------------------------

type Bool =
   True: Unit
   or False: Unit

type BaseColour =
   Red
   or Blue
   or Green;

type CompositeColour =
   Red: Real
   and Blue: Real
   and Green: Real;

type List a =
   Empty
   or Head: a and Tail: List a;


# Refinement Types ------------------------------------------------------------

type OptimisticBool =
  Bool where \b -> b;

type PositiveInt =
   Real where \x -> x >= 0;

let abs: Real -> PositiveInt =
   \x ->
   if x < 0 then -x
   else x;

# Refinement Types and ADTs ---------------------------------------------------

type CompositeColour =
   Red: Real where \x -> x >= 0 and x <= 255
   and Blue: Real where \x -> x >= 0 and x <= 255
   and Green: Real where \x -> x >= 0 and x <= 255;

# Monadic IO? -----------------------------------------------------------------

type Char =
  String where \x -> len x < 2;

let getChar: Unit -> IO Char;

let getLine: Unit -> IO String = \u ->
  let getCharRec: IO List Char -> IO List Char = \cl1 ->
    let cl2: IO List Char = getChar Unit;
    map (\x -> cl1 + x) cl2;

  map (\x -> reduce (\x' y' -> x' + y') x) getCharRec IO Empty;

let printChar: Char -> IO Unit;

let printLine: String -> IO Unit = \s ->

# Procedure IO? ---------------------------------------------------------------

p readTextFile: String -> Maybe[String];

// execution order: input -> content -> expression
let readUserInputFile: Unit -> Maybe[String] =
  val input: Maybe[String] = prompt "Enter a file path: ";

  val content: Maybe[String] =
    input
    when Just path -> readTextFile path
    when Nothing -> Nothing;

  \u -> content;

// execution order: lazy simultaneous path1, path2
let readTwoFiles: String -> String -> Pair(Maybe[String], Maybe[String]) =
  \path1 path2 -> Pair(readTextFile path1, readTextFile path2)

// hmmm -----------------------------------------------------------------------

// These are all declarative definitions. They are added to the symbol table
// when sequentially, but evaluation is delayed to when necessary and may be
// left unevaluated. They can be parallelised or memoised
let x: Real = 42;
let add: Real -> Real -> Real = \x -> \y -> x + y;
let increment: Real -> Real = add 1;
let result: Real = add 7 (increment 5);

// These are all imperative ordered procedure calls. For the same local scope
// they must be executed sequentially and can't be parallelised.
val prompt: IO[String -> String];
val input: Maybe[String] = prompt "Enter a file path: ";
val content: Maybe[String] =
  input
  when Just path -> readTextFile path
  when Nothing -> Nothing;

// Effect Types. If "*" means effectful. If "?" means polymorphic on effect.
let mapPure:        (a -> b) -> T[a] ->  T[b];
let mapImpure:      (a -> b*) -> T[a] -> T[b]*;
let mapPolymorphic: (a -> b?) -> T[a] -> T[b]?;

let add: Real -> Real -> Real;
let readFile: String -> String;
let readTwoFiles: String -> String -> String;