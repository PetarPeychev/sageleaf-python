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