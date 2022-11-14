# ---------- Arcs and Edges -----------
def thiel as (0 -> 1);

def relationship as ("Bonnie" -- "Clyde");



# ---------- Sequences -----------
def seq as [1, 2, 3];

# [0, 2, 4, 6, 8, 10] :: [Whole]
def ZeroToTen as [* n 2 for n from 0 to 5];

# [3, 33, 303, 3003, 30003..] :: [Whole]
def Threes as [* (+ (^ 10 n) 1) 3 for n from 0];

# [1, 1, 1, 1, 8, 8, 8, 8, 8, 8..] :: [Whole]
def OnesAndEights as [
  if less n 4
  then 1
  else 8
  for n from 0
];

# ---------- Sets -----------