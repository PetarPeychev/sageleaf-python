## Idea
built-in hidden concurrency model

Do a static check after parsing for dependencies between bindings in the same
expression and determine if some can be evaluated in parallel.

Turn list of bindings into list of lists and then map eval to each sublist in
parallel.

## Premise

##