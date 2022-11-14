import module;

# :: {Any}
def AnyValue as {any _};

# :: {Complex}
def AnyNegative as {any x where x < 0};

# :: {(Boolean -> Boolean)}
def not as {
  true -> false,
  false -> true
};

# :: {(Complex -> Complex)}
def abs as {
  (any x where x < 0 -> negate x),
  (any x -> x)
};

# :: {(Complex -> Complex)}
def subtract as {
  (any x -> {
    (any y -> add x (negate y))
  })
};

# :: {(Integer -> Integer), (String -> String)}
def + as {
  (any x where Integer x -> {
    (any y where Integer y ->
      add x y)}),

  (any a where String a -> {
    (any b where String b ->
      cat a b)})
};

+ 10 18; # 28
+ "Hello, " "World!"; # Hello, World!

# :: {Integer}
def NegativeInteger as {
  any x where and (Integer x) (< x 0)
};

# :: {Any}
def Any as {any _};

# ::
def IntegersAndBoolsAndUnit as {
  true,
  false,
  unit,
  any x where Integer x
};

def true as 1;
def false as 0;
def Boolean as {true, false};

print "Hello, World!";

import ../../math/algebra;

def true as 1;
def false as 0;

def not as \x ->
  if (eq x true)
  then false
  else true;

def not as {
  (true -> false),
  (false -> true)
};

def and as {
  ([true, true] -> true),
  ([true, false] -> false),
  ([false, true] -> false),
  ([false, false] -> false)
};

if (and true false)
then print "Wrong Result!"
else print "CORRECT!";