import module;

def subtract as
  \x -> \y ->
    add x (negate y);

def true as 1;
def false as 0;
def Boolean as {true, false};

def negtrue as (true -> false);
def negfalse as (false -> true);

# applying arcs as functions
negt true; # evaluates to false
negf false; # evaluates to true

def not as {negtrue, negfalse};

# applying sets of arcs (maps) as functions
not (not (not true)); # evaluates to false

print "Hello, World!";

import ../../math/algebra;

def true as 1;
def false as 0;

def not as \\x ->
  if (eq x true)
  then false
  else true;

def and as {
  ([true, true] -> true),
  ([true, false] -> false),
  ([false, true] -> false),
  ([false, false] -> false)
};

if (and true false)
then print "Wrong Result!"
else print "CORRECT!";